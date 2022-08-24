(define (problem depotprob1234)
  (:domain depot)
  (:objects
    crate0 - object
    crate1 - object
    crate4 - object
    depot0 - object
    distributor0 - object
    distributor1 - object
    hoist1 - object
    hoist2 - object
    pallet5 - object
    truck1 - object
  )
  (:init
    (clear crate4)
    (surface pallet5)
    (at pallet5 distributor1)
    (clear crate1)
    (truck truck1)
    (at truck1 depot0)
    (hoist hoist1)
    (at hoist1 distributor0)
    (available hoist1)
    (hoist hoist2)
    (at hoist2 distributor1)
    (available hoist2)
    (surface crate0)
    (crate crate1)
    (at crate1 distributor1)
    (on crate1 pallet5)
    (crate crate4)
    (surface crate4)
    (at crate4 distributor0)
    (on crate4 crate0)
    (place depot0)
    (place distributor0)
    (place distributor1)
  )
  (:goal (and (on crate1 crate4) (on crate4 pallet5)))
)
