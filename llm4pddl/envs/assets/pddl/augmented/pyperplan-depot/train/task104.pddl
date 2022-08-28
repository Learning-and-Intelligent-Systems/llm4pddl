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
    pallet3 - object
    pallet4 - object
    pallet5 - object
    truck1 - object
  )
  (:init
    (surface pallet3)
    (at pallet3 distributor0)
    (clear pallet3)
    (surface pallet4)
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
    (crate crate0)
    (surface crate0)
    (at crate0 distributor0)
    (on crate0 pallet4)
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
  (:goal (and (on crate0 pallet3) (on crate1 crate4) (on crate4 pallet5)))
)
