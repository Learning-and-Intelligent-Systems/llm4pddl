(define (problem mixed-f4-p2-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0)
  (:domain miconic)
  (:objects
    f0 - floor
    f2 - floor
    f3 - floor
    p0 - passenger
  )
  (:init
    (above f0 f3)
    (above f2 f3)
    (origin p0 f3)
    (destin p0 f2)
    (lift-at f0)
  )
  (:goal (and (served p0)))
)
