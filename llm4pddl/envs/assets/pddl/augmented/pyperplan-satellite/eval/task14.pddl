(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	satellite1
	instrument1
	instrument2
	satellite2
	instrument3
	instrument4
	instrument5
	satellite3
	instrument6
	instrument7
	instrument8
	satellite4
	instrument9
	instrument10
	satellite5
	instrument11
	satellite6
	instrument12
	instrument13
	instrument14
	satellite7
	instrument15
	satellite8
	instrument16
	instrument17
	satellite9
	instrument18
	instrument19
	satellite10
	instrument20
	instrument21
	instrument22
	satellite11
	instrument23
	infrared3
	image0
	thermograph1
	image4
	infrared2
	GroundStation2
	GroundStation4
	Star1
	GroundStation0
	Star3
	Planet5
	Planet6
	Planet7
	Star8
	Phenomenon9
	Star10
	Planet11
	Planet12
	Planet13
	Phenomenon14
	Phenomenon15
	Planet16
	Phenomenon17
	Star18
	Phenomenon19
	Phenomenon20
	Star21
	Star22
	Phenomenon23
	Phenomenon24
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 infrared3)
	(calibration_target instrument0 GroundStation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet5)
	(satellite satellite1)
	(instrument instrument1)
	(supports instrument1 image0)
	(supports instrument1 infrared2)
	(calibration_target instrument1 Star3)
	(instrument instrument2)
	(supports instrument2 thermograph1)
	(supports instrument2 image0)
	(calibration_target instrument2 GroundStation0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet5)
	(satellite satellite2)
	(instrument instrument3)
	(supports instrument3 infrared3)
	(supports instrument3 infrared2)
	(calibration_target instrument3 GroundStation4)
	(instrument instrument4)
	(supports instrument4 infrared3)
	(supports instrument4 infrared2)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 GroundStation2)
	(instrument instrument5)
	(supports instrument5 thermograph1)
	(calibration_target instrument5 GroundStation4)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star21)
	(satellite satellite3)
	(instrument instrument6)
	(supports instrument6 image0)
	(supports instrument6 infrared2)
	(calibration_target instrument6 GroundStation2)
	(instrument instrument7)
	(supports instrument7 image0)
	(supports instrument7 infrared3)
	(calibration_target instrument7 GroundStation0)
	(instrument instrument8)
	(supports instrument8 infrared2)
	(supports instrument8 image4)
	(supports instrument8 image0)
	(calibration_target instrument8 GroundStation4)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star21)
	(satellite satellite4)
	(instrument instrument9)
	(supports instrument9 infrared3)
	(calibration_target instrument9 Star1)
	(instrument instrument10)
	(supports instrument10 image4)
	(supports instrument10 image0)
	(calibration_target instrument10 Star3)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star22)
	(satellite satellite5)
	(instrument instrument11)
	(supports instrument11 infrared2)
	(calibration_target instrument11 Star1)
	(on_board instrument11 satellite5)
	(power_avail satellite5)
	(pointing satellite5 GroundStation2)
	(satellite satellite6)
	(instrument instrument12)
	(supports instrument12 image4)
	(calibration_target instrument12 GroundStation0)
	(instrument instrument13)
	(supports instrument13 image4)
	(calibration_target instrument13 Star1)
	(instrument instrument14)
	(supports instrument14 thermograph1)
	(supports instrument14 infrared2)
	(calibration_target instrument14 GroundStation2)
	(on_board instrument12 satellite6)
	(on_board instrument13 satellite6)
	(on_board instrument14 satellite6)
	(power_avail satellite6)
	(pointing satellite6 Phenomenon20)
	(satellite satellite7)
	(instrument instrument15)
	(supports instrument15 image0)
	(supports instrument15 thermograph1)
	(calibration_target instrument15 GroundStation4)
	(on_board instrument15 satellite7)
	(power_avail satellite7)
	(pointing satellite7 Planet12)
	(satellite satellite8)
	(instrument instrument16)
	(supports instrument16 image0)
	(supports instrument16 infrared2)
	(calibration_target instrument16 Star1)
	(instrument instrument17)
	(supports instrument17 infrared3)
	(calibration_target instrument17 GroundStation0)
	(on_board instrument16 satellite8)
	(on_board instrument17 satellite8)
	(power_avail satellite8)
	(pointing satellite8 Phenomenon23)
	(satellite satellite9)
	(instrument instrument18)
	(supports instrument18 thermograph1)
	(supports instrument18 infrared2)
	(supports instrument18 image4)
	(calibration_target instrument18 Star1)
	(instrument instrument19)
	(supports instrument19 infrared3)
	(calibration_target instrument19 GroundStation4)
	(on_board instrument18 satellite9)
	(on_board instrument19 satellite9)
	(power_avail satellite9)
	(pointing satellite9 Phenomenon20)
	(satellite satellite10)
	(instrument instrument20)
	(supports instrument20 infrared2)
	(calibration_target instrument20 Star1)
	(instrument instrument21)
	(supports instrument21 thermograph1)
	(supports instrument21 image0)
	(calibration_target instrument21 Star1)
	(instrument instrument22)
	(supports instrument22 thermograph1)
	(calibration_target instrument22 GroundStation0)
	(on_board instrument20 satellite10)
	(on_board instrument21 satellite10)
	(on_board instrument22 satellite10)
	(power_avail satellite10)
	(pointing satellite10 Star22)
	(satellite satellite11)
	(instrument instrument23)
	(supports instrument23 infrared2)
	(supports instrument23 image4)
	(supports instrument23 thermograph1)
	(calibration_target instrument23 Star3)
	(on_board instrument23 satellite11)
	(power_avail satellite11)
	(pointing satellite11 Star8)
	(mode infrared3)
	(mode image0)
	(mode thermograph1)
	(mode image4)
	(mode infrared2)
	(direction GroundStation2)
	(direction GroundStation4)
	(direction Star1)
	(direction GroundStation0)
	(direction Star3)
	(direction Planet5)
	(direction Planet6)
	(direction Planet7)
	(direction Star8)
	(direction Phenomenon9)
	(direction Star10)
	(direction Planet11)
	(direction Planet12)
	(direction Planet13)
	(direction Phenomenon14)
	(direction Phenomenon15)
	(direction Planet16)
	(direction Phenomenon17)
	(direction Star18)
	(direction Phenomenon19)
	(direction Phenomenon20)
	(direction Star21)
	(direction Star22)
	(direction Phenomenon23)
	(direction Phenomenon24)
)
(:goal (and
	(pointing satellite1 Star22)
	(pointing satellite4 Phenomenon20)
	(pointing satellite8 Planet16)
	(have_image Planet5 image0)
	(have_image Planet6 image4)
	(have_image Planet7 image4)
	(have_image Phenomenon9 image4)
	(have_image Star10 thermograph1)
	(have_image Planet11 image4)
	(have_image Planet12 thermograph1)
	(have_image Planet13 infrared3)
	(have_image Phenomenon14 infrared2)
	(have_image Phenomenon15 infrared2)
	(have_image Planet16 infrared2)
	(have_image Phenomenon17 thermograph1)
	(have_image Star18 image4)
	(have_image Star21 thermograph1)
	(have_image Star22 image4)
	(have_image Phenomenon23 infrared3)
	(have_image Phenomenon24 infrared3)
))

)
