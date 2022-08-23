(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    b0 - board
    oak - awood
    p0 - part
    p1 - part
    p2 - part
    s1 - aboardsize
    s2 - aboardsize
    s3 - aboardsize
    s4 - aboardsize
    saw0 - saw
    spray-varnisher0 - spray-varnisher
  )
  (:init
    (is-smooth smooth)
    (boardsize-successor s1 s2)
    (boardsize-successor s2 s3)
    (boardsize-successor s3 s4)
    (has-colour spray-varnisher0 natural)
    (unused p0)
    (goalsize p0 small)
    (wood p1 oak)
    (unused p2)
    (goalsize p2 large)
    (boardsize b0 s4)
    (wood b0 oak)
    (surface-condition b0 smooth)
    (available b0)
  )
  (:goal (and (available p0) (colour p0 natural) (treatment p0 varnished) (wood p1 oak) (available p2) (wood p2 oak) (surface-condition p2 smooth)))
)
