(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    b0 - board
    b1 - board
    blue - acolour
    glazer0 - glazer
    oak - awood
    p0 - part
    p1 - part
    p2 - part
    planer0 - planer
    red - acolour
    s1 - aboardsize
    s2 - aboardsize
    s3 - aboardsize
    saw0 - saw
    spray-varnisher0 - spray-varnisher
    teak - awood
  )
  (:init
    (is-smooth smooth)
    (boardsize-successor s1 s2)
    (boardsize-successor s2 s3)
    (has-colour glazer0 blue)
    (has-colour spray-varnisher0 natural)
    (unused p0)
    (goalsize p0 small)
    (unused p1)
    (goalsize p1 medium)
    (available p2)
    (colour p2 red)
    (wood p2 teak)
    (surface-condition p2 verysmooth)
    (treatment p2 varnished)
    (boardsize b0 s2)
    (wood b0 teak)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s3)
    (wood b1 oak)
    (surface-condition b1 rough)
    (available b1)
  )
  (:goal (and (available p0) (wood p0 teak) (surface-condition p0 smooth) (treatment p0 varnished) (available p1) (colour p1 blue) (wood p1 oak) (surface-condition p1 smooth) (treatment p1 glazed) (available p2) (colour p2 natural) (wood p2 teak) (surface-condition p2 smooth)))
)
