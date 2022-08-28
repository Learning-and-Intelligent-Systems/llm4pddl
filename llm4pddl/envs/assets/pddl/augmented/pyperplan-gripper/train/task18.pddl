(define (problem strips-gripper-x-1)
  (:domain gripper-strips)
  (:objects
    ball1 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball1)
    (at-robby rooma)
    (free right)
    (at ball1 rooma)
    (gripper right)
  )
  (:goal (and (at ball1 roomb)))
)
