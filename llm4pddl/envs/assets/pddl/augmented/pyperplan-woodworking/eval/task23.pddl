; woodworking task with 11 parts and 140% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 919452

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
    mauve white black red blue green - acolour
    pine oak mahogany - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 - part
    b0 b1 b2 - board
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
    (has-colour glazer0 white)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 mauve)
    (has-colour immersion-varnisher0 natural)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 mauve)
    (has-colour spray-varnisher0 natural)
    (has-colour spray-varnisher0 red)
    (available p0)
    (colour p0 green)
    (wood p0 mahogany)
    (surface-condition p0 smooth)
    (treatment p0 varnished)
    (goalsize p0 small)
    
    
    
    
    (available p1)
    (colour p1 green)
    (wood p1 pine)
    (surface-condition p1 smooth)
    (treatment p1 colourfragments)
    (goalsize p1 small)
    
    
    
    
    (available p2)
    (colour p2 red)
    (wood p2 pine)
    (surface-condition p2 rough)
    (treatment p2 varnished)
    (goalsize p2 medium)
    
    
    
    
    (unused p3)
    (goalsize p3 small)
    
    
    
    
    (unused p4)
    (goalsize p4 medium)
    
    
    
    
    (available p5)
    (colour p5 blue)
    (wood p5 oak)
    (surface-condition p5 smooth)
    (treatment p5 colourfragments)
    (goalsize p5 medium)
    
    
    
    
    (available p6)
    (colour p6 green)
    (wood p6 oak)
    (surface-condition p6 verysmooth)
    (treatment p6 glazed)
    (goalsize p6 medium)
    
    
    
    
    (available p7)
    (colour p7 black)
    (wood p7 oak)
    (surface-condition p7 verysmooth)
    (treatment p7 colourfragments)
    (goalsize p7 medium)
    
    
    
    
    (unused p8)
    (goalsize p8 large)
    
    
    
    
    (unused p9)
    (goalsize p9 large)
    
    
    
    
    (available p10)
    (colour p10 white)
    (wood p10 pine)
    (surface-condition p10 rough)
    (treatment p10 varnished)
    (goalsize p10 small)
    
    
    
    
    (boardsize b0 s5)
    (wood b0 mahogany)
    (surface-condition b0 smooth)
    (available b0)
    (boardsize b1 s5)
    (wood b1 oak)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s5)
    (wood b2 pine)
    (surface-condition b2 rough)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (colour p0 white)
      (wood p0 mahogany)
      (surface-condition p0 verysmooth)
      (treatment p0 glazed)
      (available p1)
      (colour p1 natural)
      (wood p1 pine)
      (surface-condition p1 verysmooth)
      (treatment p1 varnished)
      (available p2)
      (colour p2 blue)
      (wood p2 pine)
      (surface-condition p2 verysmooth)
      (treatment p2 varnished)
      (available p3)
      (wood p3 mahogany)
      (surface-condition p3 smooth)
      (treatment p3 varnished)
      (available p4)
      (wood p4 mahogany)
      (treatment p4 varnished)
      (available p5)
      (wood p5 oak)
      (surface-condition p5 verysmooth)
      (treatment p5 varnished)
      (available p6)
      (colour p6 red)
      (wood p6 oak)
      (treatment p6 varnished)
      (available p7)
      (wood p7 oak)
      (treatment p7 varnished)
      (available p8)
      (colour p8 natural)
      (wood p8 pine)
      (surface-condition p8 verysmooth)
      (treatment p8 varnished)
      (available p9)
      (colour p9 natural)
      (treatment p9 varnished)
      (available p10)
      (colour p10 mauve)
      (wood p10 pine)
      (surface-condition p10 verysmooth)
      (treatment p10 varnished)
    )
  )
  
)
