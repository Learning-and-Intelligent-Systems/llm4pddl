(define (problem task16) (:domain medium_blocks)
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
    (clear b0)
    (clear b1)
    (clear b3)
    (clear b4)
    (clear b6)
    (clear b8)
    (handempty)
    (on b3 b2)
    (on b6 b5)
    (on b8 b7)
    (ontable b0)
    (ontable b1)
    (ontable b2)
    (ontable b4)
    (ontable b5)
    (ontable b7)
  )
  (:goal (and (on b2 b1)
    (on b6 b8)
    (on b7 b5)
    (ontable b1)
    (ontable b3)
    (ontable b4)
    (ontable b5)
    (ontable b8)))
)
