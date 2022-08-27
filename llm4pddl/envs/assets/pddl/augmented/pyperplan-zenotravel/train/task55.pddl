(define (problem ztravel-2-4)
  (:domain zeno-travel)
  (:objects
    city1 - city
    city2 - city
    city3 - city
    fl0 - flevel
    fl1 - flevel
    person1 - person
    person4 - person
    plane2 - aircraft
  )
  (:init
    (at plane2 city2)
    (fuel-level plane2 fl0)
    (at person1 city3)
    (at person4 city1)
    (next fl0 fl1)
  )
  (:goal (and (at person1 city2) (at person4 city3)))
)