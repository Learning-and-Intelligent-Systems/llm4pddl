(define (problem dressed)
  (:domain dressed)
  (:objects person1 person2 person3 person4 person5 - person
            nice-pants1 - nice-pants
            collared-shirt1 - collared-shirt
            suit-jacket1 - suit-jacket
            )
  (:init (wearing-nothing-formal person1)
         (wearing-nothing-casual person1)
         (wearing-nothing-formal person2)
         (wearing-nothing-casual person2)
         (wearing-nothing-formal person3)
         (wearing-nothing-casual person3)
         (wearing-nothing-formal person4)
         (wearing-nothing-casual person4)
         (wearing-nothing-formal person5)
         (wearing-nothing-casual person5)
         (in-closet nice-pants1)
         (in-closet collared-shirt1)
         (in-closet suit-jacket1)
         )
  (:goal (and (attending-formal-event person1)
              ))
  )