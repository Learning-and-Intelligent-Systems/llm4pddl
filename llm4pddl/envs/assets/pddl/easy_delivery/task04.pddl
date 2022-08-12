(define (problem task4) (:domain easy_delivery)
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
    (at loc-4)
    (ishomebase loc-4)
    (safe loc-1)
    (safe loc-4)
    (satisfied loc-4)
    (unpacked paper-0)
    (unpacked paper-1)
    (wantspaper loc-1)
  )
  (:goal (and (satisfied loc-1)))
)
