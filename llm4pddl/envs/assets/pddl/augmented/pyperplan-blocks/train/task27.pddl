(define (problem blocks-4-0)
  (:domain blocks)
  (:objects
    c - block
    d - block
  )
  (:init
    (clear c)
    (clear d)
    (ontable d)
    (handempty)
  )
  (:goal (and (on d c)))
)
