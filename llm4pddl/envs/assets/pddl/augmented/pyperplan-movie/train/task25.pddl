(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    k1 - object
    z1 - object
  )
  (:init
    (cheese z1)
    (crackers k1)
  )
  (:goal (and (counter-at-zero) (have-cheese) (have-crackers)))
)
