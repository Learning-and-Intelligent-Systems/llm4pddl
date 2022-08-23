(define (problem p094-microban-sequential)
  (:domain sokoban-sequential)
  (:objects
    dir-down - direction
    dir-left - direction
    dir-right - direction
    dir-up - direction
    player-01 - player
    pos-3-2 - location
    pos-4-2 - location
    pos-4-3 - location
    pos-5-3 - location
    pos-6-2 - location
    pos-6-3 - location
    pos-6-5 - location
    pos-7-2 - location
    pos-7-3 - location
    pos-7-4 - location
    pos-7-5 - location
    pos-7-6 - location
    pos-7-7 - location
    pos-8-5 - location
    pos-8-6 - location
    pos-8-7 - location
    stone-02 - stone
  )
  (:init
    (is-goal pos-6-5)
    (is-nongoal pos-6-3)
    (is-nongoal pos-7-3)
    (is-nongoal pos-7-4)
    (is-nongoal pos-7-5)
    (is-nongoal pos-7-6)
    (move-dir pos-3-2 pos-4-2 dir-right)
    (move-dir pos-4-2 pos-4-3 dir-down)
    (move-dir pos-4-3 pos-5-3 dir-right)
    (move-dir pos-5-3 pos-6-3 dir-right)
    (move-dir pos-6-2 pos-7-2 dir-right)
    (move-dir pos-6-3 pos-6-2 dir-up)
    (move-dir pos-6-3 pos-7-3 dir-right)
    (move-dir pos-7-2 pos-7-3 dir-down)
    (move-dir pos-7-3 pos-7-4 dir-down)
    (move-dir pos-7-4 pos-7-5 dir-down)
    (move-dir pos-7-5 pos-6-5 dir-left)
    (move-dir pos-7-5 pos-7-6 dir-down)
    (move-dir pos-7-5 pos-8-5 dir-right)
    (move-dir pos-7-6 pos-7-5 dir-up)
    (move-dir pos-7-6 pos-8-6 dir-right)
    (move-dir pos-7-7 pos-7-6 dir-up)
    (move-dir pos-8-5 pos-7-5 dir-left)
    (move-dir pos-8-5 pos-8-6 dir-down)
    (move-dir pos-8-6 pos-8-5 dir-up)
    (move-dir pos-8-6 pos-8-7 dir-down)
    (move-dir pos-8-7 pos-7-7 dir-left)
    (at player-01 pos-3-2)
    (at stone-02 pos-5-3)
    (clear pos-4-2)
    (clear pos-4-3)
    (clear pos-6-2)
    (clear pos-6-3)
    (clear pos-6-5)
    (clear pos-7-2)
    (clear pos-7-3)
    (clear pos-7-4)
    (clear pos-7-5)
    (clear pos-7-6)
    (clear pos-7-7)
    (clear pos-8-5)
    (clear pos-8-6)
    (clear pos-8-7)
  )
  (:goal (and (at-goal stone-02)))
)
