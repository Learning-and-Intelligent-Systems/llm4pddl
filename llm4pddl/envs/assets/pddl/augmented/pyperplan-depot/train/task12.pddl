(define (problem depotprob1818)
  (:domain depot)
  (:objects
    crate0 - object
    depot0 - object
    distributor0 - object
    distributor1 - object
    hoist1 - object
    hoist2 - object
    pallet1 - object
    pallet2 - object
    truck1 - object
  )
  (:init
    (surface pallet1)
    (clear crate0)
    (surface pallet2)
    (at pallet2 distributor1)
    (clear pallet2)
    (truck truck1)
    (at truck1 depot0)
    (hoist hoist1)
    (at hoist1 distributor0)
    (available hoist1)
    (hoist hoist2)
    (at hoist2 distributor1)
    (available hoist2)
    (crate crate0)
    (at crate0 distributor0)
    (on crate0 pallet1)
    (place depot0)
    (place distributor0)
    (place distributor1)
  )
  (:goal (and (on crate0 pallet2)))
)
