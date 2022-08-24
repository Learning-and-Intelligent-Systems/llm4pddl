(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    k1 - object
  )
  (:init
    (crackers k1)
    (counter-at-other-than-two-hours)
  )
  (:goal (and (movie-rewound) (counter-at-zero) (have-crackers)))
)
