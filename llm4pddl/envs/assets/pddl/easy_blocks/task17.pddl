(define (problem task17) (:domain easy_blocks)
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
    (clear b2)
    (clear b3)
    (clear b5)
    (handempty)
    (on b1 b0)
    (on b5 b4)
    (ontable b0)
    (ontable b2)
    (ontable b3)
    (ontable b4)
  )
  (:goal (and (on b3 b4)
    (ontable b2)
    (ontable b4)
    (ontable b5)))
)
