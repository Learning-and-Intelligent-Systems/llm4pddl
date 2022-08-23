(define (problem blocks-4-1)
  (:domain blocks)
  (:objects
    a - block
    b - block
    c - block
    d - block
  )
  (:init
    (clear b)
    (on b c)
    (on c a)
    (on a d)
    (handempty)
  )
  (:goal (and (on c a) (on a b)))
)
