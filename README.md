This is a short python script that uses a decoded Fallout Shelter save file to tell you the health of each of your dwellers (along with their other stats). In-game, dweller max health is hidden and cannot be computed since it is dependant on the dwellers Endurance each time it levels up. Since increasing the endurance later does not retroactively increase the dwellers health, you can have a level 50, Endurance 10 dweller with very few hit points because it reached level 50 before it's endurance was increased.

To use this script, first ensure you have a working copy of Python 3.6 or another compatible version. Once you have installed Python, follow the steps below:

1) Find your FOS save file. It should be located in C:\Users\[YOUR USER PROFILE]\AppData\Local\FalloutShelter

2) Go to https://fossd.netlify.com/ to decrypt the save file

3) Ensure your decrypted save is named decodedsave.json and then place it in the same folder as this python script

4) Run the script either in the command line, or in IDLE.

5) Done.
