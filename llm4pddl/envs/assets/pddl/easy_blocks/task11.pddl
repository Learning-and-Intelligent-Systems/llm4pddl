(define (problem task11) (:domain easy_blocks)
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
    (clear b2)
    (clear b3)
    (clear b4)
    (handempty)
    (ontable b0)
    (ontable b1)
    (ontable b2)
    (ontable b3)
    (ontable b4)
  )
  (:goal (and (on b0 b3)
    (ontable b1)
    (ontable b2)
    (ontable b3)
    (ontable b4)))
)
