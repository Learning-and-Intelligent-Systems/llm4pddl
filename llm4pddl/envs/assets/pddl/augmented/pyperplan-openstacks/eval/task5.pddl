(define (problem os-sequencedstrips-p14_1)
(:domain openstacks-sequencedstrips-nonADL-nonNegated)
(:objects 
n0 n1 n2 n3 n4 n5 n6 n7 n8 n9 n10 n11 n12 n13 n14  - count
)

(:init
(next-count n0 n1) (next-count n1 n2) (next-count n2 n3) (next-count n3 n4) (next-count n4 n5) (next-count n5 n6) (next-count n6 n7) (next-count n7 n8) (next-count n8 n9) (next-count n9 n10) (next-count n10 n11) (next-count n11 n12) (next-count n12 n13) (next-count n13 n14) 
(stacks-avail n0)

(waiting o1)
(includes o1 p14)

(waiting o2)
(includes o2 p6)

(waiting o3)
(includes o3 p3)(includes o3 p10)

(waiting o4)
(includes o4 p3)

(waiting o5)
(includes o5 p7)

(waiting o6)
(includes o6 p9)

(waiting o7)
(includes o7 p3)(includes o7 p6)(includes o7 p7)(includes o7 p11)

(waiting o8)
(includes o8 p2)

(waiting o9)
(includes o9 p7)

(waiting o10)
(includes o10 p5)(includes o10 p11)

(waiting o11)
(includes o11 p8)

(waiting o12)
(includes o12 p4)(includes o12 p6)

(waiting o13)
(includes o13 p8)(includes o13 p9)(includes o13 p12)(includes o13 p13)

(waiting o14)
(includes o14 p1)

(not-made p1)
(not-made p2)
(not-made p3)
(not-made p4)
(not-made p5)
(not-made p6)
(not-made p7)
(not-made p8)
(not-made p9)
(not-made p10)
(not-made p11)
(not-made p12)
(not-made p13)
(not-made p14)



)

(:goal
(and
(shipped o1)
(shipped o2)
(shipped o3)
(shipped o4)
(shipped o5)
(shipped o6)
(shipped o7)
(shipped o8)
(shipped o9)
(shipped o10)
(shipped o11)
(shipped o12)
(shipped o13)
(shipped o14)
))



)

