(define (problem depotprob1234)
  (:domain depot)
  (:objects
    crate1 - object
    crate2 - object
    crate3 - object
    crate4 - object
    depot0 - object
    distributor0 - object
    distributor1 - object
    hoist1 - object
    hoist2 - object
    pallet1 - object
    pallet5 - object
    truck1 - object
  )
  (:init
    (surface pallet1)
    (at pallet1 distributor0)
    (clear pallet1)
    (clear crate3)
    (clear crate4)
    (surface pallet5)
    (clear crate1)
    (truck truck1)
    (at truck1 depot0)
    (hoist hoist1)
    (at hoist1 distributor0)
    (available hoist1)
    (hoist hoist2)
    (at hoist2 distributor1)
    (available hoist2)
    (crate crate1)
    (at crate1 distributor1)
    (on crate1 pallet5)
    (surface crate2)
    (crate crate3)
    (at crate3 distributor1)
    (on crate3 crate2)
    (surface crate4)
    (at crate4 distributor0)
    (place depot0)
    (place distributor0)
    (place distributor1)
  )
  (:goal (and (on crate1 crate4) (on crate3 pallet1)))
)
