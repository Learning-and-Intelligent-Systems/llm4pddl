; woodworking task with 6 parts and 140% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 240917

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
    blue red mauve white - acolour
    beech teak - awood
    p0 p1 p2 p3 p4 p5 - part
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
    (has-colour glazer0 white)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 white)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 white)
    (has-colour spray-varnisher0 red)
    (unused p0)
    (goalsize p0 medium)
    
    
    
    
    (unused p1)
    (goalsize p1 medium)
    
    
    
    
    (unused p2)
    (goalsize p2 medium)
    
    
    
    
    (available p3)
    (colour p3 blue)
    (wood p3 teak)
    (surface-condition p3 verysmooth)
    (treatment p3 varnished)
    (goalsize p3 large)
    
    
    
    
    (unused p4)
    (goalsize p4 small)
    
    
    
    
    (unused p5)
    (goalsize p5 medium)
    
    
    
    
    (boardsize b0 s8)
    (wood b0 beech)
    (surface-condition b0 smooth)
    (available b0)
    (boardsize b1 s4)
    (wood b1 beech)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s2)
    (wood b2 teak)
    (surface-condition b2 rough)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (colour p0 white)
      (wood p0 beech)
      (available p1)
      (wood p1 beech)
      (treatment p1 glazed)
      (available p2)
      (colour p2 blue)
      (wood p2 beech)
      (surface-condition p2 verysmooth)
      (available p3)
      (colour p3 red)
      (wood p3 teak)
      (surface-condition p3 verysmooth)
      (treatment p3 varnished)
      (available p4)
      (wood p4 teak)
      (surface-condition p4 smooth)
      (treatment p4 glazed)
      (available p5)
      (wood p5 beech)
      (treatment p5 varnished)
    )
  )
  
)
