(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    c1 - object
    z1 - object
  )
  (:init
    (chips c1)
    (cheese z1)
  )
  (:goal (and (counter-at-zero) (have-chips) (have-cheese)))
)
