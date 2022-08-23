(define (problem tpp)
  (:domain tpp-propositional)
  (:objects
    depot1 - depot
    goods2 - goods
    level0 - level
    level1 - level
    market1 - market
    market2 - market
    truck2 - truck
  )
  (:init
    (next level1 level0)
    (ready-to-load goods2 market1 level0)
    (stored goods2 level0)
    (loaded goods2 truck2 level0)
    (connected market1 market2)
    (connected market2 market1)
    (connected depot1 market2)
    (connected market2 depot1)
    (on-sale goods2 market1 level1)
    (at truck2 depot1)
  )
  (:goal (and (stored goods2 level1)))
)
