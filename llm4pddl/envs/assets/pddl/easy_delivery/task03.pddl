(define (problem task3) (:domain easy_delivery)
  (:objects
    loc-0 - loc
    loc-1 - loc
    loc-2 - loc
    paper-0 - paper
  )
  (:init
    (at loc-2)
    (ishomebase loc-2)
    (safe loc-1)
    (safe loc-2)
    (satisfied loc-2)
    (unpacked paper-0)
    (wantspaper loc-1)
  )
  (:goal (and (satisfied loc-1)))
)
