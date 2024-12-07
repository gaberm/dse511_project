#!/bin/bash

# Download the data
echo "Hello there! Welcome to our EV data analysis project about EVs in Washington State."
echo
echo "Before we begin, we need to download the data. This will take a few seconds. Stay tuned!"
echo
echo "Downloading data..."
Rscript download_data.R
echo
echo "We have 7 exiting insights to share with you. Buckle up!"
echo

# Loop until the user selects "X"
while true; do
    echo "Please select the letter of the insight you would like to see."
    echo "A: The 10 most popular EV models"
    echo "B: The 10 least popular EV models"
    echo "C: The city with the most EVs"
    echo "D: The 10 most popular EV makers"
    echo "E: Are EVs more popular in bigger counties?"
    echo "F: Are EVs more popular in richer counties?"
    echo "G: Are EVs more popular in more urban counties?"
    echo "X: Exit"
    
    # Prompt for input
    echo ""
    read -p "Enter the letter of the insight you would like to see: " insight
    
    # Handle user input
    if [ "$insight" == "A" ]; then
        python analysis.py $insight
    elif [ "$insight" == "B" ]; then
        python analysis.py $insight
    elif [ "$insight" == "C" ]; then
        python analysis.py $insight
    elif [ "$insight" == "D" ]; then
        python analysis.py $insight
    elif [ "$insight" == "E" ]; then
        python analysis.py $insight
    elif [ "$insight" == "F" ]; then
        python analysis.py $insight
    elif [ "$insight" == "G" ]; then
        python analysis.py $insight
    elif [ "$insight" == "X" ]; then
        echo
        echo "Exiting the program. Goodbye!"
        break
    else
        echo "Invalid input. Please enter a valid letter."
    fi
done