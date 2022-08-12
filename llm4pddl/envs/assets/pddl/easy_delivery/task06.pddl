(define (problem task6) (:domain easy_delivery)
  (:objects
    loc-0 - loc
    loc-1 - loc
    loc-2 - loc
    loc-3 - loc
    loc-4 - loc
    loc-5 - loc
    paper-0 - paper
    paper-1 - paper
    paper-2 - paper
  )
  (:init
    (at loc-4)
    (ishomebase loc-4)
    (safe loc-0)
    (safe loc-2)
    (safe loc-4)
    (satisfied loc-4)
    (unpacked paper-0)
    (unpacked paper-1)
    (unpacked paper-2)
    (wantspaper loc-0)
    (wantspaper loc-2)
  )
  (:goal (and (satisfied loc-0)
    (satisfied loc-2)))
)
