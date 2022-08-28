(define (problem roverprob6232)
  (:domain rover)
  (:objects
    general - lander
    rover1 - rover
    rover1store - store
    waypoint1 - waypoint
    waypoint2 - waypoint
  )
  (:init
    (visible waypoint2 waypoint1)
    (visible waypoint1 waypoint2)
    (at_rock_sample waypoint1)
    (at_lander general waypoint2)
    (channel_free general)
    (at rover1 waypoint2)
    (available rover1)
    (store_of rover1store rover1)
    (empty rover1store)
    (equipped_for_rock_analysis rover1)
    (can_traverse rover1 waypoint2 waypoint1)
  )
  (:goal (and (communicated_rock_data waypoint1)))
)
