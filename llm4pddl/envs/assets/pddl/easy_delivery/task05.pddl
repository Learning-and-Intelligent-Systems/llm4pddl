(define (problem task5) (:domain easy_delivery)
  (:objects
    loc-0 - loc
    loc-1 - loc
    loc-2 - loc
    paper-0 - paper
    paper-1 - paper
    paper-2 - paper
  )
  (:init
    (at loc-1)
    (ishomebase loc-1)
    (safe loc-0)
    (safe loc-1)
    (safe loc-2)
    (satisfied loc-1)
    (unpacked paper-0)
    (unpacked paper-1)
    (unpacked paper-2)
    (wantspaper loc-0)
    (wantspaper loc-2)
  )
  (:goal (and (satisfied loc-0)
    (satisfied loc-2)))
)
