(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    b0 - board
    oak - awood
    p0 - part
    s3 - aboardsize
    s4 - aboardsize
    saw0 - saw
  )
  (:init
    (boardsize-successor s3 s4)
    (unused p0)
    (goalsize p0 small)
    (boardsize b0 s4)
    (wood b0 oak)
    (surface-condition b0 smooth)
    (available b0)
  )
  (:goal (and (available p0)))
)
