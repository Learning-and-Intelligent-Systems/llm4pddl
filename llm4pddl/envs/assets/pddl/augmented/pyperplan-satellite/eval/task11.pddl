(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	instrument1
	satellite1
	instrument2
	instrument3
	satellite2
	instrument4
	instrument5
	satellite3
	instrument6
	satellite4
	instrument7
	instrument8
	instrument9
	satellite5
	instrument10
	instrument11
	instrument12
	satellite6
	instrument13
	instrument14
	instrument15
	satellite7
	instrument16
	instrument17
	instrument18
	image1
	infrared0
	thermograph3
	spectrograph2
	thermograph4
	Star3
	GroundStation0
	GroundStation2
	Star1
	Star4
	Phenomenon5
	Planet6
	Planet7
	Star8
	Phenomenon9
	Phenomenon10
	Planet11
	Star12
	Star13
	Planet14
	Star15
	Phenomenon16
	Planet17
	Star18
	Star19
	Planet20
	Planet21
	Planet22
	Planet23
	Planet24
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 thermograph4)
	(supports instrument0 image1)
	(calibration_target instrument0 GroundStation0)
	(instrument instrument1)
	(supports instrument1 spectrograph2)
	(supports instrument1 thermograph3)
	(calibration_target instrument1 Star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star19)
	(satellite satellite1)
	(instrument instrument2)
	(supports instrument2 spectrograph2)
	(calibration_target instrument2 Star4)
	(instrument instrument3)
	(supports instrument3 image1)
	(supports instrument3 spectrograph2)
	(calibration_target instrument3 GroundStation2)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star18)
	(satellite satellite2)
	(instrument instrument4)
	(supports instrument4 thermograph3)
	(supports instrument4 thermograph4)
	(supports instrument4 spectrograph2)
	(calibration_target instrument4 Star1)
	(instrument instrument5)
	(supports instrument5 thermograph3)
	(supports instrument5 image1)
	(supports instrument5 infrared0)
	(calibration_target instrument5 GroundStation2)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star19)
	(satellite satellite3)
	(instrument instrument6)
	(supports instrument6 spectrograph2)
	(supports instrument6 infrared0)
	(calibration_target instrument6 GroundStation2)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star4)
	(satellite satellite4)
	(instrument instrument7)
	(supports instrument7 thermograph3)
	(supports instrument7 spectrograph2)
	(calibration_target instrument7 Star3)
	(instrument instrument8)
	(supports instrument8 image1)
	(calibration_target instrument8 GroundStation2)
	(instrument instrument9)
	(supports instrument9 infrared0)
	(calibration_target instrument9 Star3)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Phenomenon9)
	(satellite satellite5)
	(instrument instrument10)
	(supports instrument10 thermograph4)
	(supports instrument10 spectrograph2)
	(supports instrument10 infrared0)
	(calibration_target instrument10 GroundStation0)
	(instrument instrument11)
	(supports instrument11 infrared0)
	(calibration_target instrument11 GroundStation0)
	(instrument instrument12)
	(supports instrument12 infrared0)
	(calibration_target instrument12 Star1)
	(on_board instrument10 satellite5)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(power_avail satellite5)
	(pointing satellite5 Planet6)
	(satellite satellite6)
	(instrument instrument13)
	(supports instrument13 thermograph3)
	(supports instrument13 infrared0)
	(calibration_target instrument13 Star3)
	(instrument instrument14)
	(supports instrument14 spectrograph2)
	(calibration_target instrument14 GroundStation2)
	(instrument instrument15)
	(supports instrument15 thermograph4)
	(calibration_target instrument15 GroundStation0)
	(on_board instrument13 satellite6)
	(on_board instrument14 satellite6)
	(on_board instrument15 satellite6)
	(power_avail satellite6)
	(pointing satellite6 Planet17)
	(satellite satellite7)
	(instrument instrument16)
	(supports instrument16 thermograph4)
	(calibration_target instrument16 GroundStation2)
	(instrument instrument17)
	(supports instrument17 spectrograph2)
	(calibration_target instrument17 Star1)
	(instrument instrument18)
	(supports instrument18 thermograph4)
	(calibration_target instrument18 Star4)
	(on_board instrument16 satellite7)
	(on_board instrument17 satellite7)
	(on_board instrument18 satellite7)
	(power_avail satellite7)
	(pointing satellite7 Planet11)
	(mode image1)
	(mode infrared0)
	(mode thermograph3)
	(mode spectrograph2)
	(mode thermograph4)
	(direction Star3)
	(direction GroundStation0)
	(direction GroundStation2)
	(direction Star1)
	(direction Star4)
	(direction Phenomenon5)
	(direction Planet6)
	(direction Planet7)
	(direction Star8)
	(direction Phenomenon9)
	(direction Phenomenon10)
	(direction Planet11)
	(direction Star12)
	(direction Star13)
	(direction Planet14)
	(direction Star15)
	(direction Phenomenon16)
	(direction Planet17)
	(direction Star18)
	(direction Star19)
	(direction Planet20)
	(direction Planet21)
	(direction Planet22)
	(direction Planet23)
	(direction Planet24)
)
(:goal (and
	(pointing satellite0 Star19)
	(pointing satellite1 Planet22)
	(pointing satellite2 Star13)
	(pointing satellite3 Planet14)
	(pointing satellite5 Planet24)
	(pointing satellite7 Star3)
	(have_image Phenomenon5 spectrograph2)
	(have_image Planet6 spectrograph2)
	(have_image Planet7 infrared0)
	(have_image Phenomenon9 infrared0)
	(have_image Phenomenon10 image1)
	(have_image Planet11 image1)
	(have_image Star12 thermograph3)
	(have_image Star13 thermograph3)
	(have_image Planet14 thermograph4)
	(have_image Star15 thermograph4)
	(have_image Phenomenon16 image1)
	(have_image Planet17 thermograph3)
	(have_image Star18 image1)
	(have_image Planet20 image1)
	(have_image Planet21 infrared0)
	(have_image Planet22 image1)
	(have_image Planet23 thermograph3)
	(have_image Planet24 infrared0)
))

)
