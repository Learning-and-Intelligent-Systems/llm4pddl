(define (problem dressed)
  (:domain dressed)
  (:objects person1 person2 person3 person4 - person
            sweatshirt1 - sweatshirt
            )
  (:init (wearing-nothing-formal person1)
         (wearing-nothing-casual person1)
         (wearing-nothing-formal person2)
         (wearing-nothing-casual person2)
         (wearing-nothing-formal person3)
         (wearing-nothing-casual person3)
         (wearing-nothing-formal person4)
         (wearing-nothing-casual person4)
         (in-closet sweatshirt1)
         )
  (:goal (and ))
  )