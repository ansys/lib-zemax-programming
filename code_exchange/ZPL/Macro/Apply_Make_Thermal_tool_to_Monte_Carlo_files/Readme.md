# ZPL Macro: Apply Make Thermal tool to Monte Carlo files

## Overview

This macro allows users to apply the "Make Thermal" tool to already-generated Monte Carlo files. The amount of MC files is hard coded into the code. This will apply five Multi-Configuration operands per surface: CRVT, THIC, SDIA, CHZN, MCSD. MC operands for extra data parameters are not included for all surface types.

## Author

Alexandra Culler

## Language
ZPL

## Download
<table>

<tr>

<th>Date</th>

<th>Version</th>

<th>OpticStudio Version</th>

<th>Comment</th>

<tr>

<tr>
<td>2019/10/15</td>

<td>1.0</td>

<td>19.4SP2</td>

<td>Creation<td>
<tr>
<td>2020/08/18</td>

<td>2.0</td>

<td>20.2</td>

<td>Updates for OpticsTalk+Envision<br>

- Updates to formatting

- Addition of option to choose not to clear the MCE before applying the Make Thermal tool

- Addition of a loop which will check for the Even Asphere type. This will add parameters to the MCE which correspond to the asphere's extra data parameters

<tr>

