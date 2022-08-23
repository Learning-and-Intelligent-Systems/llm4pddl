(define (problem strips-gripper-x-3)
  (:domain gripper-strips)
  (:objects
    ball1 - object
    ball2 - object
    ball3 - object
    ball5 - object
    ball6 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball6)
    (ball ball5)
    (ball ball3)
    (ball ball2)
    (ball ball1)
    (at-robby rooma)
    (free right)
    (at ball6 rooma)
    (at ball5 rooma)
    (at ball3 rooma)
    (at ball2 rooma)
    (at ball1 rooma)
    (gripper right)
  )
  (:goal (and (at ball6 roomb) (at ball5 roomb) (at ball3 roomb) (at ball2 roomb) (at ball1 roomb)))
)
