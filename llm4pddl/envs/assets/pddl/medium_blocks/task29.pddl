(define (problem task29) (:domain medium_blocks)
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
    (clear b5)
    (clear b8)
    (clear b9)
    (handempty)
    (on b2 b1)
    (on b3 b2)
    (on b4 b3)
    (on b5 b4)
    (on b7 b6)
    (on b8 b7)
    (ontable b0)
    (ontable b1)
    (ontable b6)
    (ontable b9)
  )
  (:goal (and (on b0 b5)
    (on b2 b7)
    (on b6 b9)
    (on b7 b8)
    (on b9 b4)
    (ontable b3)
    (ontable b4)
    (ontable b5)
    (ontable b8)))
)
