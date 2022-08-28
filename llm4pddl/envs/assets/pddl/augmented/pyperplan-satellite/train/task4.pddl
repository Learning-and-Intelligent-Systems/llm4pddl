(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	satellite1
	instrument1
	instrument2
	infrared0
	infrared1
	thermograph2
	GroundStation1
	Star0
	Star2
	Planet3
	Star4
	Planet5
	Star6
	Star7
	Phenomenon8
	Phenomenon9
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 thermograph2)
	(supports instrument0 infrared0)
	(calibration_target instrument0 Star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star6)
	(satellite satellite1)
	(instrument instrument1)
	(supports instrument1 infrared0)
	(supports instrument1 thermograph2)
	(supports instrument1 infrared1)
	(calibration_target instrument1 Star2)
	(instrument instrument2)
	(supports instrument2 thermograph2)
	(supports instrument2 infrared1)
	(calibration_target instrument2 Star2)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star0)
	(mode infrared0)
	(mode infrared1)
	(mode thermograph2)
	(direction GroundStation1)
	(direction Star0)
	(direction Star2)
	(direction Planet3)
	(direction Star4)
	(direction Planet5)
	(direction Star6)
	(direction Star7)
	(direction Phenomenon8)
	(direction Phenomenon9)
)
(:goal (and
	(pointing satellite1 Planet5)
	(have_image Planet3 infrared1)
	(have_image Star4 infrared1)
	(have_image Planet5 thermograph2)
	(have_image Star6 infrared1)
	(have_image Star7 infrared0)
	(have_image Phenomenon8 thermograph2)
	(have_image Phenomenon9 infrared0)
))

)
