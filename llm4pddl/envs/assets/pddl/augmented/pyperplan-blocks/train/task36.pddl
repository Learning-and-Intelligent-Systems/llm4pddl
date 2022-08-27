(define (problem blocks-5-2)
  (:domain blocks)
  (:objects
    c - block
    d - block
    e - block
  )
  (:init
    (clear d)
    (on d e)
    (on e c)
    (handempty)
  )
  (:goal (and (on d c)))
)
