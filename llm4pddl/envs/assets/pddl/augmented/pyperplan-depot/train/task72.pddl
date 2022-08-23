(define (problem depotprob1935)
  (:domain depot)
  (:objects
    crate0 - object
    crate1 - object
    crate3 - object
    crate4 - object
    depot0 - object
    distributor0 - object
    hoist0 - object
    hoist1 - object
    pallet1 - object
    truck1 - object
  )
  (:init
    (clear crate1)
    (surface pallet1)
    (at pallet1 distributor0)
    (clear crate4)
    (truck truck1)
    (at truck1 distributor0)
    (hoist hoist0)
    (at hoist0 depot0)
    (available hoist0)
    (hoist hoist1)
    (at hoist1 distributor0)
    (available hoist1)
    (crate crate0)
    (surface crate0)
    (at crate0 distributor0)
    (on crate0 pallet1)
    (surface crate1)
    (at crate1 depot0)
    (crate crate3)
    (surface crate3)
    (at crate3 distributor0)
    (on crate3 crate0)
    (crate crate4)
    (at crate4 distributor0)
    (on crate4 crate3)
    (place depot0)
    (place distributor0)
  )
  (:goal (and (on crate0 crate1) (on crate4 pallet1)))
)
