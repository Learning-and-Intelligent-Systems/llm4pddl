(define (problem task8) (:domain easy_delivery)
  (:objects
    loc-0 - loc
    loc-1 - loc
    loc-2 - loc
    loc-3 - loc
    paper-0 - paper
    paper-1 - paper
  )
  (:init
    (at loc-2)
    (ishomebase loc-2)
    (safe loc-0)
    (safe loc-1)
    (safe loc-2)
    (satisfied loc-2)
    (unpacked paper-0)
    (unpacked paper-1)
    (wantspaper loc-0)
    (wantspaper loc-1)
  )
  (:goal (and (satisfied loc-0)
    (satisfied loc-1)))
)
