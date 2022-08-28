(define (problem blocks-4-0)
  (:domain blocks)
  (:objects
    a - block
    b - block
    c - block
  )
  (:init
    (clear c)
    (clear a)
    (clear b)
    (ontable c)
    (ontable b)
    (handempty)
  )
  (:goal (and (on c b) (on b a)))
)
