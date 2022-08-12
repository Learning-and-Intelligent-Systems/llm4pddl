(define (problem task18) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )
  (:init
    (clear b0)
    (clear b2)
    (clear b4)
    (handempty)
    (on b2 b1)
    (on b4 b3)
    (ontable b0)
    (ontable b1)
    (ontable b3)
  )
  (:goal (and (on b0 b3)
    (on b3 b4)
    (ontable b1)
    (ontable b2)
    (ontable b4)))
)
