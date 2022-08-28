(define (problem printjob)
  (:domain etipp)
  (:objects
    image-1 - image_t
    sheet1 - sheet_t
  )
  (:init
    (uninitialized)
    (oppositeside back front)
    (sheetsize sheet1 letter)
    (location sheet1 some_feeder_tray)
    (imagecolor image-1 black)
    (notprintedwith sheet1 front black)
    (notprintedwith sheet1 back color)
  )
  (:goal (and (hasimage sheet1 front image-1) (notprintedwith sheet1 back color)))
)
