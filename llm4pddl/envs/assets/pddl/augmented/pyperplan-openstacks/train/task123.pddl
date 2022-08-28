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
    (waiting o6)
    (waiting o7)
    (not-made p1)
    (not-made p2)
    (not-made p6)
  )
  (:goal (and (shipped o2) (shipped o6) (shipped o7)))
)
