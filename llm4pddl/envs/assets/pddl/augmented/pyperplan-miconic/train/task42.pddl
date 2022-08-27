(define (problem mixed-f10-p5-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0)
  (:domain miconic)
  (:objects
    f0 - floor
    f1 - floor
    f2 - floor
    f6 - floor
    f9 - floor
    p3 - passenger
    p4 - passenger
  )
  (:init
    (above f0 f9)
    (above f1 f9)
    (above f2 f9)
    (above f6 f9)
    (origin p3 f6)
    (destin p3 f2)
    (origin p4 f9)
    (destin p4 f1)
    (lift-at f0)
  )
  (:goal (and (served p3) (served p4)))
)
