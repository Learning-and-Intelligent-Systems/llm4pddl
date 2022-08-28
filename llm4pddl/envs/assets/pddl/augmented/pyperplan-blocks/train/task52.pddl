(define (problem blocks-5-0)
  (:domain blocks)
  (:objects
    a - block
    b - block
    c - block
    e - block
  )
  (:init
    (clear c)
    (ontable a)
    (on c e)
    (on e b)
    (on b a)
    (handempty)
  )
  (:goal (and (on a e) (on e b)))
)
