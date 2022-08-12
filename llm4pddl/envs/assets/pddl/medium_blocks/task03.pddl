(define (problem task3) (:domain medium_blocks)
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
    (clear b2)
    (clear b6)
    (handempty)
    (on b1 b0)
    (on b4 b3)
    (on b5 b4)
    (on b6 b5)
    (ontable b0)
    (ontable b2)
    (ontable b3)
  )
  (:goal (and (on b0 b5)
    (on b5 b1)
    (ontable b1)
    (ontable b2)
    (ontable b3)
    (ontable b6)))
)
