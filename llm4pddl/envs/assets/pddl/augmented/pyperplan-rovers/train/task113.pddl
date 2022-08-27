(define (problem roverprob2435)
  (:domain rover)
  (:objects
    general - lander
    rover0 - rover
    rover0store - store
    rover1 - rover
    rover1store - store
    waypoint0 - waypoint
    waypoint1 - waypoint
    waypoint2 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint0 waypoint1)
    (visible waypoint1 waypoint3)
    (visible waypoint1 waypoint2)
    (visible waypoint2 waypoint3)
    (at_rock_sample waypoint0)
    (at_rock_sample waypoint1)
    (at_soil_sample waypoint2)
    (at_lander general waypoint3)
    (channel_free general)
    (at rover0 waypoint0)
    (available rover0)
    (store_of rover0store rover0)
    (empty rover0store)
    (equipped_for_rock_analysis rover0)
    (can_traverse rover0 waypoint0 waypoint1)
    (at rover1 waypoint0)
    (available rover1)
    (store_of rover1store rover1)
    (empty rover1store)
    (equipped_for_soil_analysis rover1)
    (can_traverse rover1 waypoint0 waypoint1)
    (can_traverse rover1 waypoint1 waypoint2)
  )
  (:goal (and (communicated_soil_data waypoint2) (communicated_rock_data waypoint0) (communicated_rock_data waypoint1)))
)