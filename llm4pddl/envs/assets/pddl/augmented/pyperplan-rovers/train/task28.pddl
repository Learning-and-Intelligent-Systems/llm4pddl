(define (problem roverprob1234)
  (:domain rover)
  (:objects
    general - lander
    rover0 - rover
    rover0store - store
    waypoint0 - waypoint
    waypoint1 - waypoint
    waypoint2 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint2 waypoint1)
    (visible waypoint1 waypoint2)
    (visible waypoint3 waypoint0)
    (visible waypoint3 waypoint1)
    (visible waypoint1 waypoint3)
    (at_soil_sample waypoint2)
    (at_lander general waypoint0)
    (channel_free general)
    (at rover0 waypoint3)
    (available rover0)
    (store_of rover0store rover0)
    (empty rover0store)
    (equipped_for_soil_analysis rover0)
    (can_traverse rover0 waypoint3 waypoint1)
    (can_traverse rover0 waypoint1 waypoint3)
    (can_traverse rover0 waypoint1 waypoint2)
    (can_traverse rover0 waypoint2 waypoint1)
  )
  (:goal (and (communicated_soil_data waypoint2)))
)
