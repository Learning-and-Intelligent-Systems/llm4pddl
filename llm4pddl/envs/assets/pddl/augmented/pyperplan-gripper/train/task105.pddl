(define (problem strips-gripper-x-3)
  (:domain gripper-strips)
  (:objects
    ball3 - object
    ball4 - object
    ball7 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball7)
    (ball ball4)
    (ball ball3)
    (at-robby rooma)
    (free right)
    (at ball7 rooma)
    (at ball4 rooma)
    (at ball3 rooma)
    (gripper right)
  )
  (:goal (and (at ball7 roomb) (at ball4 roomb) (at ball3 roomb)))
)
