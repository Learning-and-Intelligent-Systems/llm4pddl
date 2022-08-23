(define (problem mixed-f8-p4-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0)
  (:domain miconic)
  (:objects
    f0 - floor
    f1 - floor
    f2 - floor
    f3 - floor
    f4 - floor
    f7 - floor
    p1 - passenger
    p3 - passenger
  )
  (:init
    (above f0 f7)
    (above f1 f7)
    (above f2 f7)
    (above f3 f7)
    (above f4 f7)
    (origin p1 f1)
    (destin p1 f3)
    (origin p3 f2)
    (destin p3 f4)
    (lift-at f0)
  )
  (:goal (and (served p1) (served p3)))
)
