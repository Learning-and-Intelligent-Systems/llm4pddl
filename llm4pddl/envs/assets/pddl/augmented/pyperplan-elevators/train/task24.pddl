(define (problem elevators-sequencedstrips-p8_4_1)
  (:domain elevators-sequencedstrips)
  (:objects
    fast0 - fast-elevator
    n0 - count
    n1 - count
    n4 - count
    n5 - count
    n7 - count
    n8 - count
    p0 - passenger
    p1 - passenger
    p3 - passenger
    slow0-0 - slow-elevator
    slow1-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n0 n8)
    (above n1 n4)
    (above n4 n8)
    (above n5 n8)
    (above n7 n8)
    (lift-at fast0 n0)
    (passengers fast0 n0)
    (can-hold fast0 n1)
    (reachable-floor fast0 n0)
    (reachable-floor fast0 n8)
    (lift-at slow0-0 n1)
    (passengers slow0-0 n0)
    (can-hold slow0-0 n1)
    (reachable-floor slow0-0 n4)
    (lift-at slow1-0 n5)
    (passengers slow1-0 n0)
    (can-hold slow1-0 n1)
    (reachable-floor slow1-0 n4)
    (reachable-floor slow1-0 n5)
    (reachable-floor slow1-0 n7)
    (reachable-floor slow1-0 n8)
    (passenger-at p0 n1)
    (passenger-at p1 n8)
    (passenger-at p3 n4)
  )
  (:goal (and (passenger-at p0 n0) (passenger-at p1 n7) (passenger-at p3 n5)))
)
