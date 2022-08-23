(define (problem mixed-f6-p3-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0)
  (:domain miconic)
  (:objects
    f0 - floor
    f1 - floor
    f5 - floor
    p2 - passenger
  )
  (:init
    (above f0 f5)
    (above f1 f5)
    (origin p2 f5)
    (destin p2 f1)
    (lift-at f0)
  )
  (:goal (and (served p2)))
)
