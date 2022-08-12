(define (problem task1) (:domain easy_delivery)
  (:objects
    loc-0 - loc
    loc-1 - loc
    loc-2 - loc
    loc-3 - loc
    paper-0 - paper
  )
  (:init
    (at loc-1)
    (ishomebase loc-1)
    (safe loc-0)
    (safe loc-1)
    (satisfied loc-1)
    (unpacked paper-0)
    (wantspaper loc-0)
  )
  (:goal (and (satisfied loc-0)))
)
