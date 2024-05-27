# NICS-3D

THIS SHOULD BE CONSIDERED AS AN ALPHA. THIS HASN'T BEEN TESTED BY USERS YET!

This is my first attempt ever at publishing code. I am not a programmer nor do I have any background in CS. I am a chemist that dabbles with coding and that wished to share the tools I have written with any who may find them to be useful. All this is to say that I CANNOT and DO NOT offer any warranty for the results you produce with it.
NICS-3D uses the “orient.py” module that was written by Shane M. Parker as part of the orient-molecule repository (https://github.com/smparker/orient-molecule/tree/master). I have made slight modifications to the output that this module produces so it will fit my code, but the rest of the code remains as it was originally written.

NICS-3D was developed by me for the use of my research group with the aim of creating 3D grids of dummy atoms around a molecule and processing the results to give a 4D matrix of the NICS values across the molecule. This tool includes a graphic user interface (GUI) and designed to work on both Linux and Windows with the intent of providing a user-friendly experience to people that prefer not to work using a terminal or command prompt.

Requirements and specifications:
1) Python 2.7.xx (I used 18).
2) The ability to run Gaussian calculations (09 or 16).
3) The numpy and matplotlib modules. You can run the “Install.bat” provided to install them.
4) All of the modules that are in the repository (“orient.py” and “extract.pyc”).

How to work with NICS-3D:
1) Run the “NICS-3D.pyw” script and in the GUI that opens use the “File->Open” to select the files you with to work with. Acceptable input files are “.com” and “.log” files. In the latter case the geometry will be taken from the last instance.
2) Go to the “Create” tab. Here you can specify the options for the files that you will create. The options are “None”, “Use parent” and “Custom”. Choosing “None” indicates causes the files to be created without this line. In “Use Parent” the value or setting are copied to each new file from the file that was used to create it. Finally, choosing “Custom” or unchecking the “Use Parent” box will make the field editable, and the values or setting that are written there will be applied to all the files that will be created.
* “Checkpoint file”: This is the pathway for the folder in which the checkpoint file for each of the calculations will be saved. If you write a custom path you need to write it in the same format your operating system writes down a full pathway. In Linux, for example, it will look something like this: “/This/Is/The/Path/I/Have/Chosen/”. In Windows, for example: “C:\Your\Choice\Of\Path\”.
* “Memory Limit (GB)”: Number (integer).
* ”Shared Processors”: Number (integer).
* “Basis/Functional”: Written down in a format that is recognizable by Gaussian, for example “b3lyp/6-31g(d)” or “cam-b3lyp/3-21g”. 
* “Charge”: Total charge, a number (integer).
* “Multiplicity”: Total multiplicity, a number (integer).
* “Grid Interval”: The spacing of the dummy atoms. Default value is 0.5 and will be used if this field remains empty (values are in Å).
* “Grid Margin”: How far beyond the bounds of the original molecule you want the grid of dummy atoms to spread. Default value is 2 and will be used if this field remains empty (values are in Å). The size of the grid is determined automatically based on the minimal and maximal coordinates on all three axes plus the margin.
* “NMR Method: (nmr=)”: The NMR method used in the calculation, in the same format you would write it in a Gaussian input file (e.g. “nmr=giao” or “nmr=csgt”). Default value is “giao” and will be used if this field remains empty.
* “Additional Input”: Any additional input or keywords that you want added to the Gaussian input files that will be created. This line is copied “as-is”, so make sure what you write is recognizable by Gaussian.
* “Suffix”: An additional suffix to be added to the name of the file that will be created.
3) Once you have launched your files will be created. Note that due to Gaussian restrictions the system will automatically split the input files it creates if the number of dummy atoms is 50,000 or more. The molecule and setting remain the same in the split files and each contains a portion of the dummy atoms. The system is configured to read and recombine these files while it extracts the data so as long as you do not change their names there shouldn’t be any issues.
4) After the calculations have finished load the results back to the NICS-3D tool and go to the “Extract” tab. From there select the mode from the drop-down menu and click on the “Launch Extraction” button. A new folder will be created in the same directory as the files you have selected, one for each unique molecule, and a csv with the results will be created there. If you wish to preview the results before you plot them mark the “Create Images” checkbox before you launch. This takes time, and the tool may appear to be frozen while the plotting is running. A progress bar should pop up to show you the status.
  
Format of csv output:
“X” “Y”	  z1	  z2	  z3  …	  zf

x1  y1	Value	Value	Value	…	Value

x1	y2	Value	Value	Value	…	Value

x2	y1	Value	Value	Value	…	Value

…	  …  	…  	  …	    …	    …	  …

x1	y1	Value	Value	Value	…	Value
