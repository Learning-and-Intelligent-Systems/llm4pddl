(define (problem transport-three-cities-sequential-2nodes-1000size-1degree-100mindistance-2trucks-3packages-2008seed)
  (:domain transport)
  (:objects
    capacity-3 - capacity-number
    capacity-4 - capacity-number
    city-1-loc-1 - location
    city-1-loc-2 - location
    city-2-loc-2 - location
    city-3-loc-1 - location
    city-3-loc-2 - location
    package-1 - package
    package-2 - package
    package-3 - package
    truck-2 - vehicle
  )
  (:init
    (capacity-predecessor capacity-3 capacity-4)
    (road city-1-loc-2 city-1-loc-1)
    (road city-3-loc-2 city-3-loc-1)
    (road city-3-loc-1 city-3-loc-2)
    (road city-1-loc-2 city-2-loc-2)
    (road city-2-loc-2 city-1-loc-2)
    (road city-1-loc-2 city-3-loc-1)
    (road city-3-loc-1 city-1-loc-2)
    (at package-1 city-2-loc-2)
    (at package-2 city-1-loc-2)
    (at package-3 city-3-loc-2)
    (at truck-2 city-2-loc-2)
    (capacity truck-2 capacity-4)
  )
  (:goal (and (at package-1 city-1-loc-2) (at package-2 city-2-loc-2) (at package-3 city-1-loc-1)))
)
