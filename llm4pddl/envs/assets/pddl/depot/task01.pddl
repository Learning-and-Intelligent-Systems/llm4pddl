(define (problem depotcustom1) (:domain Depot)
(:objects
	distributor0 truck0 pallet0 pallet1 crate0 hoist0)
(:init
	(truck truck0)

	(crate crate0)

	(place distributor0)

	(pallet pallet0)
	(pallet pallet1)
	
	(hoist hoist0)

	(surface crate0)
	(surface pallet0)
	(surface pallet1)

	(clear crate0)
	(clear pallet1)

	(on crate0 pallet0)

	(available hoist0)

	(at truck0 distributor0)
	(at pallet0 distributor0)
	(at pallet1 distributor0)
	(at hoist0 distributor0)
	(at crate0 distributor0)
)

(:goal (and
		(on crate0 pallet1)
	)
))
