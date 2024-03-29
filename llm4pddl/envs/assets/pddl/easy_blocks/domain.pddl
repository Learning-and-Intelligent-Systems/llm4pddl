(define (domain easy_blocks)
  (:requirements :typing)
  (:types block)

  (:predicates
    (clear ?x0 - block)
    (handempty)
    (holding ?x0 - block)
    (on ?x0 - block ?x1 - block)
    (ontable ?x0 - block)
  )

  (:action pick-up
    :parameters (?x - block)
    :precondition (and (clear ?x)
        (handempty)
        (ontable ?x))
    :effect (and (holding ?x)
        (not (clear ?x))
        (not (handempty))
        (not (ontable ?x)))
  )

  (:action put-down
    :parameters (?x - block)
    :precondition (and (holding ?x))
    :effect (and (clear ?x)
        (handempty)
        (ontable ?x)
        (not (holding ?x)))
  )

  (:action stack
    :parameters (?x - block ?y - block)
    :precondition (and (clear ?y)
        (holding ?x))
    :effect (and (clear ?x)
        (handempty)
        (on ?x ?y)
        (not (clear ?y))
        (not (holding ?x)))
  )

  (:action unstack
    :parameters (?x - block ?y - block)
    :precondition (and (clear ?x)
        (handempty)
        (on ?x ?y))
    :effect (and (clear ?y)
        (holding ?x)
        (not (clear ?x))
        (not (handempty))
        (not (on ?x ?y)))
  )
)