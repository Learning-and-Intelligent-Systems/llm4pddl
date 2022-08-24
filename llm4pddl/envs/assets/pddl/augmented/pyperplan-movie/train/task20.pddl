(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    k1 - object
    p1 - object
    z1 - object
  )
  (:init
    (pop p1)
    (cheese z1)
    (crackers k1)
  )
  (:goal (and (counter-at-zero) (have-pop) (have-cheese) (have-crackers)))
)
