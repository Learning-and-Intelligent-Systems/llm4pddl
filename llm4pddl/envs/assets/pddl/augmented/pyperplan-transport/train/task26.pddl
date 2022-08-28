(define (problem transport-city-sequential-6nodes-1000size-2degree-100mindistance-2trucks-3packages-2008seed)
  (:domain transport)
  (:objects
    capacity-3 - capacity-number
    capacity-4 - capacity-number
    city-loc-1 - location
    city-loc-2 - location
    city-loc-3 - location
    city-loc-4 - location
    city-loc-5 - location
    city-loc-6 - location
    package-3 - package
    truck-1 - vehicle
  )
  (:init
    (capacity-predecessor capacity-3 capacity-4)
    (road city-loc-3 city-loc-1)
    (road city-loc-1 city-loc-3)
    (road city-loc-5 city-loc-1)
    (road city-loc-1 city-loc-5)
    (road city-loc-5 city-loc-4)
    (road city-loc-4 city-loc-5)
    (road city-loc-2 city-loc-6)
    (road city-loc-6 city-loc-3)
    (road city-loc-3 city-loc-6)
    (at package-3 city-loc-4)
    (at truck-1 city-loc-2)
    (capacity truck-1 capacity-4)
  )
  (:goal (and (at package-3 city-loc-6)))
)
