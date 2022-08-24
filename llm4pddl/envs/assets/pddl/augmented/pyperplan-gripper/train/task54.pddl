(define (problem strips-gripper-x-2)
  (:domain gripper-strips)
  (:objects
    ball2 - object
    ball6 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball6)
    (ball ball2)
    (at-robby rooma)
    (free right)
    (at ball6 rooma)
    (at ball2 rooma)
    (gripper right)
  )
  (:goal (and (at ball6 roomb) (at ball2 roomb)))
)
