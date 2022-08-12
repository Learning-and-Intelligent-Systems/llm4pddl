(define (problem task5) (:domain easy_blocks)
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
  (:goal (and (on b1 b2)
    (ontable b0)
    (ontable b2)))
)
