(define (problem blocks-4-0)
  (:domain blocks)
  (:objects
    b - block
    c - block
    d - block
  )
  (:init
    (clear c)
    (clear b)
    (clear d)
    (ontable c)
    (ontable d)
    (handempty)
  )
  (:goal (and (on d c) (on c b)))
)
