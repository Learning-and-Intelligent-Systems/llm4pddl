(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    p1 - object
    z1 - object
  )
  (:init
    (pop p1)
    (cheese z1)
    (counter-at-other-than-two-hours)
  )
  (:goal (and (movie-rewound) (have-pop) (have-cheese)))
)
