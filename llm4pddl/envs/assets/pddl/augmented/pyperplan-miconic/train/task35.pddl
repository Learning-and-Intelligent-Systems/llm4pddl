(define (problem mixed-f10-p5-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0)
  (:domain miconic)
  (:objects
    f0 - floor
    f1 - floor
    f2 - floor
    f3 - floor
    f5 - floor
    f6 - floor
    f7 - floor
    f9 - floor
    p0 - passenger
    p1 - passenger
    p3 - passenger
    p4 - passenger
  )
  (:init
    (above f0 f9)
    (above f1 f9)
    (above f2 f9)
    (above f3 f9)
    (above f5 f9)
    (above f6 f9)
    (above f7 f9)
    (origin p0 f3)
    (destin p0 f6)
    (origin p1 f7)
    (destin p1 f5)
    (origin p3 f6)
    (destin p3 f2)
    (origin p4 f9)
    (destin p4 f1)
    (lift-at f0)
  )
  (:goal (and (served p0) (served p1) (served p3) (served p4)))
)
