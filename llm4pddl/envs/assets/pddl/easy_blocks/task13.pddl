(define (problem task13) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )
  (:init
    (clear b2)
    (clear b4)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (on b4 b3)
    (ontable b0)
    (ontable b3)
  )
  (:goal (and (on b1 b2)
    (on b2 b4)
    (on b4 b3)
    (ontable b0)
    (ontable b3)))
)
