(define (problem task2) (:domain medium_delivery)
  (:objects
    loc-0 - loc
    loc-1 - loc
    loc-2 - loc
    loc-3 - loc
    loc-4 - loc
    loc-5 - loc
    loc-6 - loc
    paper-0 - paper
    paper-1 - paper
    paper-2 - paper
  )
  (:init
    (at loc-0)
    (ishomebase loc-0)
    (safe loc-0)
    (safe loc-1)
    (safe loc-2)
    (satisfied loc-0)
    (unpacked paper-0)
    (unpacked paper-1)
    (unpacked paper-2)
    (wantspaper loc-1)
    (wantspaper loc-2)
  )
  (:goal (and (satisfied loc-1)
    (satisfied loc-2)))
)
