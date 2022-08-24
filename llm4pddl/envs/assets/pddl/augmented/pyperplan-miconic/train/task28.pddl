(define (problem mixed-f8-p4-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0)
  (:domain miconic)
  (:objects
    f0 - floor
    f6 - floor
    f7 - floor
    p0 - passenger
  )
  (:init
    (above f0 f7)
    (above f6 f7)
    (origin p0 f7)
    (destin p0 f6)
    (lift-at f0)
  )
  (:goal (and (served p0)))
)
