(define (problem task4) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
  )
  (:init
    (clear b0)
    (clear b2)
    (handempty)
    (on b2 b1)
    (ontable b0)
    (ontable b1)
  )
  (:goal (and (on b1 b0)
    (on b2 b1)
    (ontable b0)))
)
