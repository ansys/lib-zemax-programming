# Python: Use the ZOS-API to assign Multiphysics Datasets automatically! Example script provided

## Overview

 was at the SPIE Optics & Photonics conference a couple weeks ago and a few people asked me about automatically assigning datasets to surfaces with STAR. There are a lot of cases that we have to look into to provide that reliably so it's taking some time due to our other projects. That being said, this is a great opportunity to use the ZOS-API to make life easier!

I have attached a simple script that handles the straightforward case of assigning the datasets to the surfaces and saving a new file. 

MAJOR caveats are: 

I am not a developer. As such, there may be bugs/cases where this script doesn't work.
This script is provided to serve as a guide for you to make it your own.

You must change to extension from ".txt." to ".py"

You need to provide:

 (1) A Path to the ZMX file that you want to add the datasets to

 (2) A Path to the folder where the multiphysics datasets are located

Assumptions made with this script:

 (1) The multiphysics filenames were generated with or are in the naming format that are exported

     using the Export to STAR extension ("Surface_02_Deformation_2.txt")  https://optics.ansys.com/hc/en-us/articles/42661746128787-STAR-Tools-in-OpticStudio-Ansys-Mechanical-Data-Export-Extension

 (2) The coordinate system that the datasets are saved with respect to the global coordinate reference surface in the OpticStudio file i.e. they are in the global coordinate system

## Author
Esteban Carbajal

