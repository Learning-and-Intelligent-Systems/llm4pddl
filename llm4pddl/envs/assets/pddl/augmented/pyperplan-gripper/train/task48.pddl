(define (problem strips-gripper-x-2)
  (:domain gripper-strips)
  (:objects
    ball4 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball4)
    (at-robby rooma)
    (free right)
    (at ball4 rooma)
    (gripper right)
  )
  (:goal (and (at ball4 roomb)))
)
