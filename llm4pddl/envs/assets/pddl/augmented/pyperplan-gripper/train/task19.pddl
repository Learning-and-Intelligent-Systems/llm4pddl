(define (problem strips-gripper-x-1)
  (:domain gripper-strips)
  (:objects
    ball2 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball2)
    (at-robby rooma)
    (free right)
    (at ball2 rooma)
    (gripper right)
  )
  (:goal (and (at ball2 roomb)))
)
