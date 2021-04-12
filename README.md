# iTunes-File-Compiler
This takes all the .mp3 files in my iTunes Library and compiles them into one single location, with the file names and ID3 tags altered to be what they are listed as on iTunes.
Note that this program only functions with mp3 files, as that is all I have in my iTunes library.

The .py file contains my code. It requires the user to export their iTunes library through the iTunes program, using File>Library>Export Library.
This will generate an .xml file called Library.xml
The user must then convert this to a .plist file by making a copy and saving it as such.
The Library.xml and Library.plist files found here are the ones I have used, they correspond to my iTunes library and so will not work on any other device. I uploaded them merely as example.

You must edit the Python code to tell it where you want it to search for MP3 files, and where you want to export the copies to.
