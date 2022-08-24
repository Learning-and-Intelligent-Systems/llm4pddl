(define (problem strips-gripper-x-3)
  (:domain gripper-strips)
  (:objects
    ball7 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball7)
    (at-robby rooma)
    (free right)
    (at ball7 rooma)
    (gripper right)
  )
  (:goal (and (at ball7 roomb)))
)
