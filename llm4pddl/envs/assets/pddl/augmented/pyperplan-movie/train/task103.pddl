(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    c1 - object
    p1 - object
  )
  (:init
    (chips c1)
    (pop p1)
  )
  (:goal (and (counter-at-zero) (have-chips) (have-pop)))
)
