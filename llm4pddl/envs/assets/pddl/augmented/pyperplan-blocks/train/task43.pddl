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
    (ontable d)
    (ontable a)
    (on c e)
    (on e b)
    (on b a)
    (handempty)
  )
  (:goal (and (on a e) (on b d) (on d c)))
)
