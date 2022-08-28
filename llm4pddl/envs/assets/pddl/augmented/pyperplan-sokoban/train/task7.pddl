(define (problem p024-microban-sequential)
  (:domain sokoban-sequential)
  (:objects
    dir-down - direction
    dir-left - direction
    dir-right - direction
    dir-up - direction
    player-01 - player
    pos-2-4 - location
    pos-2-5 - location
    pos-2-6 - location
    pos-3-4 - location
    pos-3-5 - location
    pos-3-6 - location
    pos-4-2 - location
    pos-4-3 - location
    pos-4-4 - location
    pos-4-5 - location
    pos-4-6 - location
    pos-5-2 - location
    pos-5-3 - location
    pos-5-5 - location
    pos-5-6 - location
    pos-6-2 - location
    pos-6-3 - location
    pos-6-5 - location
    pos-6-6 - location
    stone-01 - stone
    stone-02 - stone
  )
  (:init
    (is-goal pos-3-6)
    (is-goal pos-5-6)
    (is-nongoal pos-3-5)
    (is-nongoal pos-4-3)
    (is-nongoal pos-4-4)
    (is-nongoal pos-4-5)
    (is-nongoal pos-4-6)
    (move-dir pos-2-4 pos-2-5 dir-down)
    (move-dir pos-2-5 pos-2-6 dir-down)
    (move-dir pos-2-6 pos-3-6 dir-right)
    (move-dir pos-3-4 pos-2-4 dir-left)
    (move-dir pos-3-4 pos-3-5 dir-down)
    (move-dir pos-3-5 pos-3-6 dir-down)
    (move-dir pos-3-6 pos-4-6 dir-right)
    (move-dir pos-4-2 pos-4-3 dir-down)
    (move-dir pos-4-2 pos-5-2 dir-right)
    (move-dir pos-4-3 pos-4-2 dir-up)
    (move-dir pos-4-3 pos-4-4 dir-down)
    (move-dir pos-4-4 pos-3-4 dir-left)
    (move-dir pos-4-4 pos-4-3 dir-up)
    (move-dir pos-4-4 pos-4-5 dir-down)
    (move-dir pos-4-5 pos-3-5 dir-left)
    (move-dir pos-4-5 pos-4-4 dir-up)
    (move-dir pos-4-5 pos-4-6 dir-down)
    (move-dir pos-4-6 pos-4-5 dir-up)
    (move-dir pos-4-6 pos-5-6 dir-right)
    (move-dir pos-5-2 pos-4-2 dir-left)
    (move-dir pos-5-2 pos-6-2 dir-right)
    (move-dir pos-5-3 pos-4-3 dir-left)
    (move-dir pos-5-3 pos-6-3 dir-right)
    (move-dir pos-5-5 pos-4-5 dir-left)
    (move-dir pos-5-6 pos-6-6 dir-right)
    (move-dir pos-6-2 pos-5-2 dir-left)
    (move-dir pos-6-2 pos-6-3 dir-down)
    (move-dir pos-6-3 pos-5-3 dir-left)
    (move-dir pos-6-3 pos-6-2 dir-up)
    (move-dir pos-6-5 pos-5-5 dir-left)
    (move-dir pos-6-6 pos-6-5 dir-up)
    (at player-01 pos-6-3)
    (at stone-01 pos-4-3)
    (at stone-02 pos-5-3)
    (clear pos-2-4)
    (clear pos-2-5)
    (clear pos-2-6)
    (clear pos-3-4)
    (clear pos-3-5)
    (clear pos-3-6)
    (clear pos-4-2)
    (clear pos-4-4)
    (clear pos-4-5)
    (clear pos-4-6)
    (clear pos-5-2)
    (clear pos-5-5)
    (clear pos-5-6)
    (clear pos-6-2)
    (clear pos-6-5)
    (clear pos-6-6)
  )
  (:goal (and (at-goal stone-01) (at-goal stone-02)))
)
