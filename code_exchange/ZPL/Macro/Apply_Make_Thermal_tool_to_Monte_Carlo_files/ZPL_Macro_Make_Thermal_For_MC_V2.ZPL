!!!!!!!!!!!!! Step 1 - Enter number of configs + min&max temp !!!!!!!!!!!!!!!!
! Input temperature data
INPUT "Enter number of configurations", configNum		# Number of configurations
INPUT "Enter minimum temperature", minTemp				# Min temperature
INPUT "Enter maximum temperature", maxTemp				# Max temperature
! The max and min temps will be used to determine the temp for each config
tempStep = (maxTemp - minTemp) / (configNum - 1)


!!!!!!!!!!!!! Step 2 - Define what MC files to analyze !!!!!!!!!!!!!!!!
! Set up the titles of the MC files which will be opened
path$ = "C:\Users\Alexandra.Culler\Desktop\Tutorial Run Throughs\Training\Advanced ZPL OpticsTalk\"
prefix$ = "MC_T"
number_of_files = 20
IF (number_of_files > 9999) THEN number_of_files = 9999
! Format the values so that the numbers are 4-value integers
FORMAT "%#04i" LIT


!!!!!!!!!!!!! Step 3 - Open an MC file for editing !!!!!!!!!!!!!!!!
FOR index, 1, number_of_files, 1	
	! Convert the index value to a string
	suffix$ = $STR(index)
	myfileName$ = path$ + prefix$ + suffix$ + ".zmx"
	LOADLENS myfileName$
	

	!!!!!!!!!!!!! Step 4 - Clear the MC Editor !!!!!!!!!!!!!!!!
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


	!!!!!!!!!!!!! Step 5 - Insert new configurations !!!!!!!!!!!!!!!!
	! Insert new configurations
	FOR i, 2, configNum + 1, 1
		INSERTCONFIG i
	NEXT


	!!!!!!!!!!!!! Step 6 - Apply the standard operands !!!!!!!!!!!!!!!!
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
	
	
	! Check for Even Aspheres
	! Each Even Asphere will have 8 extra data parameters
	numSurf = NSUR()
	FOR surf, 1, numSurf, 1
		dummy = SPRO(surf,0)
		surfType$ = $buffer()
		IF (surfType$ $== "EVENASPH")
			numOps = numOps + 8
			FOR param, 1, 8, 1
				INSERTMCO param + 3
				SETMCOPERAND param + 3, 0, "PRAM", 0
				SETMCOPERAND param + 3, 0, surf, 1
				SETMCOPERAND param + 3, 0, param, 2
			NEXT
		ENDIF
	NEXT


	!!!!!!!!!!!!! Step 7 - Apply the Thermal Pickup solves !!!!!!!!!!!!!!!!
	FOR config, 2, configNum + 1, 1
		FOR row, 3, numOps - 3, 1
			SETMCOPERAND row, config, 3, 3
		NEXT
	NEXT


	!!!!!!!!!!!!! Step 8 - Update the lens and save the output !!!!!!!!!!!!!!!!
	! Update
	UPDATE ALL
	! Save changes
	SAVELENS

NEXT