(define (problem task9) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )
  (:init
    (clear b2)
    (clear b3)
    (clear b4)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (ontable b0)
    (ontable b3)
    (ontable b4)
  )
  (:goal (and (ontable b2)
    (ontable b4)))
)
