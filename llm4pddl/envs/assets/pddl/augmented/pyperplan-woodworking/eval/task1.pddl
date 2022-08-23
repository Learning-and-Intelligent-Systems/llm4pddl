; woodworking task with 4 parts and 140% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 196950

(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    grinder0 - grinder
    glazer0 - glazer
    immersion-varnisher0 - immersion-varnisher
    planer0 - planer
    highspeed-saw0 - highspeed-saw
    spray-varnisher0 - spray-varnisher
    saw0 - saw
    green white mauve - acolour
    cherry beech - awood
    p0 p1 p2 p3 - part
    b0 - board
    s0 s1 s2 s3 s4 s5 - aboardsize
  )
  (:init
    (grind-treatment-change varnished colourfragments)
    (grind-treatment-change glazed untreated)
    (grind-treatment-change untreated untreated)
    (grind-treatment-change colourfragments untreated)
    (is-smooth smooth)
    (is-smooth verysmooth)
    
    (boardsize-successor s0 s1)
    (boardsize-successor s1 s2)
    (boardsize-successor s2 s3)
    (boardsize-successor s3 s4)
    (boardsize-successor s4 s5)
    (has-colour glazer0 mauve)
    (has-colour glazer0 white)
    (has-colour immersion-varnisher0 mauve)
    (has-colour immersion-varnisher0 white)
    (has-colour immersion-varnisher0 natural)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 mauve)
    (has-colour spray-varnisher0 white)
    (has-colour spray-varnisher0 natural)
    (available p0)
    (colour p0 natural)
    (wood p0 cherry)
    (surface-condition p0 rough)
    (treatment p0 varnished)
    (goalsize p0 medium)
    
    
    
    
    (available p1)
    (colour p1 green)
    (wood p1 cherry)
    (surface-condition p1 rough)
    (treatment p1 colourfragments)
    (goalsize p1 large)
    
    
    
    
    (available p2)
    (colour p2 white)
    (wood p2 cherry)
    (surface-condition p2 verysmooth)
    (treatment p2 glazed)
    (goalsize p2 small)
    
    
    
    
    (unused p3)
    (goalsize p3 large)
    
    
    
    
    (boardsize b0 s5)
    (wood b0 beech)
    (surface-condition b0 rough)
    (available b0)
  )
  (:goal
    (and
      (available p0)
      (colour p0 mauve)
      (wood p0 cherry)
      (surface-condition p0 smooth)
      (treatment p0 glazed)
      (available p1)
      (colour p1 natural)
      (wood p1 cherry)
      (surface-condition p1 verysmooth)
      (treatment p1 varnished)
      (available p2)
      (colour p2 mauve)
      (surface-condition p2 smooth)
      (available p3)
      (colour p3 white)
      (wood p3 beech)
    )
  )
  
)
