(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    d1 - object
    p1 - object
  )
  (:init
    (dip d1)
    (pop p1)
  )
  (:goal (and (counter-at-zero) (have-dip) (have-pop)))
)
