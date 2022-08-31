(define (problem dressed)
  (:domain dressed)
  (:objects person1 person2 person3 person4 person5 - person
            dress1 dress2 - dress
            sweatpants1 sweatpants2 - sweatpants
            sweatshirt1 sweatshirt2 - sweatshirt
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
         (in-closet dress1)
         (in-closet dress2)
         (in-closet sweatpants1)
         (in-closet sweatpants2)
         (in-closet sweatshirt1)
         (in-closet sweatshirt2)
         (in-closet nice-pants1)
         (in-closet collared-shirt1)
         (in-closet suit-jacket1)
         )
  (:goal (and (attending-formal-event person2)
              (attending-casual-event person1)
              (attending-casual-event person5)
              (attending-formal-event person4)
              (attending-formal-event person3)
              ))
  )