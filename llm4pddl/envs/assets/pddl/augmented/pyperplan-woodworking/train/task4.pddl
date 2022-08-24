; woodworking task with 4 parts and 100% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 938703

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
    red black blue - acolour
    pine mahogany - awood
    p0 p1 p2 p3 - part
    b0 b1 - board
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
    (has-colour glazer0 black)
    (has-colour glazer0 natural)
    (has-colour immersion-varnisher0 black)
    (has-colour immersion-varnisher0 natural)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 black)
    (has-colour spray-varnisher0 natural)
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
  (:goal
    (and
      (available p0)
      (colour p0 black)
      (wood p0 mahogany)
      (available p1)
      (wood p1 pine)
      (surface-condition p1 smooth)
      (available p2)
      (wood p2 pine)
      (treatment p2 varnished)
      (available p3)
      (colour p3 natural)
      (wood p3 mahogany)
    )
  )
  
)
