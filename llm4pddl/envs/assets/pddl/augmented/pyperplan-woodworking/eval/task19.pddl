; woodworking task with 11 parts and 120% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 976783

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
    white black blue green red mauve - acolour
    pine walnut cherry - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 - part
    b0 b1 b2 - board
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
    (has-colour glazer0 mauve)
    (has-colour glazer0 black)
    (has-colour glazer0 red)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 mauve)
    (has-colour immersion-varnisher0 black)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 mauve)
    (has-colour spray-varnisher0 black)
    (available p0)
    (colour p0 green)
    (wood p0 walnut)
    (surface-condition p0 smooth)
    (treatment p0 colourfragments)
    (goalsize p0 large)
    
    
    
    
    (unused p1)
    (goalsize p1 small)
    
    
    
    
    (unused p2)
    (goalsize p2 small)
    
    
    
    
    (unused p3)
    (goalsize p3 medium)
    
    
    
    
    (unused p4)
    (goalsize p4 small)
    
    
    
    
    (unused p5)
    (goalsize p5 large)
    
    
    
    
    (available p6)
    (colour p6 green)
    (wood p6 walnut)
    (surface-condition p6 verysmooth)
    (treatment p6 glazed)
    (goalsize p6 large)
    
    
    
    
    (unused p7)
    (goalsize p7 medium)
    
    
    
    
    (unused p8)
    (goalsize p8 large)
    
    
    
    
    (unused p9)
    (goalsize p9 medium)
    
    
    
    
    (unused p10)
    (goalsize p10 medium)
    
    
    
    
    (boardsize b0 s6)
    (wood b0 cherry)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s8)
    (wood b1 pine)
    (surface-condition b1 smooth)
    (available b1)
    (boardsize b2 s8)
    (wood b2 walnut)
    (surface-condition b2 rough)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (surface-condition p0 verysmooth)
      (treatment p0 glazed)
      (available p1)
      (colour p1 black)
      (treatment p1 glazed)
      (available p2)
      (colour p2 mauve)
      (wood p2 pine)
      (available p3)
      (wood p3 cherry)
      (treatment p3 varnished)
      (available p4)
      (wood p4 cherry)
      (treatment p4 varnished)
      (available p5)
      (wood p5 pine)
      (surface-condition p5 smooth)
      (available p6)
      (colour p6 red)
      (treatment p6 glazed)
      (available p7)
      (surface-condition p7 smooth)
      (treatment p7 glazed)
      (available p8)
      (colour p8 blue)
      (surface-condition p8 smooth)
      (available p9)
      (colour p9 black)
      (treatment p9 glazed)
      (available p10)
      (colour p10 black)
      (wood p10 pine)
      (surface-condition p10 verysmooth)
    )
  )
  
)
