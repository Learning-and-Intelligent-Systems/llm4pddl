; Transport two-cities-sequential-6nodes-1000size-3degree-100mindistance-2trucks-4packages-2008seed

(define (problem transport-two-cities-sequential-6nodes-1000size-3degree-100mindistance-2trucks-4packages-2008seed)
 (:domain transport)
 (:objects
  city-1-loc-1 - location
  city-2-loc-1 - location
  city-1-loc-2 - location
  city-2-loc-2 - location
  city-1-loc-3 - location
  city-2-loc-3 - location
  city-1-loc-4 - location
  city-2-loc-4 - location
  city-1-loc-5 - location
  city-2-loc-5 - location
  city-1-loc-6 - location
  city-2-loc-6 - location
  truck-1 - vehicle
  truck-2 - vehicle
  package-1 - package
  package-2 - package
  package-3 - package
  package-4 - package
  capacity-0 - capacity-number
  capacity-1 - capacity-number
  capacity-2 - capacity-number
  capacity-3 - capacity-number
  capacity-4 - capacity-number
 )
 (:init
  
  (capacity-predecessor capacity-0 capacity-1)
  (capacity-predecessor capacity-1 capacity-2)
  (capacity-predecessor capacity-2 capacity-3)
  (capacity-predecessor capacity-3 capacity-4)
  ; 748,385 -> 890,543
  (road city-1-loc-3 city-1-loc-1)
  
  ; 890,543 -> 748,385
  (road city-1-loc-1 city-1-loc-3)
  
  ; 912,799 -> 890,543
  (road city-1-loc-4 city-1-loc-1)
  
  ; 890,543 -> 912,799
  (road city-1-loc-1 city-1-loc-4)
  
  ; 912,799 -> 748,385
  (road city-1-loc-4 city-1-loc-3)
  
  ; 748,385 -> 912,799
  (road city-1-loc-3 city-1-loc-4)
  
  ; 977,899 -> 890,543
  (road city-1-loc-5 city-1-loc-1)
  
  ; 890,543 -> 977,899
  (road city-1-loc-1 city-1-loc-5)
  
  ; 977,899 -> 912,799
  (road city-1-loc-5 city-1-loc-4)
  
  ; 912,799 -> 977,899
  (road city-1-loc-4 city-1-loc-5)
  
  ; 456,221 -> 384,50
  (road city-1-loc-6 city-1-loc-2)
  
  ; 384,50 -> 456,221
  (road city-1-loc-2 city-1-loc-6)
  
  ; 456,221 -> 748,385
  (road city-1-loc-6 city-1-loc-3)
  
  ; 748,385 -> 456,221
  (road city-1-loc-3 city-1-loc-6)
  
  ; 2564,783 -> 2742,542
  (road city-2-loc-2 city-2-loc-1)
  
  ; 2742,542 -> 2564,783
  (road city-2-loc-1 city-2-loc-2)
  
  ; 2273,425 -> 2564,783
  (road city-2-loc-3 city-2-loc-2)
  
  ; 2564,783 -> 2273,425
  (road city-2-loc-2 city-2-loc-3)
  
  ; 2566,552 -> 2742,542
  (road city-2-loc-4 city-2-loc-1)
  
  ; 2742,542 -> 2566,552
  (road city-2-loc-1 city-2-loc-4)
  
  ; 2566,552 -> 2564,783
  (road city-2-loc-4 city-2-loc-2)
  
  ; 2564,783 -> 2566,552
  (road city-2-loc-2 city-2-loc-4)
  
  ; 2566,552 -> 2273,425
  (road city-2-loc-4 city-2-loc-3)
  
  ; 2273,425 -> 2566,552
  (road city-2-loc-3 city-2-loc-4)
  
  ; 2174,643 -> 2564,783
  (road city-2-loc-5 city-2-loc-2)
  
  ; 2564,783 -> 2174,643
  (road city-2-loc-2 city-2-loc-5)
  
  ; 2174,643 -> 2273,425
  (road city-2-loc-5 city-2-loc-3)
  
  ; 2273,425 -> 2174,643
  (road city-2-loc-3 city-2-loc-5)
  
  ; 2174,643 -> 2566,552
  (road city-2-loc-5 city-2-loc-4)
  
  ; 2566,552 -> 2174,643
  (road city-2-loc-4 city-2-loc-5)
  
  ; 2946,916 -> 2742,542
  (road city-2-loc-6 city-2-loc-1)
  
  ; 2742,542 -> 2946,916
  (road city-2-loc-1 city-2-loc-6)
  
  ; 2946,916 -> 2564,783
  (road city-2-loc-6 city-2-loc-2)
  
  ; 2564,783 -> 2946,916
  (road city-2-loc-2 city-2-loc-6)
  
  ; 977,899 <-> 2174,643
  (road city-1-loc-5 city-2-loc-5)
  
  (road city-2-loc-5 city-1-loc-5)
  
  (at package-1 city-1-loc-6)
  (at package-2 city-1-loc-2)
  (at package-3 city-1-loc-1)
  (at package-4 city-1-loc-4)
  (at truck-1 city-2-loc-5)
  (capacity truck-1 capacity-4)
  (at truck-2 city-2-loc-2)
  (capacity truck-2 capacity-3)
 )
 (:goal (and
  (at package-1 city-2-loc-1)
  (at package-2 city-2-loc-5)
  (at package-3 city-2-loc-3)
  (at package-4 city-2-loc-5)
 ))
 
)
