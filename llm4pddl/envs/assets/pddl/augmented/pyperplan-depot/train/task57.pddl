(define (problem depotprob1935)
  (:domain depot)
  (:objects
    crate0 - object
    crate3 - object
    crate4 - object
    distributor0 - object
    hoist1 - object
    pallet1 - object
    truck1 - object
  )
  (:init
    (surface pallet1)
    (at pallet1 distributor0)
    (clear crate4)
    (truck truck1)
    (at truck1 distributor0)
    (hoist hoist1)
    (at hoist1 distributor0)
    (available hoist1)
    (crate crate0)
    (surface crate0)
    (at crate0 distributor0)
    (on crate0 pallet1)
    (crate crate3)
    (surface crate3)
    (at crate3 distributor0)
    (on crate3 crate0)
    (crate crate4)
    (at crate4 distributor0)
    (on crate4 crate3)
    (place distributor0)
  )
  (:goal (and (on crate4 pallet1)))
)
