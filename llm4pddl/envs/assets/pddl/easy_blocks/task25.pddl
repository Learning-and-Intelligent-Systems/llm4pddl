(define (problem task25) (:domain easy_blocks)
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
    (clear b1)
    (clear b3)
    (clear b5)
    (handempty)
    (on b3 b2)
    (on b5 b4)
    (ontable b0)
    (ontable b1)
    (ontable b2)
    (ontable b4)
  )
  (:goal (and (on b2 b1)
    (ontable b1)))
)
