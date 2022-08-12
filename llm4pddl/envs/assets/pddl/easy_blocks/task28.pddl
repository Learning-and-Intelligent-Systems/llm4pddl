(define (problem task28) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
  )
  (:init
    (clear b2)
    (clear b5)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (on b4 b3)
    (on b5 b4)
    (ontable b0)
    (ontable b3)
  )
  (:goal (and (on b5 b0)
    (ontable b0)
    (ontable b4)))
)
