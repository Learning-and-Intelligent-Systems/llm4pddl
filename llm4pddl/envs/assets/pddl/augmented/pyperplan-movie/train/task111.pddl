(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    c1 - object
    d1 - object
    k1 - object
    z1 - object
  )
  (:init
    (chips c1)
    (dip d1)
    (cheese z1)
    (crackers k1)
  )
  (:goal (and (counter-at-zero) (have-chips) (have-dip) (have-cheese) (have-crackers)))
)