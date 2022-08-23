(define (problem ztravel-2-5)
  (:domain zeno-travel)
  (:objects
    city1 - city
    city2 - city
    fl5 - flevel
    fl6 - flevel
    person2 - person
    plane1 - aircraft
  )
  (:init
    (at plane1 city2)
    (fuel-level plane1 fl5)
    (at person2 city1)
    (next fl5 fl6)
  )
  (:goal (and (at person2 city2)))
)
