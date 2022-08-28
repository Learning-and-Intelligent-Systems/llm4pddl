(define (problem mixed-f10-p5-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0)
  (:domain miconic)
  (:objects
    f0 - floor
    f1 - floor
    f3 - floor
    f5 - floor
    f9 - floor
    p2 - passenger
    p4 - passenger
  )
  (:init
    (above f0 f9)
    (above f1 f9)
    (above f3 f9)
    (above f5 f9)
    (origin p2 f3)
    (destin p2 f5)
    (origin p4 f9)
    (destin p4 f1)
    (lift-at f0)
  )
  (:goal (and (served p2) (served p4)))
)
