; woodworking task with 8 parts and 140% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 592815

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
    mauve green blue black red white - acolour
    oak cherry - awood
    p0 p1 p2 p3 p4 p5 p6 p7 - part
    b0 b1 b2 - board
    s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 - aboardsize
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
    (boardsize-successor s5 s6)
    (boardsize-successor s6 s7)
    (boardsize-successor s7 s8)
    (boardsize-successor s8 s9)
    (has-colour glazer0 natural)
    (has-colour glazer0 white)
    (has-colour glazer0 black)
    (has-colour immersion-varnisher0 natural)
    (has-colour immersion-varnisher0 black)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 natural)
    (has-colour spray-varnisher0 black)
    (unused p0)
    (goalsize p0 large)
    
    
    
    
    (unused p1)
    (goalsize p1 medium)
    
    
    
    
    (unused p2)
    (goalsize p2 large)
    
    
    
    
    (unused p3)
    (goalsize p3 medium)
    
    
    
    
    (unused p4)
    (goalsize p4 large)
    
    
    
    
    (unused p5)
    (goalsize p5 small)
    
    
    
    
    (available p6)
    (colour p6 blue)
    (wood p6 cherry)
    (surface-condition p6 verysmooth)
    (treatment p6 colourfragments)
    (goalsize p6 medium)
    
    
    
    
    (available p7)
    (colour p7 white)
    (wood p7 oak)
    (surface-condition p7 smooth)
    (treatment p7 varnished)
    (goalsize p7 medium)
    
    
    
    
    (boardsize b0 s3)
    (wood b0 cherry)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s9)
    (wood b1 oak)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s8)
    (wood b2 oak)
    (surface-condition b2 rough)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (wood p0 oak)
      (treatment p0 varnished)
      (available p1)
      (colour p1 natural)
      (surface-condition p1 verysmooth)
      (available p2)
      (wood p2 oak)
      (surface-condition p2 verysmooth)
      (available p3)
      (colour p3 black)
      (wood p3 oak)
      (available p4)
      (colour p4 white)
      (wood p4 oak)
      (surface-condition p4 smooth)
      (treatment p4 glazed)
      (available p5)
      (wood p5 oak)
      (surface-condition p5 smooth)
      (available p6)
      (wood p6 cherry)
      (surface-condition p6 smooth)
      (treatment p6 glazed)
      (available p7)
      (surface-condition p7 verysmooth)
      (treatment p7 glazed)
    )
  )
  
)
