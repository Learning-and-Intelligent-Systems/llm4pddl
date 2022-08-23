(define (problem strips-gripper-x-2)
  (:domain gripper-strips)
  (:objects
    ball5 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball5)
    (at-robby rooma)
    (free right)
    (at ball5 rooma)
    (gripper right)
  )
  (:goal (and (at ball5 roomb)))
)
