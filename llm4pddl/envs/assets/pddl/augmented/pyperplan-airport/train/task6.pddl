(define (problem problem_x)
  (:domain airport_fixed_structure)
  (:objects
    
  )
  (:init
    (at-segment airplane_daewh seg_pp_0_60)
    (facing airplane_daewh south)
    (has-type airplane_daewh medium)
    (is-pushing airplane_daewh)
    (not_blocked seg_ppdoor_0_40 airplane_daewh)
    (not_blocked seg_tww1_0_200 airplane_daewh)
    (not_blocked seg_twe1_0_200 airplane_daewh)
    (not_blocked seg_rwe_0_50 airplane_daewh)
    (not_blocked seg_twe4_0_50 airplane_daewh)
    (not_blocked seg_twe3_0_50 airplane_daewh)
    (not_blocked seg_twe2_0_50 airplane_daewh)
    (not_occupied seg_ppdoor_0_40)
    (not_occupied seg_tww1_0_200)
    (not_occupied seg_twe1_0_200)
    (not_occupied seg_tww2_0_50)
    (not_occupied seg_rwe_0_50)
    (not_occupied seg_twe4_0_50)
    (not_occupied seg_twe3_0_50)
    (not_occupied seg_twe2_0_50)
  )
  (:goal (and (airborne airplane_daewh seg_rwe_0_50)))
)