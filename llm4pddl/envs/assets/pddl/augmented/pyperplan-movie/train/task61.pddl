(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    d1 - object
    z1 - object
  )
  (:init
    (dip d1)
    (cheese z1)
  )
  (:goal (and (counter-at-zero) (have-dip) (have-cheese)))
)
