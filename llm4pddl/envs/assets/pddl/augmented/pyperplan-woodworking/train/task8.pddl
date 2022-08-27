(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    b0 - board
    b1 - board
    beech - awood
    cherry - awood
    glazer0 - glazer
    green - acolour
    grinder0 - grinder
    mauve - acolour
    p0 - part
    p1 - part
    p2 - part
    planer0 - planer
    s1 - aboardsize
    s2 - aboardsize
    s3 - aboardsize
    saw0 - saw
    spray-varnisher0 - spray-varnisher
  )
  (:init
    (grind-treatment-change untreated untreated)
    (is-smooth smooth)
    (is-smooth verysmooth)
    (boardsize-successor s1 s2)
    (boardsize-successor s2 s3)
    (has-colour glazer0 green)
    (has-colour spray-varnisher0 mauve)
    (unused p0)
    (goalsize p0 medium)
    (unused p1)
    (goalsize p1 medium)
    (available p2)
    (colour p2 natural)
    (wood p2 beech)
    (surface-condition p2 verysmooth)
    (treatment p2 colourfragments)
    (boardsize b0 s3)
    (wood b0 beech)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s3)
    (wood b1 cherry)
    (surface-condition b1 rough)
    (available b1)
  )
  (:goal (and (available p0) (colour p0 mauve) (wood p0 beech) (surface-condition p0 verysmooth) (treatment p0 varnished) (available p1) (colour p1 green) (wood p1 cherry) (surface-condition p1 smooth) (treatment p1 glazed) (available p2) (colour p2 mauve) (wood p2 beech)))
)
