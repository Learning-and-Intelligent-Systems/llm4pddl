(define (problem tpp)
  (:domain tpp-propositional)
  (:objects
    depot1 - depot
    goods2 - goods
    goods3 - goods
    goods4 - goods
    goods5 - goods
    level0 - level
    level1 - level
    market1 - market
    market2 - market
    truck2 - truck
  )
  (:init
    (next level1 level0)
    (ready-to-load goods2 market1 level0)
    (ready-to-load goods3 market1 level0)
    (ready-to-load goods4 market1 level0)
    (ready-to-load goods5 market1 level0)
    (stored goods2 level0)
    (stored goods3 level0)
    (stored goods4 level0)
    (stored goods5 level0)
    (loaded goods2 truck2 level0)
    (loaded goods3 truck2 level0)
    (loaded goods4 truck2 level0)
    (loaded goods5 truck2 level0)
    (connected market1 market2)
    (connected market2 market1)
    (connected depot1 market2)
    (connected market2 depot1)
    (on-sale goods2 market1 level1)
    (on-sale goods3 market1 level1)
    (on-sale goods4 market1 level1)
    (on-sale goods5 market1 level1)
    (at truck2 depot1)
  )
  (:goal (and (stored goods2 level1) (stored goods3 level1) (stored goods4 level1) (stored goods5 level1)))
)
