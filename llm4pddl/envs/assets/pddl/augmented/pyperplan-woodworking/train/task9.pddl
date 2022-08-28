(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    b0 - board
    b1 - board
    black - acolour
    mahogany - awood
    p0 - part
    p1 - part
    p2 - part
    p3 - part
    pine - awood
    planer0 - planer
    s2 - aboardsize
    s3 - aboardsize
    s4 - aboardsize
    s5 - aboardsize
    saw0 - saw
    spray-varnisher0 - spray-varnisher
  )
  (:init
    (is-smooth smooth)
    (boardsize-successor s2 s3)
    (boardsize-successor s3 s4)
    (boardsize-successor s4 s5)
    (has-colour spray-varnisher0 black)
    (unused p0)
    (goalsize p0 medium)
    (unused p1)
    (goalsize p1 large)
    (unused p2)
    (goalsize p2 medium)
    (unused p3)
    (goalsize p3 large)
    (boardsize b0 s5)
    (wood b0 mahogany)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s5)
    (wood b1 pine)
    (surface-condition b1 rough)
    (available b1)
  )
  (:goal (and (available p0) (colour p0 black) (wood p0 mahogany) (available p1) (wood p1 pine) (surface-condition p1 smooth) (available p2) (wood p2 pine) (treatment p2 varnished) (available p3) (colour p3 natural) (wood p3 mahogany)))
)
