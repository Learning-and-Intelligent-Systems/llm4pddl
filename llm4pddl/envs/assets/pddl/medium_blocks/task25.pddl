(define (problem task25) (:domain medium_blocks)
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
    (clear b3)
    (clear b6)
    (clear b8)
    (clear b9)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (on b3 b2)
    (on b5 b4)
    (on b6 b5)
    (on b8 b7)
    (ontable b0)
    (ontable b4)
    (ontable b7)
    (ontable b9)
  )
  (:goal (and (on b0 b6)
    (on b1 b8)
    (on b3 b0)
    (ontable b4)
    (ontable b6)
    (ontable b8)))
)
