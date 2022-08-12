(define (problem task10) (:domain medium_blocks)
  (:objects
    b0 - block
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
    b7 - block
    b8 - block
  )
  (:init
    (clear b0)
    (clear b3)
    (clear b5)
    (clear b6)
    (clear b7)
    (clear b8)
    (handempty)
    (on b2 b1)
    (on b3 b2)
    (on b5 b4)
    (ontable b0)
    (ontable b1)
    (ontable b4)
    (ontable b6)
    (ontable b7)
    (ontable b8)
  )
  (:goal (and (on b2 b7)
    (on b3 b0)
    (ontable b0)
    (ontable b1)
    (ontable b5)
    (ontable b6)
    (ontable b7)
    (ontable b8)))
)
