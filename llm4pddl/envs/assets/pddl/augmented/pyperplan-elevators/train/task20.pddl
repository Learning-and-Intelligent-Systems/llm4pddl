(define (problem elevators-sequencedstrips-p8_3_2)
  (:domain elevators-sequencedstrips)
  (:objects
    n0 - count
    n1 - count
    n4 - count
    n6 - count
    n8 - count
    p1 - passenger
    slow1-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n4 n8)
    (above n6 n8)
    (lift-at slow1-0 n4)
    (passengers slow1-0 n0)
    (can-hold slow1-0 n1)
    (reachable-floor slow1-0 n6)
    (reachable-floor slow1-0 n8)
    (passenger-at p1 n4)
  )
  (:goal (and (passenger-at p1 n6)))
)
