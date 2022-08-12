(define (problem task7) (:domain easy_blocks)
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
    (clear b4)
    (clear b5)
    (handempty)
    (on b1 b0)
    (on b3 b2)
    (on b4 b3)
    (ontable b0)
    (ontable b2)
    (ontable b5)
  )
  (:goal (and (on b1 b4)
    (on b4 b2)
    (on b5 b1)
    (ontable b2)
    (ontable b3)))
)
