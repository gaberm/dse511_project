# DSE511 Final Project

This is the final project for **DSE 511 - Introduction to Data Science and Computing**. The project aims to demonstrate the use of various programming languages and tools covered during the semester, including **R**, **Python**, **SQL**, **Bash**, and **Web Scraping**. 

While the approach focuses on meeting the project requirements, it may not represent the most efficient solution to the problem. For example, a dataset is web scraped instead of being downloaded directly.

## Problem

The adoption of **electric vehicles (EVs)** is a crucial step in achieving climate goals globally. However, the adoption rate is slower than desired in many countries. Policymakers need a better understanding of the factors behind this lagging adoption to adjust regulatory frameworks effectively.

## Data

The project utilizes four datasets related to EV adoption in Washington State:

1. **EV Data**: All registered electric and plug-in hybrid vehicles in the state.
2. **County Income Data**: The median household income for every ZIP code.
3. **County Area Data**: The land area of every county.
4. **ZIP Code Population Data**: The population of each ZIP code.

## Approach

1. **Data Acquisition**:  
   Data is collected using a combination of downloading and web scraping with **R**:

2. **Data Analysis**:  
   The data is analyzed using **Python** and **SQL**:
   - Plug-in hybrids are excluded to focus solely on EVs.
   - The datasets are merged into a single dataframe.
   - SQL queries are used to extract and compute insights from the data.
   - A total of **seven insights** are generated, three of which include graphical visualizations.

3. **Interactive Presentation**:  
   A **Bash** script (`main.sh`) allows users to explore insights interactively via the terminal.

4. **Results and Discussion**
Using regression analysis, we found that EV adoption per capita has the strongest correlation with population density, as indicated by the highest $R^{2}$ value. This correlation surpasses that observed between EV adoption per capita and other factors, such as household income or total population. To enhance EV adoption rates, it may be beneficial to focus on making EVs more appealing to rural communities, potentially by improving charging infrastructure in these areas.