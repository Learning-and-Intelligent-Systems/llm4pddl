(define (problem p006-microban-sequential)
  (:domain sokoban-sequential)
  (:objects
    dir-down - direction
    dir-left - direction
    dir-right - direction
    dir-up - direction
    player-01 - player
    pos-02-02 - location
    pos-02-03 - location
    pos-03-02 - location
    pos-03-03 - location
    pos-04-02 - location
    pos-04-03 - location
    pos-04-04 - location
    pos-05-02 - location
    pos-05-03 - location
    pos-06-03 - location
    pos-07-03 - location
    pos-08-03 - location
    pos-08-04 - location
    pos-09-02 - location
    pos-09-03 - location
    pos-09-04 - location
    pos-10-02 - location
    pos-10-04 - location
    pos-11-02 - location
    pos-11-03 - location
    pos-11-04 - location
    stone-01 - stone
    stone-02 - stone
  )
  (:init
    (is-goal pos-08-04)
    (is-nongoal pos-04-03)
    (is-nongoal pos-04-04)
    (is-nongoal pos-05-03)
    (is-nongoal pos-06-03)
    (is-nongoal pos-07-03)
    (is-nongoal pos-08-03)
    (is-nongoal pos-09-03)
    (is-nongoal pos-09-04)
    (move-dir pos-02-02 pos-02-03 dir-down)
    (move-dir pos-02-03 pos-03-03 dir-right)
    (move-dir pos-03-02 pos-02-02 dir-left)
    (move-dir pos-03-03 pos-04-03 dir-right)
    (move-dir pos-04-02 pos-03-02 dir-left)
    (move-dir pos-04-02 pos-04-03 dir-down)
    (move-dir pos-04-03 pos-04-04 dir-down)
    (move-dir pos-04-03 pos-05-03 dir-right)
    (move-dir pos-05-02 pos-04-02 dir-left)
    (move-dir pos-05-03 pos-05-02 dir-up)
    (move-dir pos-05-03 pos-06-03 dir-right)
    (move-dir pos-06-03 pos-05-03 dir-left)
    (move-dir pos-06-03 pos-07-03 dir-right)
    (move-dir pos-07-03 pos-06-03 dir-left)
    (move-dir pos-07-03 pos-08-03 dir-right)
    (move-dir pos-08-03 pos-07-03 dir-left)
    (move-dir pos-08-03 pos-08-04 dir-down)
    (move-dir pos-08-03 pos-09-03 dir-right)
    (move-dir pos-08-04 pos-09-04 dir-right)
    (move-dir pos-09-02 pos-09-03 dir-down)
    (move-dir pos-09-02 pos-10-02 dir-right)
    (move-dir pos-09-03 pos-08-03 dir-left)
    (move-dir pos-09-03 pos-09-02 dir-up)
    (move-dir pos-09-03 pos-09-04 dir-down)
    (move-dir pos-09-04 pos-08-04 dir-left)
    (move-dir pos-09-04 pos-10-04 dir-right)
    (move-dir pos-10-02 pos-09-02 dir-left)
    (move-dir pos-10-02 pos-11-02 dir-right)
    (move-dir pos-10-04 pos-09-04 dir-left)
    (move-dir pos-10-04 pos-11-04 dir-right)
    (move-dir pos-11-02 pos-10-02 dir-left)
    (move-dir pos-11-02 pos-11-03 dir-down)
    (move-dir pos-11-03 pos-11-02 dir-up)
    (move-dir pos-11-03 pos-11-04 dir-down)
    (move-dir pos-11-04 pos-10-04 dir-left)
    (move-dir pos-11-04 pos-11-03 dir-up)
    (at player-01 pos-11-03)
    (at stone-01 pos-03-03)
    (at stone-02 pos-04-03)
    (clear pos-02-02)
    (clear pos-02-03)
    (clear pos-03-02)
    (clear pos-04-02)
    (clear pos-04-04)
    (clear pos-05-02)
    (clear pos-05-03)
    (clear pos-06-03)
    (clear pos-07-03)
    (clear pos-08-03)
    (clear pos-08-04)
    (clear pos-09-02)
    (clear pos-09-03)
    (clear pos-09-04)
    (clear pos-10-02)
    (clear pos-10-04)
    (clear pos-11-02)
    (clear pos-11-04)
  )
  (:goal (and (at-goal stone-01)))
)
