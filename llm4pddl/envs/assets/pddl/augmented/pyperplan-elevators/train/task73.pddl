(define (problem elevators-sequencedstrips-p8_5_1)
  (:domain elevators-sequencedstrips)
  (:objects
    fast0 - fast-elevator
    n0 - count
    n1 - count
    n2 - count
    n4 - count
    n8 - count
    p2 - passenger
    p3 - passenger
    slow0-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n0 n4)
    (above n1 n2)
    (above n2 n4)
    (above n4 n8)
    (lift-at fast0 n8)
    (passengers fast0 n0)
    (can-hold fast0 n1)
    (reachable-floor fast0 n4)
    (reachable-floor fast0 n8)
    (lift-at slow0-0 n0)
    (passengers slow0-0 n0)
    (can-hold slow0-0 n1)
    (reachable-floor slow0-0 n1)
    (reachable-floor slow0-0 n2)
    (reachable-floor slow0-0 n4)
    (passenger-at p2 n1)
    (passenger-at p3 n1)
  )
  (:goal (and (passenger-at p2 n8) (passenger-at p3 n2)))
)
