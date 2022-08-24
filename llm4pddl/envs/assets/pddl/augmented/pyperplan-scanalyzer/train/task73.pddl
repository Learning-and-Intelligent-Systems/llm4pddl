(define (problem scanalyzer3d-54)
  (:domain scanalyzer3d)
  (:objects
    car-in-1a - car
    car-in-1b - car
    car-out-1a - car
    car-out-1b - car
    seg-in-1a - segment
    seg-in-1b - segment
    seg-out-1a - segment
    seg-out-1b - segment
  )
  (:init
    (cycle-4-with-analysis seg-in-1a seg-in-1b seg-out-1a seg-out-1b)
    (on car-in-1a seg-in-1a)
    (on car-in-1b seg-in-1b)
    (on car-out-1a seg-out-1a)
    (on car-out-1b seg-out-1b)
  )
  (:goal (and (analyzed car-out-1a) (on car-in-1a seg-out-1b)))
)
