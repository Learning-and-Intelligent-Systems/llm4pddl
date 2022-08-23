(define (problem strips-movie-x-5)
  (:domain movie-strips)
  (:objects
    c1 - object
    d1 - object
    k1 - object
    p1 - object
    z1 - object
  )
  (:init
    (chips c1)
    (dip d1)
    (pop p1)
    (cheese z1)
    (crackers k1)
    (counter-at-other-than-two-hours)
  )
  (:goal (and (movie-rewound) (counter-at-zero) (have-chips) (have-dip) (have-pop) (have-cheese) (have-crackers)))
)
