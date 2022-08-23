(define (problem strips-gripper-x-2)
  (:domain gripper-strips)
  (:objects
    ball3 - object
    ball4 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball4)
    (ball ball3)
    (at-robby rooma)
    (free right)
    (at ball4 rooma)
    (at ball3 rooma)
    (gripper right)
  )
  (:goal (and (at ball4 roomb) (at ball3 roomb)))
)
