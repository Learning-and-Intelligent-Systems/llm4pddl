(define (problem printjob)
  (:domain etipp)
  (:objects
    dummy-sheet - sheet_t
    sheet1 - sheet_t
  )
  (:init
    (uninitialized)
    (location dummy-sheet some_finisher_tray)
    (prevsheet sheet1 dummy-sheet)
    (sheetsize sheet1 letter)
    (location sheet1 some_feeder_tray)
    (notprintedwith sheet1 front color)
  )
  (:goal (and (notprintedwith sheet1 front color) (stackedin sheet1 sys_outputtray)))
)
