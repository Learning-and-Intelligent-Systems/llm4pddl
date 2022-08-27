(define (problem depotprob1818)
  (:domain depot)
  (:objects
    crate0 - object
    crate1 - object
    depot0 - object
    distributor0 - object
    hoist0 - object
    hoist1 - object
    pallet0 - object
    pallet1 - object
    truck1 - object
  )
  (:init
    (surface pallet0)
    (clear crate1)
    (surface pallet1)
    (at pallet1 distributor0)
    (clear crate0)
    (truck truck1)
    (at truck1 depot0)
    (hoist hoist0)
    (at hoist0 depot0)
    (available hoist0)
    (hoist hoist1)
    (at hoist1 distributor0)
    (available hoist1)
    (crate crate0)
    (at crate0 distributor0)
    (on crate0 pallet1)
    (crate crate1)
    (at crate1 depot0)
    (on crate1 pallet0)
    (place depot0)
    (place distributor0)
  )
  (:goal (and (on crate1 pallet1)))
)
