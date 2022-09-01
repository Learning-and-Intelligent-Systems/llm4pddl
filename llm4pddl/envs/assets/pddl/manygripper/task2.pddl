
(define (problem manygripper) (:domain gripper-strips)
  (:objects
        ball0
	ball1
	ball10
	ball11
	ball12
	ball13
	ball2
	ball3
	ball4
	ball5
	ball6
	ball7
	ball8
	ball9
	left
	right
	room0
	room1
  )
  (:init 
	(at ball0 room0)
	(at ball10 room0)
	(at ball11 room0)
	(at ball12 room0)
	(at ball13 room0)
	(at ball1 room0)
	(at ball2 room0)
	(at ball3 room0)
	(at ball4 room0)
	(at ball5 room0)
	(at ball6 room0)
	(at ball7 room0)
	(at ball8 room0)
	(at ball9 room0)
	(at-robby room0)
	(ball ball0)
	(ball ball10)
	(ball ball11)
	(ball ball12)
	(ball ball13)
	(ball ball1)
	(ball ball2)
	(ball ball3)
	(ball ball4)
	(ball ball5)
	(ball ball6)
	(ball ball7)
	(ball ball8)
	(ball ball9)
	(free left)
	(free right)
	(gripper left)
	(gripper right)
	(room room0)
	(room room1)
  )
  (:goal (and
	(at ball1 room1)
	(at ball6 room1)
	(at ball8 room1)
	(at ball10 room1)))
)
