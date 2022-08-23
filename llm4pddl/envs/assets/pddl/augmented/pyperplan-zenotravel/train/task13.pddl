(define (problem ztravel-1-2)
  (:domain zeno-travel)
  (:objects
    city0 - city
    city1 - city
    fl1 - flevel
    fl2 - flevel
    plane1 - aircraft
  )
  (:init
    (at plane1 city0)
    (fuel-level plane1 fl1)
    (next fl1 fl2)
  )
  (:goal (and (at plane1 city1)))
)
