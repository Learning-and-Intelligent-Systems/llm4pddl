(define (problem task13) (:domain medium_blocks)
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
    b9 - block
  )
  (:init
    (clear b5)
    (clear b6)
    (clear b9)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (on b3 b2)
    (on b4 b3)
    (on b5 b4)
    (on b8 b7)
    (on b9 b8)
    (ontable b0)
    (ontable b6)
    (ontable b7)
  )
  (:goal (and (on b4 b8)
    (on b6 b2)
    (on b9 b4)
    (ontable b0)
    (ontable b1)
    (ontable b2)
    (ontable b8)))
)
