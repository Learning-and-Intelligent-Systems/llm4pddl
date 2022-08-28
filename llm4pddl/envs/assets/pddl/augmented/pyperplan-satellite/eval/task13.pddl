(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	instrument1
	instrument2
	satellite1
	instrument3
	instrument4
	instrument5
	instrument6
	instrument7
	satellite2
	instrument8
	instrument9
	instrument10
	instrument11
	instrument12
	instrument13
	satellite3
	instrument14
	instrument15
	instrument16
	instrument17
	instrument18
	instrument19
	instrument20
	instrument21
	satellite4
	instrument22
	instrument23
	instrument24
	image4
	spectrograph6
	infrared2
	image5
	thermograph1
	infrared7
	spectrograph0
	infrared3
	Star1
	GroundStation4
	Star2
	Star3
	GroundStation0
	Phenomenon5
	Star6
	Phenomenon7
	Phenomenon8
	Planet9
	Star10
	Phenomenon11
	Star12
	Phenomenon13
	Star14
	Planet15
	Star16
	Planet17
	Star18
	Star19
	Phenomenon20
	Planet21
	Planet22
	Star23
	Phenomenon24
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 infrared2)
	(supports instrument0 image4)
	(calibration_target instrument0 GroundStation0)
	(instrument instrument1)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 Star3)
	(instrument instrument2)
	(supports instrument2 infrared3)
	(supports instrument2 thermograph1)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 Star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet21)
	(satellite satellite1)
	(instrument instrument3)
	(supports instrument3 thermograph1)
	(supports instrument3 image5)
	(calibration_target instrument3 Star1)
	(instrument instrument4)
	(supports instrument4 spectrograph0)
	(calibration_target instrument4 Star3)
	(instrument instrument5)
	(supports instrument5 thermograph1)
	(supports instrument5 spectrograph0)
	(supports instrument5 spectrograph6)
	(calibration_target instrument5 GroundStation4)
	(instrument instrument6)
	(supports instrument6 image5)
	(supports instrument6 infrared7)
	(calibration_target instrument6 Star3)
	(instrument instrument7)
	(supports instrument7 spectrograph6)
	(supports instrument7 thermograph1)
	(supports instrument7 spectrograph0)
	(calibration_target instrument7 Star2)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(on_board instrument6 satellite1)
	(on_board instrument7 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet21)
	(satellite satellite2)
	(instrument instrument8)
	(supports instrument8 infrared3)
	(supports instrument8 infrared7)
	(calibration_target instrument8 Star1)
	(instrument instrument9)
	(supports instrument9 spectrograph0)
	(calibration_target instrument9 Star3)
	(instrument instrument10)
	(supports instrument10 image4)
	(supports instrument10 infrared7)
	(supports instrument10 image5)
	(calibration_target instrument10 GroundStation4)
	(instrument instrument11)
	(supports instrument11 infrared2)
	(calibration_target instrument11 Star2)
	(instrument instrument12)
	(supports instrument12 thermograph1)
	(calibration_target instrument12 Star3)
	(instrument instrument13)
	(supports instrument13 infrared3)
	(calibration_target instrument13 Star2)
	(on_board instrument8 satellite2)
	(on_board instrument9 satellite2)
	(on_board instrument10 satellite2)
	(on_board instrument11 satellite2)
	(on_board instrument12 satellite2)
	(on_board instrument13 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Phenomenon5)
	(satellite satellite3)
	(instrument instrument14)
	(supports instrument14 thermograph1)
	(supports instrument14 infrared2)
	(calibration_target instrument14 GroundStation4)
	(instrument instrument15)
	(supports instrument15 infrared2)
	(calibration_target instrument15 Star1)
	(instrument instrument16)
	(supports instrument16 image4)
	(supports instrument16 spectrograph6)
	(calibration_target instrument16 Star2)
	(instrument instrument17)
	(supports instrument17 image4)
	(supports instrument17 infrared7)
	(supports instrument17 image5)
	(calibration_target instrument17 GroundStation0)
	(instrument instrument18)
	(supports instrument18 image4)
	(supports instrument18 spectrograph6)
	(calibration_target instrument18 Star2)
	(instrument instrument19)
	(supports instrument19 infrared3)
	(supports instrument19 infrared7)
	(supports instrument19 spectrograph6)
	(calibration_target instrument19 Star3)
	(instrument instrument20)
	(supports instrument20 infrared3)
	(supports instrument20 infrared2)
	(calibration_target instrument20 Star2)
	(instrument instrument21)
	(supports instrument21 infrared2)
	(supports instrument21 thermograph1)
	(calibration_target instrument21 GroundStation4)
	(on_board instrument14 satellite3)
	(on_board instrument15 satellite3)
	(on_board instrument16 satellite3)
	(on_board instrument17 satellite3)
	(on_board instrument18 satellite3)
	(on_board instrument19 satellite3)
	(on_board instrument20 satellite3)
	(on_board instrument21 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon20)
	(satellite satellite4)
	(instrument instrument22)
	(supports instrument22 thermograph1)
	(supports instrument22 image5)
	(calibration_target instrument22 Star2)
	(instrument instrument23)
	(supports instrument23 infrared7)
	(supports instrument23 thermograph1)
	(calibration_target instrument23 Star3)
	(instrument instrument24)
	(supports instrument24 infrared3)
	(supports instrument24 spectrograph0)
	(calibration_target instrument24 GroundStation0)
	(on_board instrument22 satellite4)
	(on_board instrument23 satellite4)
	(on_board instrument24 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star14)
	(mode image4)
	(mode spectrograph6)
	(mode infrared2)
	(mode image5)
	(mode thermograph1)
	(mode infrared7)
	(mode spectrograph0)
	(mode infrared3)
	(direction Star1)
	(direction GroundStation4)
	(direction Star2)
	(direction Star3)
	(direction GroundStation0)
	(direction Phenomenon5)
	(direction Star6)
	(direction Phenomenon7)
	(direction Phenomenon8)
	(direction Planet9)
	(direction Star10)
	(direction Phenomenon11)
	(direction Star12)
	(direction Phenomenon13)
	(direction Star14)
	(direction Planet15)
	(direction Star16)
	(direction Planet17)
	(direction Star18)
	(direction Star19)
	(direction Phenomenon20)
	(direction Planet21)
	(direction Planet22)
	(direction Star23)
	(direction Phenomenon24)
)
(:goal (and
	(pointing satellite0 Planet17)
	(have_image Phenomenon5 infrared7)
	(have_image Phenomenon5 image4)
	(have_image Phenomenon7 thermograph1)
	(have_image Planet9 spectrograph0)
	(have_image Planet9 spectrograph6)
	(have_image Star10 infrared3)
	(have_image Star10 spectrograph6)
	(have_image Phenomenon11 infrared2)
	(have_image Star12 spectrograph6)
	(have_image Star12 thermograph1)
	(have_image Phenomenon13 infrared7)
	(have_image Phenomenon13 infrared2)
	(have_image Star14 infrared2)
	(have_image Planet15 infrared2)
	(have_image Star16 image4)
	(have_image Planet17 image5)
	(have_image Planet17 image4)
	(have_image Star18 infrared2)
	(have_image Star19 infrared3)
	(have_image Star19 thermograph1)
	(have_image Phenomenon20 spectrograph0)
	(have_image Planet21 infrared3)
	(have_image Planet21 image5)
	(have_image Planet22 infrared2)
	(have_image Star23 infrared2)
	(have_image Phenomenon24 spectrograph6)
	(have_image Phenomenon24 image5)
))

)
