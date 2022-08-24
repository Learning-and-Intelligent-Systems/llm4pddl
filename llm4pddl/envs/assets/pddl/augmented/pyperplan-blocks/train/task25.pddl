(define (problem blocks-4-0)
  (:domain blocks)
  (:objects
    a - block
    b - block
  )
  (:init
    (clear a)
    (clear b)
    (ontable b)
    (handempty)
  )
  (:goal (and (on b a)))
)
