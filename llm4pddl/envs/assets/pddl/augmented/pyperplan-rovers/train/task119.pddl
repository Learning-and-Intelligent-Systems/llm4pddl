(define (problem roverprob2435)
  (:domain rover)
  (:objects
    general - lander
    rover1 - rover
    rover1store - store
    waypoint0 - waypoint
    waypoint1 - waypoint
    waypoint2 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint0 waypoint1)
    (visible waypoint1 waypoint2)
    (visible waypoint2 waypoint3)
    (at_soil_sample waypoint1)
    (at_soil_sample waypoint2)
    (at_lander general waypoint3)
    (channel_free general)
    (at rover1 waypoint0)
    (available rover1)
    (store_of rover1store rover1)
    (empty rover1store)
    (equipped_for_soil_analysis rover1)
    (can_traverse rover1 waypoint0 waypoint1)
    (can_traverse rover1 waypoint1 waypoint2)
  )
  (:goal (and (communicated_soil_data waypoint1) (communicated_soil_data waypoint2)))
)
