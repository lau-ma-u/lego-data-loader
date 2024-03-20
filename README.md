An app for batch loading information about Lego sets and the MOCs ("My Own Creation") of those sets. 
Uses Rebrickable and Brickset APIs.
Takes a .csv file containing Lego set numbers as input.
Creates a .csv file containing info about the Lego sets. Also creates separate .csv files for listing the MOCs of every set. 
Finally creates a .png file containing some plots derived from the gathered data.

You will need API keys to the following:
* Rebrickable
* Brickset

Input: my_lego_sets.csv

Output: lego_info.csv, lego_plots.png and for every set {SET_NUMBER}-MOCs.csv


Development ideas:
* Enable controlling the program with user input.
