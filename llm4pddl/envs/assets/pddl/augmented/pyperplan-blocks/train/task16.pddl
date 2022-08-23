(define (problem blocks-5-2)
  (:domain blocks)
  (:objects
    a - block
    c - block
    d - block
    e - block
  )
  (:init
    (clear d)
    (on d e)
    (on e c)
    (on c a)
    (handempty)
  )
  (:goal (and (on d c) (on e a)))
)
