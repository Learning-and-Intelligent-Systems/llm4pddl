(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    z1 - object
  )
  (:init
    (cheese z1)
    (counter-at-other-than-two-hours)
  )
  (:goal (and (movie-rewound) (counter-at-zero) (have-cheese)))
)
