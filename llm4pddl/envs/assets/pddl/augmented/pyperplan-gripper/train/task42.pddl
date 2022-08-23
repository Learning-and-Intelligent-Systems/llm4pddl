(define (problem strips-gripper-x-2)
  (:domain gripper-strips)
  (:objects
    ball2 - object
    ball3 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball3)
    (ball ball2)
    (at-robby rooma)
    (free right)
    (at ball3 rooma)
    (at ball2 rooma)
    (gripper right)
  )
  (:goal (and (at ball3 roomb) (at ball2 roomb)))
)
