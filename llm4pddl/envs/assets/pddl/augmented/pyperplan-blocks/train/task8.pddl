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
    (ontable d)
    (on b c)
    (on c a)
    (on a d)
    (handempty)
  )
  (:goal (and (on d c) (on a b)))
)
