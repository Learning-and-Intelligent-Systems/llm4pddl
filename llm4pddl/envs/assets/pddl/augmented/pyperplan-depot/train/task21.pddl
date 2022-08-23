(define (problem depotprob7512)
  (:domain depot)
  (:objects
    crate0 - object
    crate1 - object
    crate2 - object
    depot0 - object
    distributor1 - object
    hoist0 - object
    hoist2 - object
    pallet0 - object
    pallet2 - object
    truck1 - object
  )
  (:init
    (surface pallet0)
    (clear crate0)
    (surface pallet2)
    (at pallet2 distributor1)
    (clear crate2)
    (truck truck1)
    (at truck1 depot0)
    (hoist hoist0)
    (at hoist0 depot0)
    (available hoist0)
    (hoist hoist2)
    (at hoist2 distributor1)
    (available hoist2)
    (crate crate0)
    (at crate0 depot0)
    (on crate0 pallet0)
    (crate crate1)
    (surface crate1)
    (at crate1 distributor1)
    (on crate1 pallet2)
    (crate crate2)
    (at crate2 distributor1)
    (on crate2 crate1)
    (place depot0)
    (place distributor1)
  )
  (:goal (and (on crate0 pallet2)))
)
