(define (problem task16) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )
  (:init
    (clear b1)
    (clear b4)
    (handempty)
    (on b1 b0)
    (on b3 b2)
    (on b4 b3)
    (ontable b0)
    (ontable b2)
  )
  (:goal (and (on b0 b1)
    (on b1 b4)
    (on b4 b3)
    (ontable b2)
    (ontable b3)))
)
