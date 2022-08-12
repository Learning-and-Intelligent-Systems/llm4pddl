(define (domain easy_spanner)
  (:requirements :typing)
  (:types
      location locatable - object
      man nut spanner - locatable
  )

  (:predicates
    (at ?x0 - locatable ?x1 - location)
    (carrying ?x0 - man ?x1 - spanner)
    (link ?x0 - location ?x1 - location)
    (loose ?x0 - nut)
    (tightened ?x0 - nut)
    (useable ?x0 - spanner)
  )

  (:action pickup_spanner
    :parameters (?l - location ?s - spanner ?m - man)
    :precondition (and (at ?m ?l)
        (at ?s ?l))
    :effect (and (carrying ?m ?s)
        (not (at ?s ?l)))
  )

  (:action tighten_nut
    :parameters (?l - location ?s - spanner ?m - man ?n - nut)
    :precondition (and (at ?m ?l)
        (at ?n ?l)
        (carrying ?m ?s)
        (loose ?n)
        (useable ?s))
    :effect (and (tightened ?n)
        (not (loose ?n))
        (not (useable ?s)))
  )

  (:action walk
    :parameters (?start - location ?end - location ?m - man)
    :precondition (and (at ?m ?start)
        (link ?start ?end))
    :effect (and (at ?m ?end)
        (not (at ?m ?start)))
  )
)