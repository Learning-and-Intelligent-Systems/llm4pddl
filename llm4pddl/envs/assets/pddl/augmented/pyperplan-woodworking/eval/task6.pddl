; woodworking task with 6 parts and 100% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 462676

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
    mauve red blue black - acolour
    walnut pine - awood
    p0 p1 p2 p3 p4 p5 - part
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
    (has-colour glazer0 blue)
    (has-colour glazer0 black)
    (has-colour glazer0 red)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 red)
    (unused p0)
    (goalsize p0 medium)
    
    
    
    
    (available p1)
    (colour p1 mauve)
    (wood p1 pine)
    (surface-condition p1 rough)
    (treatment p1 varnished)
    (goalsize p1 medium)
    
    
    
    
    (unused p2)
    (goalsize p2 medium)
    
    
    
    
    (unused p3)
    (goalsize p3 small)
    
    
    
    
    (available p4)
    (colour p4 mauve)
    (wood p4 walnut)
    (surface-condition p4 smooth)
    (treatment p4 colourfragments)
    (goalsize p4 small)
    
    
    
    
    (unused p5)
    (goalsize p5 medium)
    
    
    
    
    (boardsize b0 s5)
    (wood b0 pine)
    (surface-condition b0 smooth)
    (available b0)
    (boardsize b1 s2)
    (wood b1 walnut)
    (surface-condition b1 rough)
    (available b1)
  )
  (:goal
    (and
      (available p0)
      (colour p0 red)
      (wood p0 walnut)
      (surface-condition p0 smooth)
      (treatment p0 varnished)
      (available p1)
      (wood p1 pine)
      (surface-condition p1 verysmooth)
      (available p2)
      (colour p2 red)
      (wood p2 pine)
      (available p3)
      (wood p3 pine)
      (surface-condition p3 smooth)
      (treatment p3 varnished)
      (available p4)
      (colour p4 blue)
      (wood p4 walnut)
      (available p5)
      (colour p5 black)
      (wood p5 pine)
      (surface-condition p5 verysmooth)
      (treatment p5 glazed)
    )
  )
  
)
