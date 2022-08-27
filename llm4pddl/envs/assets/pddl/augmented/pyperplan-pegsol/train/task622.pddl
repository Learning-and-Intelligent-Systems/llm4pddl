(define (problem pegsolitaire-sequential-014)
  (:domain pegsolitaire-sequential)
  (:objects
    pos-3-2 - location
    pos-3-3 - location
    pos-3-4 - location
  )
  (:init
    (move-ended)
    (in-line pos-3-2 pos-3-3 pos-3-4)
    (free pos-3-4)
    (occupied pos-3-2)
    (occupied pos-3-3)
  )
  (:goal (and (free pos-3-2)))
)
