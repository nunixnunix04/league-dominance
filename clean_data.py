import csv
import json

# SETTINGS
country = "england"

# Autofilled settings from json file
raw_data_file_name = country + ".csv"
settings_file_name = country + "_settings.json"
with open(country + "/" + settings_file_name) as fset:
	settings = json.load(fset)
starting_year = settings["starting_year"] # First season of the dataset
latest_year = settings["latest_year"] # Last season of the dataset
# Column indexes
date_index = settings["date_index"]
year_index = settings["year_index"]
home_goals_index = settings["home_goals_index"]
away_goals_index = settings["away_goals_index"]
division_index = settings["division_index"]
has_result_index = settings["has_result_index"]

def remove_old_seasons(raw_rows):
	raw_rows_1 = raw_rows[1:]
	count = 0
	for i in range(1, len(raw_rows)):
		if int(raw_rows[i][year_index]) < starting_year or int(raw_rows[i][year_index]) > latest_year:
			del raw_rows_1[i-count-1]
			count += 1
	return raw_rows_1

def remove_lower_division(raw_rows_1):
	raw_rows_2 = raw_rows_1[:]
	count = 0
	for i in range(0, len(raw_rows_1)):
		if not raw_rows_1[i][division_index] ==  "1":
			del raw_rows_2[i-count]
			count += 1
	return raw_rows_2

def get_match_result(raw_rows_3):
	raw_rows_3 = raw_rows_2[:]
	raw_rows_3[0].append("result")
	for row in raw_rows_3[1:]:
		if row[home_goals_index] > row[away_goals_index]:
			row.append("H")
		elif row[home_goals_index] < row[away_goals_index]:
			row.append("A")
		else:
			row.append("D")
	return raw_rows_3

def print_matches_per_season(raw_rows_3):
	for season in range(starting_year,latest_year):
		matches = 0
		for i in range(1, len(raw_rows_3)):
			if int(raw_rows_2[i][year_index]) == season:
				matches += 1
		print(str(season) + ": " + str(matches) + " matches")

with open(country + "/" + raw_data_file_name) as f:
	reader = csv.reader(f)
	raw_rows = [r for r in reader]
	raw_rows_1 = remove_old_seasons(raw_rows)
	raw_rows_2 = remove_lower_division(raw_rows_1)
	if has_result_index:
		raw_rows_3 = raw_rows_2
	else:
		raw_rows_3 = get_match_result(raw_rows_2)
	raw_rows_4 = sorted(raw_rows_3, key=lambda x: x[date_index])
	with open(country + "/" + str(country) + "_" + str(starting_year) + "_" + str(latest_year) + ".csv","w", newline="") as new_f:
		writer = csv.writer(new_f)
		writer.writerows(raw_rows_4)
