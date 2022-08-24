(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    c1 - object
    d1 - object
    k1 - object
  )
  (:init
    (chips c1)
    (dip d1)
    (crackers k1)
    (counter-at-other-than-two-hours)
  )
  (:goal (and (movie-rewound) (have-chips) (have-dip) (have-crackers)))
)
