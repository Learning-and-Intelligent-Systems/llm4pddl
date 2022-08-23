"""Tests for utils.py."""

import os
import tempfile

import numpy as np
import pytest
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from llm4pddl import utils
from llm4pddl.structs import Datum, Task


@pytest.fixture(scope="module", name="domain_file")
def _create_domain_file():
    domain_str = """;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; 4 Op-blocks world
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block)
  (:predicates (on ?x - block ?y - block)
	       (ontable ?x - block)
	       (clear ?x - block)
	       (handempty)
	       (holding ?x - block)
	       )

  (:action pick-up
	     :parameters (?x - block)
	     :precondition (and (clear ?x) (ontable ?x) (handempty))
	     :effect
	     (and (not (ontable ?x))
		   (not (clear ?x))
		   (not (handempty))
		   (holding ?x)))

  (:action put-down
	     :parameters (?x - block)
	     :precondition (holding ?x)
	     :effect
	     (and (not (holding ?x))
		   (clear ?x)
		   (handempty)
		   (ontable ?x)))
  (:action stack
	     :parameters (?x - block ?y - block)
	     :precondition (and (holding ?x) (clear ?y))
	     :effect
	     (and (not (holding ?x))
		   (not (clear ?y))
		   (clear ?x)
		   (handempty)
		   (on ?x ?y)))
  (:action unstack
	     :parameters (?x - block ?y - block)
	     :precondition (and (on ?x ?y) (clear ?x) (handempty))
	     :effect
	     (and (holding ?x)
		   (clear ?y)
		   (not (clear ?x))
		   (not (handempty))
		   (not (on ?x ?y)))))
"""
    domain_file = tempfile.NamedTemporaryFile(delete=False,
                                              suffix=".pddl").name
    with open(domain_file, "w", encoding="utf-8") as f:
        f.write(domain_str)
    return domain_file


@pytest.fixture(scope="module", name="problem_file")
def _create_problem_file():
    problem_str = """(define (problem blocks)
    (:domain blocks)
    (:objects
        d - block
        b - block
        a - block
        c - block
    )
    (:init
        (clear c)
        (clear b)
        (clear d)
        (ontable c)
        (ontable a)
        (ontable d)
        (on b a)
        (handempty)
    )
    (:goal (and (holding a)))
)
"""
    problem_file = tempfile.NamedTemporaryFile(delete=False,
                                               suffix=".pddl").name
    with open(problem_file, "w", encoding="utf-8") as f:
        f.write(problem_str)
    return problem_file


@pytest.fixture(scope="module", name="impossible_problem_file")
def _create_impossible_problem_file():
    problem_str = """(define (problem blocks)
    (:domain blocks)
    (:objects
        d - block
        b - block
        a - block
        c - block
    )
    (:init
        (clear c)
        (clear b)
        (clear d)
        (ontable c)
        (ontable d)
        (handempty)
    )
    (:goal (and (holding a)))
)
"""
    problem_file = tempfile.NamedTemporaryFile(delete=False,
                                               suffix=".pddl").name
    with open(problem_file, "w", encoding="utf-8") as f:
        f.write(problem_str)
    return problem_file


@pytest.fixture(scope="module", name="valid_plans")
def _create_valid_plans():
    # Optimal valid plan.
    valid_plan1 = ["(unstack b a)", "(stack b c)", "(pick-up a)"]
    # Not optimal, but still valid.
    valid_plan2 = [
        "(unstack b a)", "(stack b c)", "(unstack b c)", "(stack b c)",
        "(pick-up a)"
    ]
    valid_plans = [valid_plan1, valid_plan2]
    return valid_plans


@pytest.fixture(scope="module", name="invalid_plans")
def _create_invalid_plans():
    # Invalid because the second action's preconditions do not hold.
    invalid_plan1 = [
        "(unstack b a)", "(unstack b a)", "(stack b c)", "(pick-up a)"
    ]
    # Invalid because there's a garbage entry.
    invalid_plan2 = ["garbage", "(unstack b a)", "(stack b c)", "(pick-up a)"]
    # Invalid because the plan stops short.
    invalid_plan3 = [
        "(unstack b a)",
        "(stack b c)",
    ]
    invalid_plans = [invalid_plan1, invalid_plan2, invalid_plan3]
    return invalid_plans


def test_validate_plan(domain_file, problem_file, valid_plans, invalid_plans):
    """Tests for validate_plan()."""
    task = Task(domain_file, problem_file)
    for valid_plan in valid_plans:
        assert utils.validate_plan(task, valid_plan)
    for invalid_plan in invalid_plans:
        assert not utils.validate_plan(task, invalid_plan)


def test_get_pyperplan_benchmark_task():
    """Tests for get_pyperplan_benchmark_task()."""
    # Standard domain format.
    task = utils.get_pyperplan_benchmark_task("blocks", 1)
    assert os.path.exists(task.domain_file)
    assert os.path.exists(task.problem_file)
    # Per-problem domain files.
    task = utils.get_pyperplan_benchmark_task("airport", 1)
    assert os.path.exists(task.domain_file)
    assert os.path.exists(task.problem_file)
    # Domain doesn't exist.
    with pytest.raises(FileNotFoundError) as e:
        utils.get_pyperplan_benchmark_task("not a real domain", 1)
    assert "Domain not found" in str(e)
    # Problem doesn't exist.
    with pytest.raises(FileNotFoundError) as e:
        utils.get_pyperplan_benchmark_task("blocks", 100)
    assert "Problem not found" in str(e)


def test_get_custom_task():
    """Tests get_custom_task()"""
    # Dressed:
    task = utils.get_custom_task("dressed", 1)
    assert os.path.exists(task.domain_file)
    assert os.path.exists(task.problem_file)
    # Domain doesn't exist:
    with pytest.raises(FileNotFoundError) as f:
        task = utils.get_custom_task("nonsense", 1)
    assert "Domain not found" in str(f)
    # Problem doesn't exist:
    with pytest.raises(FileNotFoundError) as f:
        task = utils.get_custom_task("dressed", 100)
    assert "Task not found" in str(f)


def test_minify_pddl_problem():
    """Tests minify_pddl_problem().

    Note: I separately ran prep_problem() and then planned with the
    new problem. Pyperplan still planned correctly with it.
    """
    utils.reset_flags({"llm_prompt_flatten_pddl": False})
    # Testing big example #1:
    task01_path = utils.get_custom_task('dressed', 1).problem_file
    with open(task01_path, 'r', encoding='utf-8') as f:
        task01 = f.read()
    answer01 = """(define (problem dressed)
(:domain dressed)
(:objects person1 person2 person3 person4 - person
dress1 - dress
sweatpants1 sweatpants2 - sweatpants
sweatshirt1 sweatshirt2 - sweatshirt
nice-pants1 - nice-pants
collared-shirt1 - collared-shirt
suit-jacket1 - suit-jacket)
(:init (wearing-nothing-formal person1)
(wearing-nothing-casual person1)
(wearing-nothing-formal person2)
(wearing-nothing-casual person2)
(wearing-nothing-formal person3)
(wearing-nothing-casual person3)
(wearing-nothing-formal person4)
(wearing-nothing-casual person4)
(in-closet dress1)
(in-closet sweatpants1)
(in-closet sweatpants2)
(in-closet sweatshirt1)
(in-closet sweatshirt2)
(in-closet nice-pants1)
(in-closet collared-shirt1)
(in-closet suit-jacket1))
(:goal (and (attending-casual-event person3)
(attending-formal-event person1)
(attending-casual-event person4)
(attending-formal-event person2))))"""
    assert utils.minify_pddl_problem(task01) == answer01
    #Testing big example #2(same as above but with noise added):
    initial = """(define (problem dressed)


(:domain dressed)
(:objects person1 person2 person3 person4 - person
dress1 - dress
    sweatpants1 sweatpants2 - sweatpants
sweatshirt1 sweatshirt2 - sweatshirt   
        nice-pants1 - nice-pants
collared-shirt1 - collared-shirt   
    suit-jacket1 - suit-jacket)
(:init (wearing-nothing-formal person1)
(wearing-nothing-casual person1)


(wearing-nothing-formal person2)
(wearing-nothing-casual person2)
  (wearing-nothing-formal person3)
(wearing-nothing-casual person3)

(wearing-nothing-formal person4)
(wearing-nothing-casual person4)
(in-closet dress1)
(in-closet sweatpants1)
(in-closet sweatpants2)
  (in-closet sweatshirt1)   
  (in-closet sweatshirt2)
  (in-closet nice-pants1)
(in-closet collared-shirt1)
(in-closet suit-jacket1))

(:goal (and (attending-casual-event person3)
(attending-formal-event person1)
(attending-casual-event person4)  
(attending-formal-event person2) )  )   )"""
    assert utils.minify_pddl_problem(initial) == answer01
    # Testing many blank lines:
    example01 = """(in-closet sweatshirt2)


(in-closet nice-pants1)"""
    assert utils.minify_pddl_problem(example01) == """(in-closet sweatshirt2)
(in-closet nice-pants1)"""
    # Testing odd spaces between right parentheses and multiple on a line:
    example02 = """(:goal (and (attending-casual-event person3)
)   ) """
    assert utils.minify_pddl_problem(
        example02) == """(:goal (and (attending-casual-event person3)))"""
    # Testing both:
    example03 = """
    (  (in-closet sweatpants1) )
    """
    assert utils.minify_pddl_problem(
        example03) == """((in-closet sweatpants1))"""
    q_a_example_no_flatten = """Q:
(:objects
red blue - color
)
(:init
(here red)
)
(:goal
(and (here red) (here blue))
)
A:
(make blue)
(end)"""
    assert utils.minify_pddl_problem(q_a_example_no_flatten) == """Q:
(:objects
red blue - color)
(:init
(here red))
(:goal
(and (here red)(here blue)))
A:
(make blue)
(end)"""
    # --------- From flatten: ---------
    utils.reset_flags({"llm_prompt_flatten_pddl": True})
    flatten_example01 = """(:init
(pred a b)
(pred a)
(pred  c)"""
    assert utils.minify_pddl_problem(
        flatten_example01) == """(:init (pred a b)(pred a)(pred  c)"""
    flatten_example02 = """(:objects
thing1 thing2 - thing
d d d - d
purple - color"""
    assert utils.minify_pddl_problem(
        flatten_example02
    ) == """(:objects thing1 thing2 - thing d d d - d purple - color"""
    flatten_example03 = """(:goal
(no touch)
(no touch)"""
    assert utils.minify_pddl_problem(
        flatten_example03) == """(:goal (no touch)(no touch)"""
    flatten_big_example = """(define (problem dressed)
(:domain dressed)
(:objects
a b c - letters
one two - numbers)
(:init
(yes a)
(yes b))
(:goal (and
(yes a)
(yes b)
(yes c))))"""
    assert utils.minify_pddl_problem(
        flatten_big_example) == """(define (problem dressed)(:domain dressed)\
(:objects a b c - letters one two - numbers)(:init (yes a)(yes b))\
(:goal (and (yes a)(yes b)(yes c))))"""
    q_a_example = """Q:
(:objects
red blue - color
)
(:init
(here red)
)
(:goal
(and (here red) (here blue))
)
A:
(make blue)
(end)"""
    assert utils.minify_pddl_problem(q_a_example) == """Q:
(:objects red blue - color)(:init (here red))(:goal (and (here red)(here blue)))
A:
(make blue)(end)"""


def test_embed_training_tasks():
    utils.reset_flags({
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_prompt_flatten_pddl": True
    })
    tasks = [utils.get_custom_task('dressed', i) for i in range(1, 5)]
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    for j, emb in enumerate(utils.embed_training_tasks(tasks)):
        assert np.all(
            emb == utils.embed_task(utils.get_custom_task('dressed', j +
                                                          1), embedding_model))


def test_embed_task():
    """Tests for embed_task()."""
    utils.reset_flags({
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_prompt_flatten_pddl": True
    })
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    task01 = utils.get_custom_task('dressed', 1)
    embedding1 = utils.embed_task(task01, embedding_model)
    with open(task01.problem_file, 'r', encoding='utf-8') as f:
        task_string = f.read()
    task_string = utils.minify_pddl_problem(task_string)
    embedding2 = embedding_model.encode(task_string)
    assert np.all(embedding1 == embedding2)


def test_make_embeddings_mapping():
    """Tests make_embeddings_mapping()."""
    embeddings = [[0.5], [0.1], [0.2]]
    tasks = [utils.get_custom_task('dressed', i) for i in range(1, 4)]
    dataset = [Datum(task, ['insert plan here']) for task in tasks]
    mapping = utils.make_embeddings_mapping(embeddings, dataset)
    assert len(mapping) == 3
    assert mapping[0]['embedding'] == [0.5]
    assert mapping[1]['embedding'] == [0.1]
    assert mapping[0]['datum'].solution == ['insert plan here']


def test_get_closest():
    """Tests for get_closest()."""
    utils.reset_flags({
        "llm_prompt_flatten_pddl": True,
        "embedding_model_name": "paraphrase-MiniLM-L6-v2"
    })
    dressed01 = utils.get_custom_task('dressed', 1)
    tasks = [utils.get_custom_task('dressed', i) for i in range(2, 5)]
    blocks01 = utils.get_pyperplan_benchmark_task('blocks', 1)
    blocks02 = utils.get_pyperplan_benchmark_task('blocks', 2)
    depot01 = utils.get_pyperplan_benchmark_task('depot', 1)
    tasks.append(blocks01)
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    embeddings = [utils.embed_task(task, embedding_model) for task in tasks]
    dataset = [Datum(task, ['insert plan here']) for task in tasks]
    embeddings_mapping = utils.make_embeddings_mapping(embeddings, dataset)
    # checking correct output size
    most_similar = utils.get_closest(dressed01, embeddings_mapping, 1)
    assert len(most_similar) == 1
    most_similar2 = utils.get_closest(dressed01, embeddings_mapping, 3)
    assert len(most_similar2) == 3
    most_similar3 = utils.get_closest(dressed01, embeddings_mapping, 4)
    assert len(most_similar3) == 4
    # checking that blocks is the least likely:
    assert most_similar3[0].task == utils.get_pyperplan_benchmark_task(
        'blocks', 1)
    dif_tasks = [dressed01, blocks01, depot01]
    dif_embeddings = [
        utils.embed_task(task, embedding_model) for task in dif_tasks
    ]
    dif_dataset = [Datum(task, ['insert plan here']) for task in dif_tasks]
    dif_emb_map = utils.make_embeddings_mapping(dif_embeddings, dif_dataset)
    most_sim1 = utils.get_closest(blocks02, dif_emb_map, 1)
    # checking that blocks is the most likely of the 3:
    assert most_sim1[0].task == utils.get_pyperplan_benchmark_task('blocks', 1)
    # big example selecting the correct tasks each time:
    dressed = [utils.get_custom_task('dressed', i) for i in range(2, 5)]
    depot = [
        utils.get_pyperplan_benchmark_task('depot', i) for i in range(2, 5)
    ]
    blocks = [
        utils.get_pyperplan_benchmark_task('blocks', i) for i in range(2, 5)
    ]
    big_tasks = dressed + depot + blocks
    big_embeddings = [
        utils.embed_task(task, embedding_model) for task in big_tasks
    ]
    big_dataset = [Datum(task, ['insert plan here']) for task in big_tasks]
    big_emb_map = utils.make_embeddings_mapping(big_embeddings, big_dataset)
    # comparing to dressed:
    most_similar_dressed = utils.get_closest(dressed01, big_emb_map, 9)
    assert len(most_similar_dressed) == len(big_tasks)
    for datum in most_similar_dressed[-3:]:
        assert datum.task in dressed

    # comparing to blocks:
    most_similar_blocks = utils.get_closest(blocks01, big_emb_map, 9)
    for datum in most_similar_blocks[-3:]:
        assert datum.task in blocks

    # comparing to depot:
    most_similar_depot = utils.get_closest(depot01, big_emb_map, 9)
    for datum in most_similar_depot[-3:]:
        assert datum.task in depot

    # proving identical is considered best:
    most_sim = utils.get_closest(blocks02, big_emb_map, 9)[-1]
    assert most_sim.task == utils.get_pyperplan_benchmark_task('blocks', 2)

    #make test here that shows it selects a more similar task in the same domain.


def test_get_cosine_sim():
    """Tests get_cosine_sim()."""
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    embedding1 = embedding_model.encode('hello')
    embedding2 = embedding_model.encode('hello')
    cos_sim1 = utils.get_cosine_sim(embedding1, embedding2)
    assert cos_sim1 == 1
    embedding3 = embedding_model.encode('hell')
    cos_sim2 = utils.get_cosine_sim(embedding1, embedding3)
    assert cos_sim2 != 1
    embedding4 = embedding_model.encode('my name is')
    embedding5 = embedding_model.encode('my dog is here')
    cos_sim3 = utils.get_cosine_sim(embedding4, embedding5)
    assert cos_sim3 == cos_sim(embedding4, embedding5).item()


def test_run_planning(domain_file, problem_file, impossible_problem_file):
    """Tests for run_planning().

    Fast downward is not tested because it's not easy to install on the
    github checks server.
    """
    utils.reset_flags({"planning_timeout": 100})
    # Test planning successfully.
    task = Task(domain_file, problem_file)
    plan, metrics = utils.run_planning(task)
    assert metrics["nodes_created"] > metrics["nodes_expanded"]
    assert plan is not None
    assert utils.validate_plan(task, plan)
    # Test planning in an impossible problem.
    impossible_task = Task(domain_file, impossible_problem_file)
    plan, metrics = utils.run_planning(impossible_task)
    assert metrics["nodes_created"] == metrics["nodes_expanded"] == 1
    assert plan is None
    # Test planning in a pyperplan benchmark problem.
    task = utils.get_pyperplan_benchmark_task("blocks", 1)
    plan, metrics = utils.run_planning(task)
    assert metrics["nodes_created"] > metrics["nodes_expanded"]
    assert plan is not None
    assert utils.validate_plan(task, plan)
    # Test planning with an invalid planner.
    with pytest.raises(NotImplementedError) as e:
        utils.run_planning(task, planner="not a real planner")
    assert "Unrecognized planner" in str(e)


if __name__ == "__main__":
    test_embed_training_tasks()
    test_embed_task()
    test_get_cosine_sim()
    test_make_embeddings_mapping()
    test_get_closest()
