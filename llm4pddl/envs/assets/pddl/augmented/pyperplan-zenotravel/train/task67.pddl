(define (problem ztravel-2-5)
  (:domain zeno-travel)
  (:objects
    city0 - city
    city2 - city
    fl5 - flevel
    fl6 - flevel
    plane1 - aircraft
  )
  (:init
    (at plane1 city2)
    (fuel-level plane1 fl5)
    (next fl5 fl6)
  )
  (:goal (and (at plane1 city0)))
)
