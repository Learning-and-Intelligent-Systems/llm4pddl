; woodworking task with 10 parts and 100% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 443905

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
    white red blue mauve green black - acolour
    cherry mahogany oak - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 - part
    b0 b1 b2 b3 - board
    s0 s1 s2 s3 s4 s5 s6 s7 s8 - aboardsize
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
    (has-colour glazer0 blue)
    (has-colour glazer0 natural)
    (has-colour glazer0 green)
    (has-colour glazer0 mauve)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 natural)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 natural)
    (unused p0)
    (goalsize p0 large)
    
    
    
    
    (unused p1)
    (goalsize p1 large)
    
    
    
    
    (unused p2)
    (goalsize p2 large)
    
    
    
    
    (unused p3)
    (goalsize p3 large)
    
    
    
    
    (unused p4)
    (goalsize p4 medium)
    
    
    
    
    (unused p5)
    (goalsize p5 large)
    
    
    
    
    (unused p6)
    (goalsize p6 medium)
    
    
    
    
    (unused p7)
    (goalsize p7 medium)
    
    
    
    
    (unused p8)
    (goalsize p8 medium)
    
    
    
    
    (unused p9)
    (goalsize p9 medium)
    
    
    
    
    (boardsize b0 s8)
    (wood b0 cherry)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s7)
    (wood b1 mahogany)
    (surface-condition b1 smooth)
    (available b1)
    (boardsize b2 s3)
    (wood b2 mahogany)
    (surface-condition b2 smooth)
    (available b2)
    (boardsize b3 s7)
    (wood b3 oak)
    (surface-condition b3 rough)
    (available b3)
  )
  (:goal
    (and
      (available p0)
      (wood p0 cherry)
      (surface-condition p0 verysmooth)
      (available p1)
      (wood p1 cherry)
      (surface-condition p1 verysmooth)
      (available p2)
      (colour p2 blue)
      (wood p2 mahogany)
      (available p3)
      (colour p3 natural)
      (treatment p3 glazed)
      (available p4)
      (colour p4 natural)
      (treatment p4 glazed)
      (available p5)
      (colour p5 green)
      (wood p5 oak)
      (surface-condition p5 verysmooth)
      (treatment p5 glazed)
      (available p6)
      (colour p6 natural)
      (wood p6 oak)
      (surface-condition p6 smooth)
      (treatment p6 varnished)
      (available p7)
      (colour p7 natural)
      (surface-condition p7 smooth)
      (treatment p7 varnished)
      (available p8)
      (colour p8 natural)
      (wood p8 mahogany)
      (available p9)
      (colour p9 mauve)
      (treatment p9 glazed)
    )
  )
  
)
