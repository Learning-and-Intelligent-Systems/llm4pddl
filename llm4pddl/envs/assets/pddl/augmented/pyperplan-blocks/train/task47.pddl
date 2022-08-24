(define (problem blocks-5-0)
  (:domain blocks)
  (:objects
    b - block
    c - block
    d - block
    e - block
  )
  (:init
    (clear d)
    (clear c)
    (ontable d)
    (on e b)
    (handempty)
  )
  (:goal (and (on e b) (on d c)))
)
