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
  )
  (:goal (and (sideup sheet1 front)))
)
