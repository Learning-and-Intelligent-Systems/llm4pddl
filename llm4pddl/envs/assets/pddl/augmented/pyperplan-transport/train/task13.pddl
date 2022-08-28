(define (problem transport-three-cities-sequential-1nodes-1000size-0degree-100mindistance-2trucks-2packages-2008seed)
  (:domain transport)
  (:objects
    capacity-3 - capacity-number
    capacity-4 - capacity-number
    city-2-loc-1 - location
    city-3-loc-1 - location
    package-2 - package
    truck-2 - vehicle
  )
  (:init
    (capacity-predecessor capacity-3 capacity-4)
    (road city-2-loc-1 city-3-loc-1)
    (road city-3-loc-1 city-2-loc-1)
    (at package-2 city-3-loc-1)
    (at truck-2 city-2-loc-1)
    (capacity truck-2 capacity-4)
  )
  (:goal (and (at package-2 city-2-loc-1)))
)
