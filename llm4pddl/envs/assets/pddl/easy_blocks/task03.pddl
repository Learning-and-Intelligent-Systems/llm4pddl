(define (problem task3) (:domain easy_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
  )
  (:init
    (clear b1)
    (clear b3)
    (handempty)
    (on b1 b0)
    (on b3 b2)
    (ontable b0)
    (ontable b2)
  )
  (:goal (and (ontable b0)
    (ontable b1)
    (ontable b3)))
)
