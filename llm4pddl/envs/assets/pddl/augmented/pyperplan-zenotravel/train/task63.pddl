(define (problem ztravel-2-5)
  (:domain zeno-travel)
  (:objects
    city0 - city
    city2 - city
    fl5 - flevel
    fl6 - flevel
    person3 - person
    person5 - person
    plane1 - aircraft
  )
  (:init
    (at plane1 city2)
    (fuel-level plane1 fl5)
    (at person3 city0)
    (at person5 city2)
    (next fl5 fl6)
  )
  (:goal (and (at plane1 city0) (at person3 city0) (at person5 city2)))
)
