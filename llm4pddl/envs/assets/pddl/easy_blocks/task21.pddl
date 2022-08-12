(define (problem task21) (:domain easy_blocks)
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
    (clear b3)
    (clear b4)
    (clear b5)
    (handempty)
    (on b2 b1)
    (on b3 b2)
    (ontable b0)
    (ontable b1)
    (ontable b4)
    (ontable b5)
  )
  (:goal (and (on b3 b5)
    (ontable b0)
    (ontable b1)
    (ontable b4)
    (ontable b5)))
)
