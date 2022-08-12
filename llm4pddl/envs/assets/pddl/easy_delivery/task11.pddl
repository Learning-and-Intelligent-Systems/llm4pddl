(define (problem task11) (:domain easy_delivery)
  (:objects
    loc-0 - loc
    loc-1 - loc
    loc-2 - loc
    loc-3 - loc
    loc-4 - loc
    paper-0 - paper
    paper-1 - paper
    paper-2 - paper
  )
  (:init
    (at loc-2)
    (ishomebase loc-2)
    (safe loc-0)
    (safe loc-2)
    (safe loc-3)
    (safe loc-4)
    (satisfied loc-2)
    (unpacked paper-0)
    (unpacked paper-1)
    (unpacked paper-2)
    (wantspaper loc-0)
    (wantspaper loc-3)
    (wantspaper loc-4)
  )
  (:goal (and (satisfied loc-0)
    (satisfied loc-3)
    (satisfied loc-4)))
)
