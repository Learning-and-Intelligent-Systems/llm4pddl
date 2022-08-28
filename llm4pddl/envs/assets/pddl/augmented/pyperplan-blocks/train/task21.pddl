(define (problem blocks-4-2)
  (:domain blocks)
  (:objects
    a - block
    b - block
    c - block
  )
  (:init
    (clear a)
    (clear c)
    (ontable a)
    (on c b)
    (handempty)
  )
  (:goal (and (on a b)))
)
