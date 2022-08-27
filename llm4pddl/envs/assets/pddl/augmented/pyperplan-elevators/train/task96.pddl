(define (problem elevators-sequencedstrips-p8_6_1)
  (:domain elevators-sequencedstrips)
  (:objects
    n0 - count
    n1 - count
    n4 - count
    p0 - passenger
    slow0-0 - slow-elevator
  )
  (:init
    (next n0 n1)
    (above n0 n4)
    (lift-at slow0-0 n0)
    (passengers slow0-0 n0)
    (can-hold slow0-0 n1)
    (reachable-floor slow0-0 n4)
    (passenger-at p0 n0)
  )
  (:goal (and (passenger-at p0 n4)))
)
