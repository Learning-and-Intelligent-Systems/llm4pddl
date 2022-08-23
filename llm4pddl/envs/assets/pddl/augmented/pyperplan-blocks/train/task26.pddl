(define (problem blocks-4-0)
  (:domain blocks)
  (:objects
    b - block
    c - block
  )
  (:init
    (clear c)
    (clear b)
    (ontable c)
    (handempty)
  )
  (:goal (and (on c b)))
)
