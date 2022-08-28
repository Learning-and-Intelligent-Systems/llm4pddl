(define (problem roverprob1234)
  (:domain rover)
  (:objects
    general - lander
    rover0 - rover
    rover0store - store
    waypoint0 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint3 waypoint0)
    (at_rock_sample waypoint3)
    (at_lander general waypoint0)
    (channel_free general)
    (at rover0 waypoint3)
    (available rover0)
    (store_of rover0store rover0)
    (empty rover0store)
    (equipped_for_rock_analysis rover0)
  )
  (:goal (and (communicated_rock_data waypoint3)))
)
