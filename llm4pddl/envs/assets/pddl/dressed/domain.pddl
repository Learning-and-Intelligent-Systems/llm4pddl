(define 
    (domain dressed)
    (:requirements :typing)
    (:types 
        clothing person - object
        sweatshirt sweatpants collared-shirt suit-jacket nice-pants dress - clothing
    )
; assume the person is wearing their underclothing of choice.
    (:predicates 
        (in-closet ?c - clothing)
        (wearing-collared-shirt ?p - person)
        (wearing-suit-jacket ?p - person)
        (wearing-nice-pants ?p - person)
        (wearing-sweatshirt ?p - person)
        (wearing-sweatpants ?p - person)
        (wearing-dress ?p - person)
        (attending-casual-event ?p - person)
        (attending-formal-event ?p - person)
        (wearing-nothing-formal ?p - person)
        (wearing-nothing-casual ?p - person)
    )

    (:action put-on-dress
        :parameters (?p - person ?d - dress)
        :precondition (and (in-closet ?d))
        :effect (and (not (in-closet ?d))
                     (wearing-dress ?p)
                     (not (wearing-nothing-formal ?p)))
    )

    (:action put-on-sweatshirt
        :parameters (?p - person ?s - sweatshirt)
        :precondition (and (in-closet ?s))
        :effect (and (not (in-closet ?s))
                     (wearing-sweatshirt ?p)
                     (not (wearing-nothing-casual ?p)))
    )

    (:action put-on-collared-shirt
        :parameters (?p - person ?cs - collared-shirt)
        :precondition (and (in-closet ?cs))
        :effect (and (not (in-closet ?cs))
                     (wearing-collared-shirt ?p)
                     (not (wearing-nothing-formal ?p)))
    )

    (:action put-on-suit-jacket
        :parameters (?p - person ?sj - suit-jacket)
        :precondition (and (in-closet ?sj) 
                           (wearing-collared-shirt ?p))
        :effect (and (not (in-closet ?sj))
                     (wearing-suit-jacket ?p)
                     (not (wearing-nothing-formal ?p)))
    )

    (:action put-on-sweatpants
        :parameters (?p - person ?s - sweatpants)
        :precondition (and (in-closet ?s))
        :effect (and (not (in-closet ?s))
                     (wearing-sweatpants ?p)
                     (not (wearing-nothing-casual ?p)))
    )

    (:action put-on-nice-pants
        :parameters (?p - person ?np - nice-pants)
        :precondition (and (in-closet ?np))
        :effect (and (not (in-closet ?np))
                     (wearing-nice-pants ?p)
                     (not (wearing-nothing-formal ?p)))
    )

    (:action attend-casual-event
        :parameters (?p - person)
        :precondition (and (wearing-nothing-formal ?p)
                           (wearing-sweatshirt ?p)
                           (wearing-sweatpants ?p))
        :effect (and (attending-casual-event ?p))
    )

    (:action attend-formal-event-in-suit
        :parameters (?p - person)
        :precondition (and (wearing-nothing-casual ?p)
                           (wearing-collared-shirt ?p) 
                           (wearing-suit-jacket ?p) 
                           (wearing-nice-pants ?p))
        :effect (and (attending-formal-event ?p))
    )

    (:action attend-formal-event-in-dress
        :parameters (?p - person)
        :precondition (and (wearing-nothing-casual ?p)
                           (wearing-dress ?p))
        :effect (and (attending-formal-event ?p))
    )
)
