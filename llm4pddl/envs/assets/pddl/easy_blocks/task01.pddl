(define (problem task1) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
  )
  (:init
    (clear b2)
    (handempty)
    (on b1 b0)
    (on b2 b1)
    (ontable b0)
  )
  (:goal (and (ontable b0)
    (ontable b1)))
)
