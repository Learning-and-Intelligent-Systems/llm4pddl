(define (problem dressed)
  (:domain dressed)
  (:objects person1 person2 person3 person4 person5 person6 person7 person8 person9 person10 person11 person12 person13 person14 person15 - person
            dress1 dress2 dress3 - dress
            sweatpants1 sweatpants2 sweatpants3 sweatpants4 sweatpants5 sweatpants6 sweatpants7 - sweatpants
            sweatshirt1 sweatshirt2 sweatshirt3 sweatshirt4 sweatshirt5 sweatshirt6 sweatshirt7 - sweatshirt
            nice-pants1 nice-pants2 nice-pants3 nice-pants4 nice-pants5 nice-pants6 nice-pants7 - nice-pants
            collared-shirt1 collared-shirt2 collared-shirt3 collared-shirt4 collared-shirt5 - collared-shirt
            suit-jacket1 suit-jacket2 suit-jacket3 suit-jacket4 suit-jacket5 - suit-jacket
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
         (wearing-nothing-formal person8)
         (wearing-nothing-casual person8)
         (wearing-nothing-formal person9)
         (wearing-nothing-casual person9)
         (wearing-nothing-formal person10)
         (wearing-nothing-casual person10)
         (wearing-nothing-formal person11)
         (wearing-nothing-casual person11)
         (wearing-nothing-formal person12)
         (wearing-nothing-casual person12)
         (wearing-nothing-formal person13)
         (wearing-nothing-casual person13)
         (wearing-nothing-formal person14)
         (wearing-nothing-casual person14)
         (wearing-nothing-formal person15)
         (wearing-nothing-casual person15)
         (in-closet dress1)
         (in-closet dress2)
         (in-closet dress3)
         (in-closet sweatpants1)
         (in-closet sweatpants2)
         (in-closet sweatpants3)
         (in-closet sweatpants4)
         (in-closet sweatpants5)
         (in-closet sweatpants6)
         (in-closet sweatpants7)
         (in-closet sweatshirt1)
         (in-closet sweatshirt2)
         (in-closet sweatshirt3)
         (in-closet sweatshirt4)
         (in-closet sweatshirt5)
         (in-closet sweatshirt6)
         (in-closet sweatshirt7)
         (in-closet nice-pants1)
         (in-closet nice-pants2)
         (in-closet nice-pants3)
         (in-closet nice-pants4)
         (in-closet nice-pants5)
         (in-closet nice-pants6)
         (in-closet nice-pants7)
         (in-closet collared-shirt1)
         (in-closet collared-shirt2)
         (in-closet collared-shirt3)
         (in-closet collared-shirt4)
         (in-closet collared-shirt5)
         (in-closet suit-jacket1)
         (in-closet suit-jacket2)
         (in-closet suit-jacket3)
         (in-closet suit-jacket4)
         (in-closet suit-jacket5)
         )
  (:goal (and (attending-casual-event person1)
              (attending-formal-event person10)
              (attending-casual-event person12)
              (attending-casual-event person9)
              (attending-formal-event person15)
              (attending-formal-event person13)
              (attending-formal-event person5)
              (attending-casual-event person6)
              (attending-formal-event person7)
              (attending-casual-event person2)
              (attending-formal-event person3)
              (attending-formal-event person8)
              (attending-casual-event person4)
              (attending-formal-event person14)
              (attending-casual-event person11)
              ))
  )