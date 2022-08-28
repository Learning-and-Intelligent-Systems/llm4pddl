(define (problem depotcustom5) (:domain Depot)
(:objects
	distributor0 depot0 truck0 truck1 pallet0 pallet1 pallet2 crate0 crate1 hoist0 hoist1)
(:init
	(truck truck0)
	(truck truck1)

	(crate crate0)
	(crate crate1)

	(place distributor0)
	(place depot0)

	(pallet pallet0)
	(pallet pallet1)
	(pallet pallet2)
	
	(hoist hoist0)
	(hoist hoist1)

	(surface crate0)
	(surface crate1)
	(surface pallet0)
	(surface pallet1)
	(surface pallet2)

	(clear crate0)
	(clear crate1)
	(clear pallet2)

	(on crate0 pallet0)
	(on crate1 pallet1)

	(available hoist0)
	(available hoist1)

	(at truck0 distributor0)
	(at truck1 depot0)
	(at pallet0 distributor0)
	(at pallet1 depot0)
	(at pallet2 distributor0)
	(at hoist0 distributor0)
	(at hoist1 depot0)
	(at crate0 distributor0)
	(at crate1 depot0)
)

(:goal (and
		(on crate0 pallet1)
		(on crate1 pallet2)
	)
))
