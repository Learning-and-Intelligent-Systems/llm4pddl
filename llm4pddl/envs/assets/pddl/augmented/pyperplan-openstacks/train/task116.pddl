(define (problem os-sequencedstrips-p7_1)
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
    (waiting o3)
    (waiting o4)
    (waiting o6)
    (waiting o7)
    (not-made p2)
    (not-made p3)
    (not-made p4)
    (not-made p6)
  )
  (:goal (and (shipped o1) (shipped o2) (shipped o3) (shipped o4) (shipped o7)))
)
