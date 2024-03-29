(define (problem elevators-sequencedstrips-p8_6_1)
  (:domain elevators-sequencedstrips)
  (:objects
    fast0 - fast-elevator
    n0 - count
    n1 - count
    n2 - count
    n6 - count
    n8 - count
    p5 - passenger
    slow1-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n2 n8)
    (above n6 n8)
    (lift-at fast0 n2)
    (passengers fast0 n0)
    (can-hold fast0 n1)
    (reachable-floor fast0 n2)
    (reachable-floor fast0 n8)
    (lift-at slow1-0 n8)
    (passengers slow1-0 n0)
    (can-hold slow1-0 n1)
    (reachable-floor slow1-0 n6)
    (reachable-floor slow1-0 n8)
    (passenger-at p5 n6)
  )
  (:goal (and (passenger-at p5 n2)))
)
