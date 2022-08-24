(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    b0 - board
    oak - awood
    p0 - part
    s3 - aboardsize
    s4 - aboardsize
    saw0 - saw
    spray-varnisher0 - spray-varnisher
  )
  (:init
    (is-smooth smooth)
    (boardsize-successor s3 s4)
    (has-colour spray-varnisher0 natural)
    (unused p0)
    (goalsize p0 small)
    (boardsize b0 s4)
    (wood b0 oak)
    (surface-condition b0 smooth)
    (available b0)
  )
  (:goal (and (treatment p0 varnished)))
)
