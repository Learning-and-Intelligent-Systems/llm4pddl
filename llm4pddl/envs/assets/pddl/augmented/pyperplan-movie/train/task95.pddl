(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    c1 - object
    k1 - object
    z1 - object
  )
  (:init
    (chips c1)
    (cheese z1)
    (crackers k1)
  )
  (:goal (and (have-chips) (have-cheese) (have-crackers)))
)
