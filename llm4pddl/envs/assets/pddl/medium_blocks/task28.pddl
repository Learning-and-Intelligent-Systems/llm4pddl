(define (problem task28) (:domain medium_blocks)
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
    (clear b4)
    (clear b5)
    (clear b7)
    (clear b8)
    (clear b9)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (on b3 b2)
    (on b4 b3)
    (on b7 b6)
    (ontable b0)
    (ontable b5)
    (ontable b6)
    (ontable b8)
    (ontable b9)
  )
  (:goal (and (on b0 b6)
    (on b1 b9)
    (on b7 b0)
    (on b8 b1)
    (ontable b2)
    (ontable b3)
    (ontable b5)
    (ontable b6)
    (ontable b9)))
)
