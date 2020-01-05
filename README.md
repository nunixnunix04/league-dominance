# League Dominance
A python tool for analyzing a team's variable long term performance in the top 6 leagues since their inception.
The tool takes James Curley's league match data (see below) and creates an average points per game over a length of matches specified by the user. The tool works for any team that has played in the tope league of any of the following countries from the corresponding years:
* England 1888-2019
* Spain 1928-2016
* Italy 1934 - 2018
* Germany 1963 - 2016
* Portugal 1994 - 2016
* France 1932 - 2016
The years above are only restricted by the original raw data from James Curley.

## Where the data comes from:
James P. Curley (2016). engsoccerdata: English Soccer Data 1871-2016. R package version 0.1.5

URL: https://github.com/jalapic/engsoccerdata

# How to use the tool

## clean_data.py
clean_data.py is used to take the raw data csv file and standardize it for easier use with the main python tool.
This program can do/does the following:
* Removes matches from earlier years than the one specified in the *country*_settings.json file (this was used originally for troubleshooting purposes)
* Removes matches from lower divisions
* Adds a column to the csv that lists which team (Home, Away, or Draw) won the match. (This is only done if the column doesn't already exist.

The repository already comes with the formatted csv files (eg: england_1888_2016.json), but if the original data is updated or you want to use the tool for another country, use clean_data.py first to format it. Just open the file, change the variable 'country' to be the country whose data you're changing (eg: "england"), and run the program. The new csv file should be under a folder with the country's name.

## [country]_settings.json
Each country has a file called [country]_settings.py. For the 6 countries in the repository, the setting files are already made and you shouldn't have to change them. However if you want to use the tool for another country, here is what is stored in the setting files:
* The first year of the league that will be graphed
* The last year of the league that will be graphed
* The column indexes for various important columns in the formatted csv file (this is because not all the columns in the raw data files from James Curley are in the same order)
* Whether the raw data file has a column for results (this is used by clean_data.py to determine whether to add one or not)
* The number of matches per team per season in the league. This takes a while to make as it needs to list every year between the first and last year. If the number of matches is 0, it is because the league was suspended that year (eg: World War II)

## [country]_team_list.json
This file contains a dictionary of each team in the league and a true/false attached to them. Set the teams that you want to display to true so that league_dominance.py graphs them. You can add more teams to the list if they aren't on there already. Make sure you are spelling the teams the same way they appear in the raw data csv files.

## league_dominance.py
This is the main tool of the program. You must have pyplot from matplotlib installed to run this program. You can chane two settings in this file:
* The number of seasons that the program will record the point per game of. This number is then multiplied by 38 (the most common number of matches per team per season) to get the number of games it will look back on. You can edit the number of matches analyze directly by changing the 'games' variable.
* The country you are graphing. You must have the formatted csv file in a folder with that country's name for the program to run.

Once you run the program, you should get a pyplot graph pop up. The colors of each team are random. Maybe in the future I can make it so each team has a specific color, but honestly that would be a lot of work and also not helpful if you are comparing two teams with similar colors.
