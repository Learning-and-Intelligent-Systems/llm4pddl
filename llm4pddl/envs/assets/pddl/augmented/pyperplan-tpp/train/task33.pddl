(define (problem tpp)
  (:domain tpp-propositional)
  (:objects
    depot1 - depot
    goods3 - goods
    goods4 - goods
    level0 - level
    level1 - level
    market1 - market
    market2 - market
    truck2 - truck
  )
  (:init
    (next level1 level0)
    (ready-to-load goods3 market1 level0)
    (ready-to-load goods4 market1 level0)
    (stored goods3 level0)
    (stored goods4 level0)
    (loaded goods3 truck2 level0)
    (loaded goods4 truck2 level0)
    (connected market1 market2)
    (connected market2 market1)
    (connected depot1 market2)
    (connected market2 depot1)
    (on-sale goods3 market1 level1)
    (on-sale goods4 market1 level1)
    (at truck2 depot1)
  )
  (:goal (and (stored goods3 level1) (stored goods4 level1)))
)
