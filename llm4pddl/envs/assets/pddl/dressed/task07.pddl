(define (problem dressed)
  (:domain dressed)
  (:objects person1 person2 person3 person4 person5 person6 person7 - person
            dress1 dress2 - dress
            sweatpants1 sweatpants2 sweatpants3 - sweatpants
            sweatshirt1 sweatshirt2 sweatshirt3 - sweatshirt
            nice-pants1 nice-pants2 - nice-pants
            collared-shirt1 collared-shirt2 - collared-shirt
            suit-jacket1 suit-jacket2 - suit-jacket
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
         (wearing-nothing-formal person6)
         (wearing-nothing-casual person6)
         (wearing-nothing-formal person7)
         (wearing-nothing-casual person7)
         (in-closet dress1)
         (in-closet dress2)
         (in-closet sweatpants1)
         (in-closet sweatpants2)
         (in-closet sweatpants3)
         (in-closet sweatshirt1)
         (in-closet sweatshirt2)
         (in-closet sweatshirt3)
         (in-closet nice-pants1)
         (in-closet nice-pants2)
         (in-closet collared-shirt1)
         (in-closet collared-shirt2)
         (in-closet suit-jacket1)
         (in-closet suit-jacket2)
         )
  (:goal (and (attending-casual-event person5)
              (attending-casual-event person6)
              (attending-formal-event person2)
              (attending-formal-event person3)
              (attending-casual-event person7)
              (attending-formal-event person1)
              (attending-formal-event person4)
              ))
  )