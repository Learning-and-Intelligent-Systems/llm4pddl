(define (problem printjob)
  (:domain etipp)
  (:objects
    sheet1 - sheet_t
  )
  (:init
    (uninitialized)
    (oppositeside back front)
    (sheetsize sheet1 letter)
    (location sheet1 some_feeder_tray)
    (notprintedwith sheet1 back black)
    (notprintedwith sheet1 front color)
    (notprintedwith sheet1 back color)
  )
  (:goal (and (notprintedwith sheet1 front color) (notprintedwith sheet1 back black) (notprintedwith sheet1 back color) (sideup sheet1 front)))
)
