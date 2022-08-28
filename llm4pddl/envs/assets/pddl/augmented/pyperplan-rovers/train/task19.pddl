(define (problem roverprob3726)
  (:domain rover)
  (:objects
    general - lander
    rover1 - rover
    rover1store - store
    waypoint0 - waypoint
    waypoint2 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint0 waypoint3)
    (visible waypoint3 waypoint0)
    (visible waypoint3 waypoint2)
    (visible waypoint2 waypoint3)
    (at_rock_sample waypoint0)
    (at_soil_sample waypoint2)
    (at_lander general waypoint0)
    (channel_free general)
    (at rover1 waypoint3)
    (available rover1)
    (store_of rover1store rover1)
    (empty rover1store)
    (equipped_for_soil_analysis rover1)
    (equipped_for_rock_analysis rover1)
    (can_traverse rover1 waypoint3 waypoint0)
    (can_traverse rover1 waypoint0 waypoint3)
    (can_traverse rover1 waypoint3 waypoint2)
    (can_traverse rover1 waypoint2 waypoint3)
  )
  (:goal (and (communicated_soil_data waypoint2) (communicated_rock_data waypoint0)))
)
