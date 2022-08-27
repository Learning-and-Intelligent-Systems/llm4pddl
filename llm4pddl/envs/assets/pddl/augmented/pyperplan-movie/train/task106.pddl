(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    c1 - object
    k1 - object
    p1 - object
    z1 - object
  )
  (:init
    (chips c1)
    (pop p1)
    (cheese z1)
    (crackers k1)
  )
  (:goal (and (have-chips) (have-pop) (have-cheese) (have-crackers)))
)
