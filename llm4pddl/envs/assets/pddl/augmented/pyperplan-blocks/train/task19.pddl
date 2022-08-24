(define (problem blocks-4-2)
  (:domain blocks)
  (:objects
    b - block
    c - block
    d - block
  )
  (:init
    (clear c)
    (clear d)
    (on c b)
    (handempty)
  )
  (:goal (and (on c d)))
)
