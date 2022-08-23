(define (problem pegsolitaire-sequential-014)
  (:domain pegsolitaire-sequential)
  (:objects
    pos-2-4 - location
    pos-3-2 - location
    pos-3-3 - location
    pos-3-4 - location
    pos-4-3 - location
    pos-4-4 - location
    pos-4-5 - location
    pos-4-6 - location
    pos-5-2 - location
    pos-5-3 - location
    pos-5-4 - location
    pos-6-2 - location
    pos-6-3 - location
    pos-6-4 - location
  )
  (:init
    (move-ended)
    (in-line pos-2-4 pos-3-4 pos-4-4)
    (in-line pos-3-2 pos-3-3 pos-3-4)
    (in-line pos-5-3 pos-4-3 pos-3-3)
    (in-line pos-4-3 pos-4-4 pos-4-5)
    (in-line pos-4-5 pos-4-4 pos-4-3)
    (free pos-3-4)
    (free pos-4-5)
    (free pos-4-6)
    (free pos-5-2)
    (free pos-5-4)
    (free pos-6-2)
    (free pos-6-3)
    (free pos-6-4)
    (occupied pos-2-4)
    (occupied pos-3-2)
    (occupied pos-3-3)
    (occupied pos-4-3)
    (occupied pos-4-4)
    (occupied pos-5-3)
  )
  (:goal (and (free pos-3-2) (free pos-3-4) (free pos-4-3) (free pos-4-4) (free pos-4-5) (free pos-4-6) (free pos-5-2) (free pos-5-3) (free pos-5-4) (free pos-6-2) (free pos-6-3) (free pos-6-4) (occupied pos-3-3)))
)
