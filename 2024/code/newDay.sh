#!/bin/bash

# Allows the file to be executed anywhere (resolves the path to the file's path rather than the executioner's path)
# Thanks to https://stackoverflow.com/a/24112741
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Checks if it's during the Advent of Code season
if [[ $(date +%m) -ne 12 || $(date +%e) -gt 26 ]]; then
	echo "This script should only be run during the Advent of Code!"
	exit 1
fi

# Gets the current day
day=$( date +%d )
dayNoZero=$( date +%-d )

# Checks if the day was already created
if [ -d "Day$day/" ]; then
	echo "Day$day/ already exists!"
	exit 1
fi

# Copies the template
cp -r "Template/" "Day$day/"
echo "Created Day$day/"

# Creates the symbolic link for today
if [ -d "current" ]; then
	rm current
fi
ln -s "Day$day" "current"
echo "Linked Day$day/ to current/"

# Adds it to the year's README
echo "| [Day $dayNoZero: XXXXX](notes/day$day.md) |        |        |       |" >> ../README.md
echo "Added this Day$dayNoZero to the year's README"

echo "Good luck!"

