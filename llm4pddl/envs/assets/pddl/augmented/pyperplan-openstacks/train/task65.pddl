(define (problem os-sequencedstrips-p6_1)
  (:domain openstacks-sequencedstrips-nonadl-nonnegated)
  (:objects
    n0 - count
    n1 - count
  )
  (:init
    (next-count n0 n1)
    (stacks-avail n0)
    (waiting o3)
    (waiting o5)
    (not-made p1)
    (not-made p5)
  )
  (:goal (and (shipped o3) (shipped o5)))
)
