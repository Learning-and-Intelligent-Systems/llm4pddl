; woodworking task with 7 parts and 120% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 978438

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
    black red green mauve blue - acolour
    teak oak - awood
    p0 p1 p2 p3 p4 p5 p6 - part
    b0 b1 b2 - board
    s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 - aboardsize
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
    (boardsize-successor s9 s10)
    (has-colour glazer0 blue)
    (has-colour glazer0 mauve)
    (has-colour glazer0 natural)
    (has-colour glazer0 red)
    (has-colour immersion-varnisher0 mauve)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 mauve)
    (unused p0)
    (goalsize p0 small)
    
    
    
    
    (unused p1)
    (goalsize p1 medium)
    
    
    
    
    (unused p2)
    (goalsize p2 small)
    
    
    
    
    (unused p3)
    (goalsize p3 medium)
    
    
    
    
    (unused p4)
    (goalsize p4 large)
    
    
    
    
    (unused p5)
    (goalsize p5 large)
    
    
    
    
    (available p6)
    (colour p6 mauve)
    (wood p6 oak)
    (surface-condition p6 smooth)
    (treatment p6 varnished)
    (goalsize p6 small)
    
    
    
    
    (boardsize b0 s10)
    (wood b0 teak)
    (surface-condition b0 smooth)
    (available b0)
    (boardsize b1 s4)
    (wood b1 teak)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s2)
    (wood b2 oak)
    (surface-condition b2 smooth)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (colour p0 red)
      (treatment p0 glazed)
      (available p1)
      (colour p1 blue)
      (treatment p1 glazed)
      (available p2)
      (colour p2 mauve)
      (surface-condition p2 verysmooth)
      (available p3)
      (colour p3 natural)
      (wood p3 teak)
      (surface-condition p3 smooth)
      (treatment p3 glazed)
      (available p4)
      (colour p4 natural)
      (surface-condition p4 verysmooth)
      (treatment p4 glazed)
      (available p5)
      (wood p5 teak)
      (treatment p5 glazed)
      (available p6)
      (wood p6 oak)
      (surface-condition p6 verysmooth)
      (treatment p6 glazed)
    )
  )
  
)
