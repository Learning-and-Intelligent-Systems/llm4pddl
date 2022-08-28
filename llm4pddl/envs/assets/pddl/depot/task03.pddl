(define (problem depotcustom4) (:domain Depot)
(:objects
	distributor0 depot0 truck0 truck1 pallet0 pallet1 crate0 hoist0 hoist1)
(:init
	(truck truck0)
	(truck truck1)

	(crate crate0)

	(place distributor0)
	(place depot0)

	(pallet pallet0)
	(pallet pallet1)
	
	(hoist hoist0)
	(hoist hoist1)

	(surface crate0)
	(surface pallet0)
	(surface pallet1)

	(clear crate0)
	(clear pallet1)

	(on crate0 pallet0)

	(available hoist0)
	(available hoist1)

	(at truck0 distributor0)
	(at truck1 depot0)
	(at pallet0 distributor0)
	(at pallet1 depot0)
	(at hoist0 distributor0)
	(at hoist1 depot0)
	(at crate0 distributor0)
)

(:goal (and
		(on crate0 pallet1)
	)
))
