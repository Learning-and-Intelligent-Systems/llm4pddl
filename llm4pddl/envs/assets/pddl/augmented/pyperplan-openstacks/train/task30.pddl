(define (problem os-sequencedstrips-p5_1)
  (:domain openstacks-sequencedstrips-nonadl-nonnegated)
  (:objects
    n0 - count
    n1 - count
  )
  (:init
    (next-count n0 n1)
    (stacks-avail n0)
    (waiting o1)
    (waiting o2)
    (waiting o5)
    (not-made p2)
    (not-made p5)
  )
  (:goal (and (shipped o1) (shipped o5)))
)
