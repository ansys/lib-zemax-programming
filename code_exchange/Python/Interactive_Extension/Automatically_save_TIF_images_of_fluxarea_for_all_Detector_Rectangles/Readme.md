# Automatically save TIF images of flux/area for all Detector Rectangles

## Overview

An Interactive Extension was created that will automatically save flux/area data of all Detector Rectangles to TIF images having double data type. This follows a post(https://community.zemax.com/people-pointers-9/detector-viewers-to-different-image-formats-8-16-bits-with-a-user-extension-850) from David Nguyen and support feedback from Sandrine Auriol and Alexandra Culler,

Script was tested with Samples\Short course\Illumination & Stray Light\Double Gauss for Sun Shield.zos. The images "Double Gauss for Sun Shield, Field 1, D11.tif" and "Double Gauss for Sun Shield, Field 1, D12.tif" were created, then opened using ImageJ(https://imagej.nih.gov/ij/download.html).  The images will be uninteresting unless rays are traced before the extension is run.

LoopOverAndSaveDDRs(TheSystem) is in a separate file from the Interactive Extension boilerplate so that it could also be used from a Standalone Application, though this has not yet been tested.

## Author

Stev Boege

## Download
<table>

<tr>

<th>Date</th>

<th>Version</th>

<th>OpticStudio Version</th>

<th>Comment</th>

<tr>

<tr>
<td>2021/11/01</td>

<td>1.0</td>

<td>-</td>

<td>Creation<td>
<tr>


