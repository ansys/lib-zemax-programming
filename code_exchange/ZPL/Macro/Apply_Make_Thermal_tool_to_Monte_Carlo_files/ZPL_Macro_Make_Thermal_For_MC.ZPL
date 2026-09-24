! Written 10/15/19
! This macro will emulate the Make Thermal tool for use in Monte Carlo analysis

! Input temperature data
INPUT "Enter number of configurations", configNum
! configNum	= 0		# uncomment this line and comment the above for automation
INPUT "Enter minimum temperature", minTemp
! minTemp = 0		# uncomment for automation
INPUT "Enter maximum temperature", maxTemp
! maxTemp = 0		# uncomment for automation

tempStep = (maxTemp - minTemp) / (configNum - 1)

!!!!!!!!!!!!!! Open file !!!!!!!!!!!!!!!
path$ = "C:\Documents\"
prefix$ = "MC_T"
number_of_files = 20

IF (number_of_files > 9999) THEN number_of_files = 9999

FORMAT "%#04i" LIT

FOR index, 1, number_of_files, 1		# NOTE: the "NEXT" for this loop is at the end of the macro
	suffix$ = $STR(index)
	
	myfileName$ = path$ + prefix$ + suffix$ + ".zmx"
	LOADLENS myfileName$
	

!!!!!!!!!!!!!!!! Run Make Thermal tool !!!!!!!!!!!!!!!!

	! Remove config data? Assume yes for now
	!INPUT "Delete other config data? Y/N?", del$
	del$ = "Y"

	IF (del$ $== "Y")
		FOR i, NCON(), 1, -1
			DELETECONFIG i
		NEXT
	
		FOR i, MCON(0, 0, 0), 1, -1
			DELETEMCO i
		NEXT
	ENDIF

	! Insert new configurations
	FOR i, 2, configNum + 1, 1
		INSERTCONFIG i
	NEXT

!!!!!!!!! Populate with operands !!!!!!!!!!!!
	numSurf = NSUR()

	! Pull the current system information
	GETSYSTEMDATA 2
	sysTemp = VEC2(5)
	sysPres = VEC2(6)

	! Set TEMP and PRES
	INSERTMCO 2

	SETMCOPERAND 1, 0, "TEMP", 0
	SETMCOPERAND 1, 1, sysTemp, 0	# Initial system
	SETMCOPERAND 1, 2, minTemp, 0
	tempVal = minTemp
	FOR i, 3, configNum + 1, 1
		tempVal = tempVal + tempStep
		SETMCOPERAND 1, i, tempVal, 0
	NEXT

	SETMCOPERAND 2, 0, "PRES", 0
	SETMCOPERAND 2, 1, sysPres, 0	# Initial system

	! Add CRVT, THIC, SDIA, CHZN, MCSD
	numOps = numSurf * 5

	FOR i, 3, numOps-3, 1
		INSERTMCO i
	NEXT

	surfVal = 1

	FOR i, 3, numOps - 3, 5
		! CRVT
		SETMCOPERAND i, 0, "CRVT", 0
		SETMCOPERAND i, 0, surfVal, 1
		! THIC
		SETMCOPERAND i+1, 0, "THIC", 0
		SETMCOPERAND i+1, 0, surfVal, 1
		! SDIA
		SETMCOPERAND i+2, 0, "SDIA", 0
		SETMCOPERAND i+2, 0, surfVal, 1
		! CHZN
		SETMCOPERAND i+3, 0, "CHZN", 0
		SETMCOPERAND i+3, 0, surfVal, 1
		! MCSD
		SETMCOPERAND i+4, 0, "MCSD", 0
		SETMCOPERAND i+4, 0, surfVal, 1
	
		surfVal = surfVal + 1
	NEXT

	! No glass data - they will all be pickups anyway

	! Apply thermal pickups

	FOR config, 2, configNum + 1, 1
		FOR row, 3, numOps - 3, 1
			SETMCOPERAND row, config, 3, 3
		NEXT
	NEXT

	! Update
	UPDATE ALL
	
	! Save changes
	SAVELENS

NEXT