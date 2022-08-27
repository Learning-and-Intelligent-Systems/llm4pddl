(define (problem blocks-5-0)
  (:domain blocks)
  (:objects
    c - block
    d - block
  )
  (:init
    (clear d)
    (clear c)
    (ontable d)
    (handempty)
  )
  (:goal (and (on d c)))
)
