(define (problem mixed-f4-p2-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0)
  (:domain miconic)
  (:objects
    f0 - floor
    f1 - floor
    f3 - floor
    p1 - passenger
  )
  (:init
    (above f0 f3)
    (above f1 f3)
    (origin p1 f1)
    (destin p1 f3)
    (lift-at f0)
  )
  (:goal (and (served p1)))
)
