(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    d1 - object
    p1 - object
    z1 - object
  )
  (:init
    (dip d1)
    (pop p1)
    (cheese z1)
    (counter-at-other-than-two-hours)
  )
  (:goal (and (movie-rewound) (have-dip) (have-pop) (have-cheese)))
)
