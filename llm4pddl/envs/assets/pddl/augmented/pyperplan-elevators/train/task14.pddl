(define (problem elevators-sequencedstrips-p8_3_1)
  (:domain elevators-sequencedstrips)
  (:objects
    n0 - count
    n1 - count
    n2 - count
    n4 - count
    p2 - passenger
    slow0-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n1 n4)
    (above n2 n4)
    (lift-at slow0-0 n2)
    (passengers slow0-0 n0)
    (can-hold slow0-0 n1)
    (reachable-floor slow0-0 n1)
    (reachable-floor slow0-0 n4)
    (passenger-at p2 n2)
  )
  (:goal (and (passenger-at p2 n1)))
)
