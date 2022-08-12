(define (problem task23) (:domain medium_blocks)
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
    (clear b1)
    (clear b3)
    (clear b4)
    (clear b5)
    (clear b9)
    (handempty)
    (on b1 b0)
    (on b3 b2)
    (on b7 b6)
    (on b8 b7)
    (on b9 b8)
    (ontable b0)
    (ontable b2)
    (ontable b4)
    (ontable b5)
    (ontable b6)
  )
  (:goal (and (ontable b0)
    (ontable b3)
    (ontable b4)
    (ontable b5)
    (ontable b6)
    (ontable b7)
    (ontable b9)))
)
