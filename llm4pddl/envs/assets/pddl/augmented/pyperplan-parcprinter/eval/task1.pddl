(define (problem PrintJob)
(:domain eTipp)
(:objects
		dummy-sheet
		sheet1
		sheet2 - sheet_t
		image-1
		image-2 - image_t
)
(:init
		(Uninitialized)
		
		(Oppositeside Front Back)
		(Oppositeside Back Front)
		(Location dummy-sheet Some_Finisher_Tray)
		(Prevsheet sheet1 dummy-sheet)
		(Prevsheet sheet2 sheet1)
		(Sheetsize sheet1 Letter)
		(Sheetsize sheet2 Letter)
		(Location sheet1 Some_Feeder_Tray)
		(Location sheet2 Some_Feeder_Tray)
		(Imagecolor image-1 Color)
		(Imagecolor image-2 Black)
		(Notprintedwith sheet1 Front Black)
		(Notprintedwith sheet1 Back Black)
		(Notprintedwith sheet1 Front Color)
		(Notprintedwith sheet1 Back Color)
		(Notprintedwith sheet2 Front Black)
		(Notprintedwith sheet2 Back Black)
		(Notprintedwith sheet2 Front Color)
		(Notprintedwith sheet2 Back Color)
)
(:goal (and
		(Hasimage sheet1 Front image-1)
		(Notprintedwith sheet1 Front Black)
		(Notprintedwith sheet1 Back Black)
		(Notprintedwith sheet1 Back Color)
		(Hasimage sheet2 Front image-2)
		(Notprintedwith sheet2 Front Color)
		(Notprintedwith sheet2 Back Black)
		(Notprintedwith sheet2 Back Color)
		(Sideup sheet1 Front)
		(Sideup sheet2 Front)
		(Stackedin sheet1 sys_OutputTray)
		(Stackedin sheet2 sys_OutputTray))
)

)
