(define (problem custom-blocks-2)
(:domain BLOCKS)
(:objects H L J X K W M Z Y - block)
(:INIT
    (CLEAR H)
    (ON H J)
    (ON J L)
    (ON L K)
    (ON K M)
    (ONTABLE M)

    (CLEAR Z)
    (ON Z X)
    (ONTABLE X)

    (CLEAR W)
    (ON W Y)
    (ONTABLE Y)
    
    (HANDEMPTY)
)
(:goal (AND
    (ON Z H)
    (ON H J)
    
    (ON K L)
    (ON L M)
    (ON M Y)
    (ON Y W)
))
)