(define (problem blocks-5-0)
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
    (clear c)
    (on c e)
    (on e b)
    (on b a)
    (handempty)
  )
  (:goal (and (on e b) (on b d)))
)
