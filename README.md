This is a short python script that uses a decoded Fallout Shelter save file to tell you the health of each of your dwellers (along with their other stats). In-game, dweller max health is hidden and cannot be computed since it is dependant on the dwellers Endurance each time it levels up. Since increasing the endurance later does not retroactively increase the dwellers health, you can have a level 50, Endurance 10 dweller with very few hit points because it reached level 50 before it's endurance was increased.

To use this script, first ensure you have a working copy of Python 3.6 or another compatible version. Once you have installed Python, follow the steps below:

1) Find your FOS save file. It should be located in C:\Users\[YOUR USER PROFILE]\AppData\Local\FalloutShelter

2) Go to https://fossd.netlify.com/ to decrypt the save file

3) Ensure your decrypted save is named decodedsave.json and then place it in the same folder as this python script

4) Run the script either in the command line, or in IDLE.

5) Done.


Help:
                
                
                FOS Stat Viewer:

                    Allows you to see stats regarding your vault that would otherwise be hidden

                SYNOPSIS

                    list
                        List's all the stats

                    sort [column number] [-R]
                        Sorts stats by column number specified.


                DESCRIPTION

                    Use the List command to print a list of all dwellers and their stats in either
                    an arbitrary order, or the order previously specified by Sort.

                    Use the sort command to specify a column you want to sort by. if -R is set to 1,
                    the order will be Reversed. If it is set to anything else or not included, the order will be normal.


                    Stats:
                        Most of the stats are self explanatory, but some are not.

                        Avg. E refers to average Endurance over the course of the dweler leveling up. For
                        A dweller that leveled to 25 with an endurance of 1 and then leveled the rest of the
                        way to 50 with an endurance of 10 would have an Avg. E around 5. If the dweller's END
                        remained static as it leveled up, it's Avg. E would be the same as it's E now.
                        I computed this value to determine what dwellers have lost the most potential health points
                        so that I could remove them.

                        H/L refers to health per level. This isn't a particularly useful stat, I think Avg. E does
                        essentially the same thing better, but I had already built this and included it anyway.

                        Room refers to the room the dweller is currently in. If it says break, it could also mean exploring
                        or returning from an adventure.

                        Coords refer to the coordinates of the room that they are in if you are looking for them. The first
                        number represents the vertical coordinate, the second the horizontal.

                        The SPECIAL stats are normal, expect for the first one. The column heading is ? because I have no idea
                        what it is. For my dwellers, it was 1. Let me know if you discover it's meaning.
