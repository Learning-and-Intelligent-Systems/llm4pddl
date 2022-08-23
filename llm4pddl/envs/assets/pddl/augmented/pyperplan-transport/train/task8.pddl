(define (problem transport-two-cities-sequential-2nodes-1000size-2degree-100mindistance-2trucks-2packages-2008seed)
  (:domain transport)
  (:objects
    capacity-2 - capacity-number
    capacity-3 - capacity-number
    city-1-loc-1 - location
    city-1-loc-2 - location
    city-2-loc-1 - location
    city-2-loc-2 - location
    package-1 - package
    package-2 - package
    truck-2 - vehicle
  )
  (:init
    (capacity-predecessor capacity-2 capacity-3)
    (road city-1-loc-2 city-1-loc-1)
    (road city-1-loc-1 city-1-loc-2)
    (road city-2-loc-2 city-2-loc-1)
    (road city-1-loc-2 city-2-loc-2)
    (road city-2-loc-2 city-1-loc-2)
    (at package-1 city-1-loc-1)
    (at package-2 city-1-loc-1)
    (at truck-2 city-2-loc-2)
    (capacity truck-2 capacity-3)
  )
  (:goal (and (at package-1 city-2-loc-1) (at package-2 city-2-loc-2)))
)
