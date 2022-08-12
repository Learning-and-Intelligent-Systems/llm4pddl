(define (problem task8) (:domain medium_blocks)
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
    (clear b0)
    (clear b1)
    (clear b2)
    (clear b4)
    (clear b6)
    (clear b7)
    (clear b8)
    (clear b9)
    (handempty)
    (on b4 b3)
    (on b6 b5)
    (ontable b0)
    (ontable b1)
    (ontable b2)
    (ontable b3)
    (ontable b5)
    (ontable b7)
    (ontable b8)
    (ontable b9)
  )
  (:goal (and (on b4 b2)
    (on b5 b7)
    (on b7 b4)
    (ontable b1)
    (ontable b2)
    (ontable b6)
    (ontable b9)))
)
