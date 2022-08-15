(define (problem task30) (:domain medium_delivery)
  (:objects
    loc-0 - loc
    loc-1 - loc
    loc-10 - loc
    loc-11 - loc
    loc-12 - loc
    loc-13 - loc
    loc-14 - loc
    loc-15 - loc
    loc-16 - loc
    loc-17 - loc
    loc-18 - loc
    loc-19 - loc
    loc-2 - loc
    loc-3 - loc
    loc-4 - loc
    loc-5 - loc
    loc-6 - loc
    loc-7 - loc
    loc-8 - loc
    loc-9 - loc
    paper-0 - paper
    paper-1 - paper
    paper-10 - paper
    paper-11 - paper
    paper-12 - paper
    paper-2 - paper
    paper-3 - paper
    paper-4 - paper
    paper-5 - paper
    paper-6 - paper
    paper-7 - paper
    paper-8 - paper
    paper-9 - paper
  )
  (:init
    (at loc-0)
    (ishomebase loc-0)
    (safe loc-0)
    (safe loc-11)
    (safe loc-12)
    (safe loc-13)
    (safe loc-14)
    (safe loc-15)
    (safe loc-17)
    (safe loc-18)
    (safe loc-19)
    (safe loc-1)
    (safe loc-4)
    (safe loc-8)
    (satisfied loc-0)
    (unpacked paper-0)
    (unpacked paper-10)
    (unpacked paper-11)
    (unpacked paper-12)
    (unpacked paper-1)
    (unpacked paper-2)
    (unpacked paper-3)
    (unpacked paper-4)
    (unpacked paper-5)
    (unpacked paper-6)
    (unpacked paper-7)
    (unpacked paper-8)
    (unpacked paper-9)
    (wantspaper loc-11)
    (wantspaper loc-12)
    (wantspaper loc-13)
    (wantspaper loc-14)
    (wantspaper loc-15)
    (wantspaper loc-17)
    (wantspaper loc-18)
    (wantspaper loc-19)
    (wantspaper loc-1)
    (wantspaper loc-4)
    (wantspaper loc-8)
  )
  (:goal (and (satisfied loc-11)
    (satisfied loc-12)
    (satisfied loc-13)
    (satisfied loc-14)
    (satisfied loc-15)
    (satisfied loc-17)
    (satisfied loc-18)
    (satisfied loc-19)
    (satisfied loc-1)
    (satisfied loc-4)
    (satisfied loc-8)))
)