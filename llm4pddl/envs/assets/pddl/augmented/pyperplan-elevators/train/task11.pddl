(define (problem elevators-sequencedstrips-p8_3_1)
  (:domain elevators-sequencedstrips)
  (:objects
    fast0 - fast-elevator
    n0 - count
    n1 - count
    n2 - count
    n3 - count
    n4 - count
    n6 - count
    n8 - count
    p1 - passenger
    slow0-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n0 n4)
    (above n0 n8)
    (above n2 n4)
    (above n3 n4)
    (above n6 n8)
    (lift-at fast0 n0)
    (passengers fast0 n0)
    (can-hold fast0 n1)
    (reachable-floor fast0 n6)
    (reachable-floor fast0 n8)
    (lift-at slow0-0 n2)
    (passengers slow0-0 n0)
    (can-hold slow0-0 n1)
    (reachable-floor slow0-0 n0)
    (reachable-floor slow0-0 n3)
    (reachable-floor slow0-0 n4)
    (passenger-at p1 n3)
  )
  (:goal (and (passenger-at p1 n6)))
)