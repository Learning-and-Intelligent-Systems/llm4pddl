(define (problem blocks-5-2)
  (:domain blocks)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
  )
  (:init
    (clear d)
    (ontable b)
    (on d e)
    (on e c)
    (on c a)
    (on a b)
    (handempty)
  )
  (:goal (and (on c b) (on b e)))
)
