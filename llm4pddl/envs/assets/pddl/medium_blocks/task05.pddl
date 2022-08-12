(define (problem task5) (:domain medium_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
    b7 - block
  )
  (:init
    (clear b0)
    (clear b1)
    (clear b2)
    (clear b7)
    (handempty)
    (on b4 b3)
    (on b5 b4)
    (on b6 b5)
    (on b7 b6)
    (ontable b0)
    (ontable b1)
    (ontable b2)
    (ontable b3)
  )
  (:goal (and (on b0 b1)
    (ontable b1)
    (ontable b3)
    (ontable b4)
    (ontable b5)
    (ontable b6)))
)
