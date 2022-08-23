(define (problem strips-gripper-x-2)
  (:domain gripper-strips)
  (:objects
    ball6 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball6)
    (at-robby rooma)
    (free right)
    (at ball6 rooma)
    (gripper right)
  )
  (:goal (and (at ball6 roomb)))
)
