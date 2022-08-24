(define (problem elevators-sequencedstrips-p8_3_1)
  (:domain elevators-sequencedstrips)
  (:objects
    n0 - count
    n1 - count
    n2 - count
    n4 - count
    n8 - count
    p0 - passenger
    p2 - passenger
    slow0-0 - slow-elevator
    slow1-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n1 n4)
    (above n2 n4)
    (above n4 n8)
    (lift-at slow0-0 n2)
    (passengers slow0-0 n0)
    (can-hold slow0-0 n1)
    (reachable-floor slow0-0 n1)
    (reachable-floor slow0-0 n4)
    (lift-at slow1-0 n4)
    (passengers slow1-0 n0)
    (can-hold slow1-0 n1)
    (reachable-floor slow1-0 n4)
    (reachable-floor slow1-0 n8)
    (passenger-at p0 n8)
    (passenger-at p2 n2)
  )
  (:goal (and (passenger-at p0 n4) (passenger-at p2 n1)))
)
