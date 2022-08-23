(define (problem ztravel-2-5)
  (:domain zeno-travel)
  (:objects
    city0 - city
    city1 - city
    city2 - city
    fl0 - flevel
    fl1 - flevel
    person2 - person
    person4 - person
    plane2 - aircraft
  )
  (:init
    (at plane2 city2)
    (fuel-level plane2 fl0)
    (at person2 city1)
    (at person4 city0)
    (next fl0 fl1)
  )
  (:goal (and (at person2 city2) (at person4 city1)))
)
