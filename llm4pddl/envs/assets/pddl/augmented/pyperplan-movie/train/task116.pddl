(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    c1 - object
    d1 - object
  )
  (:init
    (chips c1)
    (dip d1)
  )
  (:goal (and (have-chips) (have-dip)))
)
