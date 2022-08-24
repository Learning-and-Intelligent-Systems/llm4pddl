(define (problem blocks-4-2)
  (:domain blocks)
  (:objects
    b - block
    c - block
  )
  (:init
    (clear c)
    (ontable b)
    (on c b)
    (handempty)
  )
  (:goal (and (on b c)))
)
