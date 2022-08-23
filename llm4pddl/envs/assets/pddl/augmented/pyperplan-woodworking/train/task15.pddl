(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    b0 - board
    blue - acolour
    oak - awood
    p0 - part
    p1 - part
    p2 - part
    planer0 - planer
    red - acolour
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
    (has-colour spray-varnisher0 red)
    (unused p0)
    (goalsize p0 small)
    (available p1)
    (colour p1 blue)
    (surface-condition p1 rough)
    (treatment p1 varnished)
    (unused p2)
    (goalsize p2 large)
    (boardsize b0 s4)
    (wood b0 oak)
    (surface-condition b0 smooth)
    (available b0)
  )
  (:goal (and (available p0) (colour p0 natural) (treatment p0 varnished) (available p1) (surface-condition p1 smooth) (available p2) (colour p2 red) (wood p2 oak) (surface-condition p2 smooth) (treatment p2 varnished)))
)
