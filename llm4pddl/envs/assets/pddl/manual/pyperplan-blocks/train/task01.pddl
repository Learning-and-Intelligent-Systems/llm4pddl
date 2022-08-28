(define (problem custom-blocks-1)
(:domain BLOCKS)
(:objects N M O P Q R S T - block)
(:INIT
    (CLEAR P)
    (ON P N)
    (ON N M)
    (ON M T)
    (ONTABLE T)

    (CLEAR O)
    (ON O Q)
    (ON Q R)
    (ONTABLE R)

    (CLEAR S)
    (ONTABLE S)
    
    (HANDEMPTY)
)
(:goal (AND
    (ON M S)
    (ON S N)
    (ON N R)
    (ON Q T)
    (ON T O)
))
)