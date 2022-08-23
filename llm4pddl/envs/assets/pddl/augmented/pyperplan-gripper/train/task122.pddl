(define (problem strips-gripper-x-3)
  (:domain gripper-strips)
  (:objects
    ball3 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball3)
    (at-robby rooma)
    (free right)
    (at ball3 rooma)
    (gripper right)
  )
  (:goal (and (at ball3 roomb)))
)
