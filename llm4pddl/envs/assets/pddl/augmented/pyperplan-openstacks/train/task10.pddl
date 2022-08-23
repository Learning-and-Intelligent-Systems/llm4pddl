(define (problem os-sequencedstrips-p9_1)
  (:domain openstacks-sequencedstrips-nonadl-nonnegated)
  (:objects
    n0 - count
    n1 - count
    n2 - count
    n3 - count
    n4 - count
  )
  (:init
    (next-count n0 n1)
    (next-count n1 n2)
    (next-count n2 n3)
    (next-count n3 n4)
    (stacks-avail n0)
    (waiting o1)
    (waiting o2)
    (waiting o3)
    (waiting o4)
    (waiting o5)
    (waiting o6)
    (waiting o7)
    (waiting o8)
    (waiting o9)
    (not-made p1)
    (not-made p2)
    (not-made p3)
    (not-made p4)
    (not-made p5)
    (not-made p6)
    (not-made p7)
    (not-made p8)
    (not-made p9)
  )
  (:goal (and (shipped o1) (shipped o2) (shipped o3) (shipped o4) (shipped o5) (shipped o6) (shipped o7) (shipped o8) (shipped o9)))
)
