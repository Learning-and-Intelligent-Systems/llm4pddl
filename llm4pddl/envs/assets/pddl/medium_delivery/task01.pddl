(define (problem task1) (:domain medium_delivery)
  (:objects
    loc-0 - loc
    loc-1 - loc
    loc-2 - loc
    loc-3 - loc
    loc-4 - loc
    paper-0 - paper
    paper-1 - paper
  )
  (:init
    (at loc-2)
    (ishomebase loc-2)
    (safe loc-0)
    (safe loc-2)
    (safe loc-4)
    (satisfied loc-2)
    (unpacked paper-0)
    (unpacked paper-1)
    (wantspaper loc-0)
    (wantspaper loc-4)
  )
  (:goal (and (satisfied loc-0)
    (satisfied loc-4)))
)
