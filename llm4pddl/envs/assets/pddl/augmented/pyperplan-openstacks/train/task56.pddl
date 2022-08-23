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
    (waiting o4)
    (waiting o6)
    (not-made p2)
    (not-made p3)
    (not-made p5)
  )
  (:goal (and (shipped o3) (shipped o4) (shipped o6)))
)
