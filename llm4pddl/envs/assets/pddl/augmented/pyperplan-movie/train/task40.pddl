(define (problem strips-movie-x-1)
  (:domain movie-strips)
  (:objects
    k1 - object
    p1 - object
  )
  (:init
    (pop p1)
    (crackers k1)
    (counter-at-other-than-two-hours)
  )
  (:goal (and (movie-rewound) (have-pop) (have-crackers)))
)
