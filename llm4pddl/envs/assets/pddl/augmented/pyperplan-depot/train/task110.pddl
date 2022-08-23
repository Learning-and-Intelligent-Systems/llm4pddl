(define (problem depotprob1234)
  (:domain depot)
  (:objects
    crate0 - object
    crate4 - object
    depot0 - object
    distributor0 - object
    distributor1 - object
    hoist1 - object
    pallet3 - object
    pallet4 - object
    truck1 - object
  )
  (:init
    (surface pallet3)
    (at pallet3 distributor0)
    (clear pallet3)
    (surface pallet4)
    (clear crate4)
    (truck truck1)
    (at truck1 depot0)
    (hoist hoist1)
    (at hoist1 distributor0)
    (available hoist1)
    (crate crate0)
    (surface crate0)
    (at crate0 distributor0)
    (on crate0 pallet4)
    (crate crate4)
    (at crate4 distributor0)
    (on crate4 crate0)
    (place depot0)
    (place distributor0)
    (place distributor1)
  )
  (:goal (and (on crate0 pallet3)))
)
