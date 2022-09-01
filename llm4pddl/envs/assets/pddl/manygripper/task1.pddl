
(define (problem manygripper) (:domain gripper-strips)
  (:objects
        ball0
	ball1
	ball2
	ball3
	left
	right
	room0
	room1
  )
  (:init 
	(at ball0 room0)
	(at ball1 room0)
	(at ball2 room0)
	(at ball3 room0)
	(at-robby room0)
	(ball ball0)
	(ball ball1)
	(ball ball2)
	(ball ball3)
	(free left)
	(free right)
	(gripper left)
	(gripper right)
	(room room0)
	(room room1)
  )
  (:goal (and
	(at ball2 room1)
	(at ball3 room1)
	(at ball1 room1)
	(at ball0 room1)))
)
