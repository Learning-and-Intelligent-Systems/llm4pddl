(define (problem task23) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )
  (:init
    (clear b0)
    (clear b1)
    (clear b4)
    (handempty)
    (on b3 b2)
    (on b4 b3)
    (ontable b0)
    (ontable b1)
    (ontable b2)
  )
  (:goal (and (ontable b1)
    (ontable b2)
    (ontable b3)))
)
