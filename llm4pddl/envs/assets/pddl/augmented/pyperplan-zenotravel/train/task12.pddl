(define (problem ztravel-1-2)
  (:domain zeno-travel)
  (:objects
    city0 - city
    city1 - city
    fl1 - flevel
    fl2 - flevel
    person1 - person
    plane1 - aircraft
  )
  (:init
    (at plane1 city0)
    (fuel-level plane1 fl1)
    (at person1 city0)
    (next fl1 fl2)
  )
  (:goal (and (at plane1 city1) (at person1 city0)))
)
