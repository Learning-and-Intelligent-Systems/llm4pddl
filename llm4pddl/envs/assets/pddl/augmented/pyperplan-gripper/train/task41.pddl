(define (problem strips-gripper-x-2)
  (:domain gripper-strips)
  (:objects
    ball3 - object
    ball5 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball5)
    (ball ball3)
    (at-robby rooma)
    (free right)
    (at ball5 rooma)
    (at ball3 rooma)
    (gripper right)
  )
  (:goal (and (at ball5 roomb) (at ball3 roomb)))
)
