(define (problem depotprob1935)
  (:domain depot)
  (:objects
    crate0 - object
    crate1 - object
    crate2 - object
    crate3 - object
    crate4 - object
    crate5 - object
    depot0 - object
    distributor0 - object
    distributor1 - object
    hoist0 - object
    hoist1 - object
    hoist2 - object
    pallet0 - object
    pallet1 - object
    pallet2 - object
    truck1 - object
  )
  (:init
    (surface pallet0)
    (at pallet0 depot0)
    (clear crate1)
    (surface pallet1)
    (at pallet1 distributor0)
    (clear crate4)
    (surface pallet2)
    (at pallet2 distributor1)
    (clear crate5)
    (truck truck1)
    (at truck1 distributor0)
    (hoist hoist0)
    (at hoist0 depot0)
    (available hoist0)
    (hoist hoist1)
    (at hoist1 distributor0)
    (available hoist1)
    (hoist hoist2)
    (at hoist2 distributor1)
    (available hoist2)
    (crate crate0)
    (surface crate0)
    (at crate0 distributor0)
    (on crate0 pallet1)
    (crate crate1)
    (at crate1 depot0)
    (on crate1 pallet0)
    (crate crate2)
    (surface crate2)
    (at crate2 distributor1)
    (on crate2 pallet2)
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
    (place depot0)
    (place distributor0)
    (place distributor1)
  )
  (:goal (and (on crate1 pallet2) (on crate3 crate2) (on crate4 pallet1)))
)
