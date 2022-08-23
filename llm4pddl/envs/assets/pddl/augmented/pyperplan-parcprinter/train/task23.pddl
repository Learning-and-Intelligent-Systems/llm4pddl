(define (problem printjob)
  (:domain upp)
  (:objects
    sheet1 - sheet_t
  )
  (:init
    (uninitialized)
    (sheetsize sheet1 letter)
    (location sheet1 some_feeder_tray)
    (notprintedwith sheet1 back black)
    (notprintedwith sheet1 front color)
  )
  (:goal (and (notprintedwith sheet1 front color) (notprintedwith sheet1 back black) (sideup sheet1 front)))
)
