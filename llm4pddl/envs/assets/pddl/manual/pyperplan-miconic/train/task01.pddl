(define (problem miconic-custom-1)
   (:domain miconic)
   (:objects alice bob carol dave edna - passenger
             floor30 floor31 floor32 floor33 floor34 floor35 - floor)


(:init
(above floor30 floor31)
(above floor30 floor32)
(above floor30 floor33)
(above floor30 floor34)
(above floor30 floor35)

(above floor31 floor32)
(above floor31 floor33)
(above floor31 floor34)
(above floor31 floor35)

(above floor32 floor33)
(above floor32 floor34)
(above floor32 floor35)

(above floor33 floor34)
(above floor33 floor35)

(above floor34 floor35)

(origin alice floor31)
(destin alice floor34)

(origin bob floor33)
(destin bob floor31)

(origin carol floor35)
(destin carol floor31)

(origin dave floor34)
(destin dave floor31)

(origin edna floor33)
(destin edna floor32)

(lift-at floor30)
)


(:goal (and 
(served alice)
(served bob)
(served carol)
(served dave)
(served edna)
))
)


