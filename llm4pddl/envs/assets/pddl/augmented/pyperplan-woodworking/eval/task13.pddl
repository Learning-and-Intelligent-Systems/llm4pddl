; woodworking task with 8 parts and 120% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 44688

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
    blue green black red white mauve - acolour
    cherry walnut - awood
    p0 p1 p2 p3 p4 p5 p6 p7 - part
    b0 b1 - board
    s0 s1 s2 s3 s4 s5 s6 - aboardsize
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
    (has-colour glazer0 blue)
    (has-colour glazer0 mauve)
    (has-colour glazer0 black)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 mauve)
    (has-colour immersion-varnisher0 green)
    (has-colour immersion-varnisher0 black)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 mauve)
    (has-colour spray-varnisher0 green)
    (has-colour spray-varnisher0 black)
    (unused p0)
    (goalsize p0 medium)
    
    
    
    
    (unused p1)
    (goalsize p1 small)
    
    
    
    
    (unused p2)
    (goalsize p2 large)
    
    
    
    
    (unused p3)
    (goalsize p3 medium)
    
    
    
    
    (available p4)
    (colour p4 black)
    (wood p4 cherry)
    (surface-condition p4 rough)
    (treatment p4 varnished)
    (goalsize p4 medium)
    
    
    
    
    (available p5)
    (colour p5 green)
    (wood p5 cherry)
    (surface-condition p5 smooth)
    (treatment p5 colourfragments)
    (goalsize p5 medium)
    
    
    
    
    (unused p6)
    (goalsize p6 small)
    
    
    
    
    (available p7)
    (colour p7 black)
    (wood p7 walnut)
    (surface-condition p7 rough)
    (treatment p7 varnished)
    (goalsize p7 large)
    
    
    
    
    (boardsize b0 s5)
    (wood b0 cherry)
    (surface-condition b0 smooth)
    (available b0)
    (boardsize b1 s6)
    (wood b1 walnut)
    (surface-condition b1 rough)
    (available b1)
  )
  (:goal
    (and
      (available p0)
      (colour p0 black)
      (wood p0 walnut)
      (available p1)
      (colour p1 blue)
      (wood p1 cherry)
      (available p2)
      (wood p2 walnut)
      (surface-condition p2 smooth)
      (available p3)
      (colour p3 blue)
      (wood p3 cherry)
      (surface-condition p3 verysmooth)
      (treatment p3 varnished)
      (available p4)
      (colour p4 mauve)
      (surface-condition p4 smooth)
      (available p5)
      (wood p5 cherry)
      (surface-condition p5 smooth)
      (treatment p5 varnished)
      (available p6)
      (colour p6 green)
      (treatment p6 varnished)
      (available p7)
      (wood p7 walnut)
      (surface-condition p7 smooth)
      (treatment p7 varnished)
    )
  )
  
)
