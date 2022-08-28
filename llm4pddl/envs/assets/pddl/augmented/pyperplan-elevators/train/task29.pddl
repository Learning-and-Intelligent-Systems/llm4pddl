(define (problem elevators-sequencedstrips-p8_4_1)
  (:domain elevators-sequencedstrips)
  (:objects
    n0 - count
    n1 - count
    n4 - count
    n5 - count
    n8 - count
    p3 - passenger
    slow1-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n4 n8)
    (above n5 n8)
    (lift-at slow1-0 n5)
    (passengers slow1-0 n0)
    (can-hold slow1-0 n1)
    (reachable-floor slow1-0 n4)
    (reachable-floor slow1-0 n5)
    (reachable-floor slow1-0 n8)
    (passenger-at p3 n4)
  )
  (:goal (and (passenger-at p3 n5)))
)
