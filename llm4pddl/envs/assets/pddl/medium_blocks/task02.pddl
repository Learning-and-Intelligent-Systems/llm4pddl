(define (problem task2) (:domain medium_blocks)
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
    (clear b4)
    (clear b5)
    (clear b6)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (on b3 b2)
    (on b4 b3)
    (ontable b0)
    (ontable b5)
    (ontable b6)
  )
  (:goal (and (on b0 b6)
    (on b3 b2)
    (on b5 b3)
    (on b6 b4)
    (ontable b2)
    (ontable b4)))
)
