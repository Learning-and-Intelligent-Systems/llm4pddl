(define (problem ztravel-2-4)
  (:domain zeno-travel)
  (:objects
    city0 - city
    city1 - city
    city2 - city
    fl5 - flevel
    fl6 - flevel
    person2 - person
    person3 - person
    plane2 - aircraft
  )
  (:init
    (at plane2 city2)
    (fuel-level plane2 fl5)
    (at person2 city0)
    (at person3 city1)
    (next fl5 fl6)
  )
  (:goal (and (at person2 city0) (at person3 city0)))
)
