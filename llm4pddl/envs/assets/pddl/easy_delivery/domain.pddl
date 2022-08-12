(define (domain easy_delivery)
  (:requirements :typing)
  (:types loc paper)

  (:predicates
    (at ?x0 - loc)
    (carrying ?x0 - paper)
    (ishomebase ?x0 - loc)
    (safe ?x0 - loc)
    (satisfied ?x0 - loc)
    (unpacked ?x0 - paper)
    (wantspaper ?x0 - loc)
  )

  (:action deliver
    :parameters (?paper - paper ?loc - loc)
    :precondition (and (at ?loc)
        (carrying ?paper))
    :effect (and (satisfied ?loc)
        (not (carrying ?paper))
        (not (wantspaper ?loc)))
  )

  (:action move
    :parameters (?from - loc ?to - loc)
    :precondition (and (at ?from)
        (safe ?from))
    :effect (and (at ?to)
        (not (at ?from)))
  )

  (:action pick-up
    :parameters (?paper - paper ?loc - loc)
    :precondition (and (at ?loc)
        (ishomebase ?loc)
        (unpacked ?paper))
    :effect (and (carrying ?paper)
        (not (unpacked ?paper)))
  )
)