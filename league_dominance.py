import csv
import json
from matplotlib import pyplot as plt

# SETTINGS
country = "germany"
seasons = 5

# Autofilled settings loaded from json file
games = 38 * seasons
settings_file_name = country + "_settings.json"
teams_file_name = country + "_team_list.json"
with open(country + "/" + settings_file_name) as fset:
	settings = json.load(fset)
starting_year = settings["starting_year"] # First season of the dataset
latest_year = settings["latest_year"] # Last season of the dataset
data_file_name = country + "_" + str(starting_year) + "_" + str(latest_year) + ".csv" # Filename of dataset
date_index = settings["date_index"]
year_index = settings["year_index"]
home_team_index = settings["home_team_index"]
away_team_index = settings["away_team_index"]
result_index = settings["result_index"]


class Team():
	# Creates necessary information for each team
	def __init__(self, team, reader):
		self.team = team
		self.reader = reader
		self.matches = self.get_list_of_matches()
		self.points_per_match_list = self.get_points_per_match_list()
		self.points_total_list = self.get_points_total_list()
		self.points_average_list = self.get_points_average_list()

	# Creates a list with each match row from the data set pertaining to the team
	def get_list_of_matches(self):
		list_of_matches = []
		for row in self.reader:
			# Appends row to team match list if team appears Home or Away
			if (self.team == row[home_team_index]):
				row.append("H")
				list_of_matches.append(row)
			elif (self.team == row[away_team_index]):
				row.append("A")
				list_of_matches.append(row)
		# Sorts the match list based on the date it was played
		list_of_matches_sorted = sorted(list_of_matches, key=lambda x: x[date_index])
		return list_of_matches_sorted

	# Makes a list with the points earned per match starting from 1888
	def get_points_per_match_list(self):
		points_per_match_list = []
		# Goes through each season
		for year in range(starting_year,latest_year+1):
			in_top_division = False
			# Goes through each match
			for match in self.matches:
				# If the match was played the same year, it adds the points earned
				if int(match[year_index]) == year:
					in_top_division = True
					if match[result_index] == "D":
						points_per_match_list.append(1)
					elif match[result_index] == match[-1]:
						points_per_match_list.append(3)
					else:
						points_per_match_list.append(0)
			# If the team was not in the top division that season, it appends an empty element
			# for every match that would have happened that season
			if not in_top_division:
				for i in range(settings[str(year)]):
					points_per_match_list.append(None)
		return points_per_match_list

	def get_points_total_list(self):
		points_total_list = []
		# Sums up the last games amount of points earned for each gameweek
		for i in range(len(self.points_per_match_list)):
			if (i < games):
				points_total_list.append(sum(filter(None,self.points_per_match_list[0:i])))
			else:
				points_total_list.append(sum(filter(None,self.points_per_match_list[i-games:i])))
		return points_total_list

	# Averages the points sum list by the number of games involved so as to standardize the data
	def get_points_average_list(self):
		points_average_list = []
		for i in range(len(self.points_total_list)):
			if (i < games):
				points_average_list.append(self.points_total_list[i]/(i+1))
			else:
				points_average_list.append(self.points_total_list[i]/(games))
		return points_average_list

	# Prints a row for each match from that team
	def print_list_of_matches(self):
		for match in self.matches:
			print(match)

# Loads list of teams that will be loaded and plotted
with open(country + "/" + teams_file_name) as ftl:
	team_list = json.load(ftl)

# Creates team object for every team on the team list
league = {}
for team in team_list.keys():
	if team_list[team]:
		with open(country + "/" + data_file_name) as f:
			reader = csv.reader(f)
			league[team] = Team(team, reader)

# Plotting begins
fig = plt.figure(dpi=64, figsize=(20,12))
# If team is set to true in team list, its PPG is plotted
for team in team_list.keys():
	if team_list[team]:
		plt.plot(league[team].points_average_list, alpha=0.8, label=team, linewidth=2)


matches_count = 0
matches_count_list = [0]
years_list = []
# Makes light grey vertical line for beginning of every season
for year in range(starting_year,10*(int(latest_year/10)+1)+1):
	matches_in_season = settings[str(year)]
	matches_count += matches_in_season
	matches_count_list.append(matches_count)
	years_list.append(year)
	# Skips war years unless its a multiple of 10
	if not str(year)[-1:] == "0" and settings[str(year)] == 0:
		pass
	else:
		plt.axvline(x=matches_count_list[year-starting_year], c = "black", alpha = 0.1)
		# If the year is a multiple of ten, it creates a darker vertical line
		if str(year)[-1:] == "0":
			plt.axvline(x=matches_count_list[year-starting_year], c = "black", alpha = 0.4)

# Creates tick mark for every 10 seasons
year_skip = 10 - starting_year%10
plt.xticks(matches_count_list[year_skip::10], years_list[year_skip::10])
# plt.axis([0,matches_count_list[-1],0,2.6]) # Use this to change the vertical bound limits on the graph
# Gives plot a title, labels, and a legend
plt.title("Points per game over a " + str(seasons) + "-year period", fontsize=20)
plt.xlabel("Year", fontsize=16)
plt.ylabel("Points per game", fontsize=16)
plt.legend()
plt.show()