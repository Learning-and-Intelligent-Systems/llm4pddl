(define (problem task4) (:domain medium_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
  )
  (:init
    (clear b1)
    (clear b5)
    (clear b6)
    (handempty)
    (on b1 b0)
    (on b3 b2)
    (on b4 b3)
    (on b5 b4)
    (ontable b0)
    (ontable b2)
    (ontable b6)
  )
  (:goal (and (on b4 b2)
    (on b6 b0)
    (ontable b0)
    (ontable b1)
    (ontable b2)
    (ontable b3)))
)
