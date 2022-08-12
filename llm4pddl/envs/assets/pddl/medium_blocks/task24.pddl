(define (problem task24) (:domain medium_blocks)
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
    (clear b7)
    (clear b8)
    (clear b9)
    (handempty)
    (on b1 b0)
    (on b3 b2)
    (on b6 b5)
    (on b7 b6)
    (ontable b0)
    (ontable b2)
    (ontable b4)
    (ontable b5)
    (ontable b8)
    (ontable b9)
  )
  (:goal (and (on b1 b3)
    (on b5 b8)
    (on b6 b9)
    (on b8 b4)
    (on b9 b5)
    (ontable b0)
    (ontable b3)
    (ontable b4)
    (ontable b7)))
)
