(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    d1 - object
    k1 - object
    p1 - object
  )
  (:init
    (dip d1)
    (pop p1)
    (crackers k1)
  )
  (:goal (and (have-dip) (have-pop) (have-crackers)))
)
