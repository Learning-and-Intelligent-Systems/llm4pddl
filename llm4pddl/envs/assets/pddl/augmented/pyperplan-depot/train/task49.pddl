(define (problem depotprob1935)
  (:domain depot)
  (:objects
    crate1 - object
    crate2 - object
    crate5 - object
    depot0 - object
    distributor0 - object
    distributor1 - object
    hoist0 - object
    hoist2 - object
    pallet0 - object
    pallet2 - object
    truck1 - object
  )
  (:init
    (surface pallet0)
    (clear crate1)
    (surface pallet2)
    (at pallet2 distributor1)
    (clear crate5)
    (truck truck1)
    (at truck1 distributor0)
    (hoist hoist0)
    (at hoist0 depot0)
    (available hoist0)
    (hoist hoist2)
    (at hoist2 distributor1)
    (available hoist2)
    (crate crate1)
    (at crate1 depot0)
    (on crate1 pallet0)
    (crate crate2)
    (surface crate2)
    (at crate2 distributor1)
    (on crate2 pallet2)
    (crate crate5)
    (at crate5 distributor1)
    (on crate5 crate2)
    (place depot0)
    (place distributor0)
    (place distributor1)
  )
  (:goal (and (on crate1 pallet2)))
)
