
(define (problem manygripper) (:domain gripper-strips)
  (:objects
        ball0
	ball1
	ball10
	ball11
	ball12
	ball13
	ball14
	ball15
	ball16
	ball17
	ball18
	ball19
	ball2
	ball20
	ball21
	ball22
	ball23
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
	(at ball14 room0)
	(at ball15 room0)
	(at ball16 room0)
	(at ball17 room0)
	(at ball18 room0)
	(at ball19 room0)
	(at ball1 room0)
	(at ball20 room0)
	(at ball21 room0)
	(at ball22 room0)
	(at ball23 room0)
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
	(ball ball14)
	(ball ball15)
	(ball ball16)
	(ball ball17)
	(ball ball18)
	(ball ball19)
	(ball ball1)
	(ball ball20)
	(ball ball21)
	(ball ball22)
	(ball ball23)
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
	(at ball22 room1)
	(at ball20 room1)
	(at ball16 room1)
	(at ball10 room1)))
)
