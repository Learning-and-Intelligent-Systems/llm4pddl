(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    c1 - object
    k1 - object
  )
  (:init
    (chips c1)
    (crackers k1)
  )
  (:goal (and (counter-at-zero) (have-chips) (have-crackers)))
)
