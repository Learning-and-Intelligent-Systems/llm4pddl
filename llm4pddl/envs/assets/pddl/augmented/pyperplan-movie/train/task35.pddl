(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    z1 - object
  )
  (:init
    (cheese z1)
  )
  (:goal (and (counter-at-zero) (have-cheese)))
)
