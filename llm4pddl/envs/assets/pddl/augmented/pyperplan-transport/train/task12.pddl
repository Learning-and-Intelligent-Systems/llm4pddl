(define (problem transport-city-sequential-3nodes-1000size-2degree-100mindistance-2trucks-2packages-2008seed)
  (:domain transport)
  (:objects
    capacity-3 - capacity-number
    capacity-4 - capacity-number
    city-loc-2 - location
    city-loc-3 - location
    package-1 - package
    truck-1 - vehicle
  )
  (:init
    (capacity-predecessor capacity-3 capacity-4)
    (road city-loc-3 city-loc-2)
    (at package-1 city-loc-3)
    (at truck-1 city-loc-3)
    (capacity truck-1 capacity-4)
  )
  (:goal (and (at package-1 city-loc-2)))
)
