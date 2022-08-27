(define (problem roverprob4213)
  (:domain rover)
  (:objects
    general - lander
    rover0 - rover
    rover0store - store
    waypoint0 - waypoint
    waypoint1 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint3 waypoint1)
    (visible waypoint0 waypoint3)
    (at_rock_sample waypoint0)
    (at_lander general waypoint1)
    (channel_free general)
    (at rover0 waypoint0)
    (available rover0)
    (store_of rover0store rover0)
    (empty rover0store)
    (equipped_for_rock_analysis rover0)
    (can_traverse rover0 waypoint0 waypoint3)
  )
  (:goal (and (communicated_rock_data waypoint0)))
)
