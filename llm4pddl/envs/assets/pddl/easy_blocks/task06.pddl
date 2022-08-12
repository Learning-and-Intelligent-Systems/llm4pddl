(define (problem task6) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
  )
  (:init
    (clear b0)
    (clear b2)
    (clear b3)
    (clear b5)
    (handempty)
    (on b2 b1)
    (on b5 b4)
    (ontable b0)
    (ontable b1)
    (ontable b3)
    (ontable b4)
  )
  (:goal (and (ontable b2)
    (ontable b3)
    (ontable b4)))
)
