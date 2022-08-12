(define (problem task18) (:domain medium_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
    b7 - block
    b8 - block
  )
  (:init
    (clear b2)
    (clear b4)
    (clear b5)
    (clear b6)
    (clear b7)
    (clear b8)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (on b4 b3)
    (ontable b0)
    (ontable b3)
    (ontable b5)
    (ontable b6)
    (ontable b7)
    (ontable b8)
  )
  (:goal (and (on b3 b6)
    (on b5 b7)
    (ontable b0)
    (ontable b4)
    (ontable b6)
    (ontable b7)))
)
