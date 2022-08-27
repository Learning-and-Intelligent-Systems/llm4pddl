(define (problem tpp)
  (:domain tpp-propositional)
  (:objects
    depot1 - depot
    goods4 - goods
    level0 - level
    level1 - level
    market1 - market
    truck1 - truck
  )
  (:init
    (next level1 level0)
    (ready-to-load goods4 market1 level0)
    (stored goods4 level0)
    (loaded goods4 truck1 level0)
    (connected depot1 market1)
    (connected market1 depot1)
    (on-sale goods4 market1 level1)
    (at truck1 depot1)
  )
  (:goal (and (stored goods4 level1)))
)