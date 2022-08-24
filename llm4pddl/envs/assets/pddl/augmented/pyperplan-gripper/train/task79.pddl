(define (problem strips-gripper-x-3)
  (:domain gripper-strips)
  (:objects
    ball2 - object
    ball3 - object
    ball4 - object
    ball5 - object
    ball6 - object
    ball7 - object
    ball8 - object
    right - object
    rooma - object
    roomb - object
  )
  (:init
    (room rooma)
    (room roomb)
    (ball ball8)
    (ball ball7)
    (ball ball6)
    (ball ball5)
    (ball ball4)
    (ball ball3)
    (ball ball2)
    (at-robby rooma)
    (free right)
    (at ball8 rooma)
    (at ball7 rooma)
    (at ball6 rooma)
    (at ball5 rooma)
    (at ball4 rooma)
    (at ball3 rooma)
    (at ball2 rooma)
    (gripper right)
  )
  (:goal (and (at ball8 roomb) (at ball7 roomb) (at ball6 roomb) (at ball5 roomb) (at ball4 roomb) (at ball3 roomb) (at ball2 roomb)))
)
