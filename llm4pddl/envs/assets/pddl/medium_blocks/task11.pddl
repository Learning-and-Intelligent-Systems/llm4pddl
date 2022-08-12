(define (problem task11) (:domain medium_blocks)
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
    (clear b2)
    (clear b3)
    (clear b4)
    (clear b7)
    (clear b9)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (on b6 b5)
    (on b7 b6)
    (on b9 b8)
    (ontable b0)
    (ontable b3)
    (ontable b4)
    (ontable b5)
    (ontable b8)
  )
  (:goal (and (on b0 b7)
    (on b1 b3)
    (on b2 b0)
    (on b6 b2)
    (on b7 b1)
    (on b8 b4)
    (ontable b3)
    (ontable b4)))
)
