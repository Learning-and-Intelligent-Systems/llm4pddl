(define (problem mixed-f8-p4-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0)
  (:domain miconic)
  (:objects
    f0 - floor
    f1 - floor
    f7 - floor
    p2 - passenger
  )
  (:init
    (above f0 f7)
    (above f1 f7)
    (origin p2 f1)
    (destin p2 f7)
    (lift-at f0)
  )
  (:goal (and (served p2)))
)
