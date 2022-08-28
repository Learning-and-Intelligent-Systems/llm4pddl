(define (problem depotprob1935)
  (:domain depot)
  (:objects
    crate0 - object
    crate2 - object
    crate3 - object
    crate4 - object
    crate5 - object
    distributor0 - object
    distributor1 - object
    hoist1 - object
    hoist2 - object
    truck1 - object
  )
  (:init
    (clear crate4)
    (clear crate5)
    (truck truck1)
    (at truck1 distributor0)
    (hoist hoist1)
    (at hoist1 distributor0)
    (available hoist1)
    (hoist hoist2)
    (at hoist2 distributor1)
    (available hoist2)
    (surface crate0)
    (at crate0 distributor0)
    (surface crate2)
    (at crate2 distributor1)
    (crate crate3)
    (surface crate3)
    (at crate3 distributor0)
    (on crate3 crate0)
    (crate crate4)
    (at crate4 distributor0)
    (on crate4 crate3)
    (crate crate5)
    (at crate5 distributor1)
    (on crate5 crate2)
    (place distributor0)
    (place distributor1)
  )
  (:goal (and (on crate3 crate2) (on crate5 crate0)))
)
