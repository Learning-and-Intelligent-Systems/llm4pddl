(define (problem task19) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
  )
  (:init
    (clear b1)
    (clear b3)
    (clear b5)
    (handempty)
    (on b1 b0)
    (on b3 b2)
    (on b5 b4)
    (ontable b0)
    (ontable b2)
    (ontable b4)
  )
  (:goal (and (on b0 b4)
    (on b1 b0)
    (ontable b4)))
)
