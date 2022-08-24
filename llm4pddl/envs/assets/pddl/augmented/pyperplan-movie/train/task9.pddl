(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    d1 - object
    k1 - object
    p1 - object
    z1 - object
  )
  (:init
    (dip d1)
    (pop p1)
    (cheese z1)
    (crackers k1)
    (counter-at-other-than-two-hours)
  )
  (:goal (and (movie-rewound) (counter-at-zero) (have-dip) (have-pop) (have-cheese) (have-crackers)))
)
