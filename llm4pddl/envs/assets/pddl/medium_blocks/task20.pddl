(define (problem task20) (:domain medium_blocks)
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
    (clear b1)
    (clear b2)
    (clear b4)
    (clear b6)
    (clear b7)
    (clear b8)
    (handempty)
    (on b1 b0)
    (on b4 b3)
    (on b6 b5)
    (ontable b0)
    (ontable b2)
    (ontable b3)
    (ontable b5)
    (ontable b7)
    (ontable b8)
  )
  (:goal (and (on b0 b1)
    (on b1 b3)
    (on b2 b0)
    (on b4 b6)
    (on b6 b2)
    (ontable b3)
    (ontable b7)
    (ontable b8)))
)
