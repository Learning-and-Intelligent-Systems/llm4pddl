(define (problem printjob)
  (:domain upp)
  (:objects
    dummy-sheet - sheet_t
    image-1 - image_t
    image-2 - image_t
    sheet1 - sheet_t
    sheet2 - sheet_t
  )
  (:init
    (uninitialized)
    (location dummy-sheet some_finisher_tray)
    (prevsheet sheet1 dummy-sheet)
    (prevsheet sheet2 sheet1)
    (sheetsize sheet1 letter)
    (sheetsize sheet2 letter)
    (location sheet1 some_feeder_tray)
    (location sheet2 some_feeder_tray)
    (imagecolor image-1 black)
    (imagecolor image-2 color)
    (notprintedwith sheet1 front black)
    (notprintedwith sheet1 back black)
    (notprintedwith sheet1 front color)
    (notprintedwith sheet1 back color)
    (notprintedwith sheet2 front black)
    (notprintedwith sheet2 back black)
    (notprintedwith sheet2 front color)
    (notprintedwith sheet2 back color)
  )
  (:goal (and (hasimage sheet1 front image-1) (notprintedwith sheet1 front color) (notprintedwith sheet1 back black) (notprintedwith sheet1 back color) (hasimage sheet2 front image-2) (notprintedwith sheet2 front black) (notprintedwith sheet2 back black) (notprintedwith sheet2 back color) (sideup sheet1 front) (sideup sheet2 front) (stackedin sheet1 finisher1_tray) (stackedin sheet2 finisher1_tray)))
)
