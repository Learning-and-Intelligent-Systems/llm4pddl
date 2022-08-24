(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    d1 - object
    k1 - object
  )
  (:init
    (dip d1)
    (crackers k1)
    (counter-at-other-than-two-hours)
  )
  (:goal (and (movie-rewound) (counter-at-zero) (have-dip) (have-crackers)))
)
