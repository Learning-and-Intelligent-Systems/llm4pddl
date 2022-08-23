(define (problem ztravel-1-3)
  (:domain zeno-travel)
  (:objects
    city0 - city
    city2 - city
    fl2 - flevel
    fl3 - flevel
    person3 - person
    plane1 - aircraft
  )
  (:init
    (at plane1 city0)
    (fuel-level plane1 fl2)
    (at person3 city2)
    (next fl2 fl3)
  )
  (:goal (and (at plane1 city2) (at person3 city2)))
)
