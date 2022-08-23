(define (problem printjob)
  (:domain upp)
  (:objects
    sheet1 - sheet_t
  )
  (:init
    (uninitialized)
    (sheetsize sheet1 letter)
    (location sheet1 some_feeder_tray)
  )
  (:goal (and (sideup sheet1 front)))
)
