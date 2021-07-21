Attribute VB_Name = "Module2"
Sub Main()
'makes grid files for surveys 3d (franks3)files
	Dim SurferApp As Object
	Dim InFile As String
	Dim OutFile As String
	Dim finA As String
	Dim retValue As Boolean

	On Error Resume Next

	file1 = "C:\Scratch\InputFiles.dat"
	Open file1 For Input As #1
	Input #1, finA, lsMin, lsMax, xsMin, xsMAx, ncol, nrow, path
	Close #1

	'Creates an instance of the Surfer Application object and assigns it to the variable named "SurferApp"
	Set SurferApp = CreateObject("Surfer.Application")
	SurferApp.Visible = False

'    On Error GoTo X

	InFile =  path + finA
	OutFile=  path + finA + "_grid.txt"

 
	''Grids the specified data file using the Kriging algorithm and assigns the return value To the variable named "retValue"
	''ASCII col 6,7=state plane  8,9=FRF coords
	retValue = SurferApp.GridData(DataFile:=InFile, Algorithm:=srfKriging,  _
		ShowReport:=False, OutGrid:=OutFile, OutFmt:=srfGridFmtXYZ, _
		ymax:=lsMax, ymin:=lsMin, _
		xmin:=xsMin, xmax:=xsMax, _
		NumCols:=ncol , NumRows:=nrow, _
		xcol:=8, ycol:=9, zcol:=10)

	''binary  col 6,7=state plane  8,9=FRF coords
	'retValue = SurferApp.GridData(DataFile:=InFile, Algorithm:=srfKriging, _
	'	ShowReport:=False, OutGrid:=OutFile, _
	'	ymax:=lsMax, ymin:=lsMin, _
	'	xmin:=xsMin, xmax:=xsMax, _
	'	NumCols:=ncol , NumRows:=nrow, _
	'	xcol:=6, ycol:=7, zcol:=10)



X:  Exit Sub

End Sub
