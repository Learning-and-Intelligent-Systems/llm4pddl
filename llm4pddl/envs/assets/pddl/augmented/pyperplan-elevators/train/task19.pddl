(define (problem elevators-sequencedstrips-p8_3_2)
  (:domain elevators-sequencedstrips)
  (:objects
    fast1 - fast-elevator
    n0 - count
    n1 - count
    n4 - count
    n6 - count
    n8 - count
    p0 - passenger
    p1 - passenger
    slow1-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n0 n8)
    (above n4 n8)
    (above n6 n8)
    (lift-at fast1 n8)
    (passengers fast1 n0)
    (can-hold fast1 n1)
    (reachable-floor fast1 n0)
    (reachable-floor fast1 n8)
    (lift-at slow1-0 n4)
    (passengers slow1-0 n0)
    (can-hold slow1-0 n1)
    (reachable-floor slow1-0 n4)
    (reachable-floor slow1-0 n6)
    (reachable-floor slow1-0 n8)
    (passenger-at p0 n0)
    (passenger-at p1 n4)
  )
  (:goal (and (passenger-at p0 n4) (passenger-at p1 n6)))
)
