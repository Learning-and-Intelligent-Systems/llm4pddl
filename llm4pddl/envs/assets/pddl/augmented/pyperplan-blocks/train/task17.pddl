(define (problem blocks-4-2)
  (:domain blocks)
  (:objects
    a - block
    b - block
    c - block
    d - block
  )
  (:init
    (clear a)
    (clear c)
    (clear d)
    (ontable a)
    (on c b)
    (handempty)
  )
  (:goal (and (on a b) (on c d)))
)
