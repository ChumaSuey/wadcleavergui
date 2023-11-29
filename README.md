# WADCleaver GUI

This is a GUI (Graphical User Interface) for the python script by Nickster called WADCleaver, that aims to provide a graphical interface for the wad chopper itself.

WADCleaver aims to cut/chop/cleave Makkon's custom textures for Quake for easier use for those interested 

Referencial links:
- Makkon's Textures : https://www.slipseer.com/index.php?resources/makkon-textures.28/
- WADCleaver: https://www.slipseer.com/index.php?resources/wadcleaver.268/


## How to run it and what does is it require?

As i'm a very graphical and methodical when it comes to tools, i've always been running the script on Pycharm, but an executable was basically made, the options are as follows:

- You can download the script from the repository or the release and run it.
- You can also download the executable RAR (this should be with all the source code of this version).


It's required :
- Python 3.11 on your computer ( i think from version 3 can work).
- TKinter (install it from the CMD/Powershell).

"pip install tk" on CMD / Powershell should work. (at least for Windows)

## Instructions on how to use it the script (GUI).

![image](https://github.com/ChumaSuey/wadcleavergui/assets/3680154/dc654320-4d00-494d-a0d2-dac67b56ee9e)

1. Select the wad file : This will allow you to find the wad file you want to chop, once done press the button "Select file"

2. Select the folder to save the separated WADs : You will find the direction you wanna save the WAD files, but this function generates a folder, so at the end of the line, make sure to name the folder that will generate the chopped wads, f.e "C:/Users/Desktop/makkonnewstuff" in this case we are saving in our desktop, but makkonnewstuff will be the folder with the chopped wads per se, after all of this is done, press "Select Directory" [Note: The Reminder says what i basically said here].

3. Once the wad is found and the directory is selected, just press the button "Generate WAD".

Extras functions per se:

- Delimiter : Will work on telling how the wad is or will be delimited, by default is "_".

- Token : It will organize the wad depending on the values given.

For using these values, just before step 3, put the number in the white field (Entry).
## Notes

Not much to say as the script is simple, i'd extend on the Delimiter and Token functions but it's a topic within WADCleaver's original code.

[Note from nickster] If you run into the following error using the Linux executable...

    FileNotFoundError: [Errno 2] No such file or directory: 'python'

...you may be able to fix this by running the following command in the terminal; it has to do with how the Python executable is named in Linux:

    sudo apt install python-is-python3


[Note about the script]: A Linux executable was made by Nepta, and the note above from Nickster is just a small fix for a nuance... it works on Linux.

[Note about the branch]: There's a branch where i experimented switching from .pack to .grid, i didn't like much the end result, but i left it there, it should work executing the code... but it's a "spinoff" the master branch will be the only one updated and treated in the future.

[Note about future releases]: The script may need some polishing in the placements of the labels, entry fields, and others but the script is fully functional, so using it would be almost the same case, just some different graphics, i'll change the picture if we get to do a major change.

## Credits

Programmers:
- Chuma.
- Nepta.
co crediting my small freelance development team:
- Absolute Quantum (AQ), shoutout to Dany for testing the script and feedback.

Original script creator:
- Nickster.

Original Texture maker and artist extraordinare:
- Makkon.

Special thanks for Feedback:
- 4LT.
- PixelKiri.

Tools used:
- Python
- tkinter
- Makkon's Textures
- WADCleaver
