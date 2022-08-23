(define (problem roverprob6232)
  (:domain rover)
  (:objects
    camera0 - camera
    general - lander
    high_res - mode
    objective0 - objective
    rover1 - rover
    waypoint1 - waypoint
    waypoint2 - waypoint
  )
  (:init
    (visible waypoint2 waypoint1)
    (visible waypoint1 waypoint2)
    (at_lander general waypoint2)
    (channel_free general)
    (at rover1 waypoint2)
    (available rover1)
    (equipped_for_imaging rover1)
    (can_traverse rover1 waypoint2 waypoint1)
    (on_board camera0 rover1)
    (calibration_target camera0 objective0)
    (supports camera0 high_res)
    (visible_from objective0 waypoint2)
  )
  (:goal (and (communicated_image_data objective0 high_res)))
)
