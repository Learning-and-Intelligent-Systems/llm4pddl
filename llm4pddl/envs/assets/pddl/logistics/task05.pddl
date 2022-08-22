(define (problem logistics-custom-5)
(:domain logistics)
(:objects
  myairplane - airplane
  myairport1 myairport2 - airport
  place1 place2 - location
  mycity1 mycity2 - city
  mytruck1 mytruck2 - truck
  mypackage6 mypackage5 mypackage4 mypackage3 mypackage2 mypackage1 - package)

(:init (at myairplane myairport1) (at mytruck1 place1) (at mypackage1 place1)
 (at mypackage2 place1) (at mypackage3 place1) (at mytruck2 place2) (at mypackage4 place2) (at mypackage5 place2)
 (at mypackage6 place2) (in-city place1 mycity1) (in-city myairport1 mycity1) (in-city place2 mycity2)
 (in-city myairport2 mycity2))

(:goal (and (at mypackage4 myairport2) (at mypackage1 myairport2)))
)
