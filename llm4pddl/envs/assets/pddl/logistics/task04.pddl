(define (problem logistics-custom-4)
(:domain logistics)
(:objects
  apn1 - airplane
  apt2 apt1 - airport
  pos2 pos1 - location
  cit2 cit1 - city
  tru2 tru1 - truck
  obj11 - package)

(:init (at apn1 apt1) (at tru1 pos1) (at obj11 pos1)
 (at tru2 pos2) (in-city pos1 cit1) (in-city apt1 cit1) (in-city pos2 cit2)
 (in-city apt2 cit2))

(:goal (and (at obj11 apt2)))
)
