import argparse
import pandas as pd
from pandasql import sqldf
import os
import matplotlib.pyplot as plt
from scipy.stats import linregress

def main(arg):
    # Load the data from files
    ev_df = pd.read_csv("data/ev.csv")
    ev_df["County"] = ev_df["County"] + " County"
    ev_df = ev_df[~ev_df["Postal Code"].isna()] # drop 5 rows with missing postal codes
    ev_df["Postal Code"] = ev_df["Postal Code"].astype(int)
    ev_df = ev_df[ev_df["Electric Vehicle Type"] == "Battery Electric Vehicle (BEV)"]
    pop_df = pd.read_csv("data/population.csv")
    income_df = pd.read_csv("data/household_income.csv")
    area_df = pd.read_csv("data/area.csv")

    # Merge the data
    merged_df = pd.merge(ev_df, pop_df, on="Postal Code")
    merged_df = pd.merge(merged_df, income_df, on="Postal Code")
    merged_df = pd.merge(merged_df, area_df, on="County")

    # Most popular EV models
    if arg == "A":
        query = "SELECT Make, Model, COUNT(*) FROM merged_df GROUP BY Make, Model ORDER BY COUNT(*) DESC"; 
        df = sqldf(query, locals())
        os.system("echo")
        os.system("echo 'The 10 least popular EV models (based on the number of registered cars) in the state of Washington are:'")
        for i in range(10):
            os.system(f"echo '{i+1}. {df.iloc[i, 0].capitalize()} {df.iloc[i, 1].title()}: {df.iloc[i, 2]}'")
        os.system("echo")

    # Least popular EV models
    elif arg == "B":
        query = "SELECT Make, Model, COUNT(*) FROM merged_df GROUP BY Make, Model ORDER BY COUNT(*) DESC"; 
        df = sqldf(query, locals())
        l = len(df)
        os.system("echo")
        os.system("echo 'The 10 least popular EV models (based on the number of registered cars) in the state of Washington are:'")
        for i in range(10):
            os.system(f"echo '{l-10+i}. {df.iloc[(-10+i), 0].capitalize()} {df.iloc[(-10+i), 1].title()}: {df.iloc[(-10+i), 2]}'")
        os.system("echo")

    # City with the most EVs
    elif arg == "C":
        query = "SELECT City, COUNT(*) FROM merged_df ORDER BY COUNT(*) DESC"
        df = sqldf(query, locals())
        os.system(f"echo '\nThe city with the most registered EVs in the state of Washington is {df.iloc[0, 0]} with {df.iloc[0, 1]} cars. Can you figure out why?\n'")

    # Most popular EV makers
    elif arg == "D":
        query = "SELECT Make, COUNT(*) FROM merged_df GROUP BY Make ORDER BY COUNT(*) DESC"; 
        df = sqldf(query, locals())
        os.system("echo")
        os.system("echo 'The 10 most popular EV makers (based on the number of registered cars) in the state of Washington are:'")
        for i in range(10):
            os.system(f"echo '{i+1}. {df.iloc[i, 0].capitalize()}: {df.iloc[i, 1]}'")
        os.system("echo")

    # EVs per capita
    elif arg == "E":
        query = 'SELECT County, COUNT(*) AS "EV" FROM merged_df GROUP BY County ORDER BY COUNT(*) DESC'
        ev_per_county = sqldf(query, locals())
        
        query = 'SELECT County, Sum(Population) AS "Population" FROM (SELECT DISTINCT "Postal Code", County, Population FROM merged_df) GROUP BY County'
        county_pop = sqldf(query, locals())

        df = pd.merge(ev_per_county, county_pop, on="County")
        df["EV per Capita"] = df["EV"] / df["Population"] * 1000

        plt.scatter(df["Population"], df["EV per Capita"])
        plt.xlabel("Population (in Millions)")
        plt.ylabel("EVs per csapita (per 1000 people)")
        plt.title("Number of EVs vs Population by County")

        slope, intercept, r_value, p_value, _ = linregress(df["Population"], df["EV per Capita"])
        plt.plot(df["Population"], intercept + slope * df["Population"], 'r', label=f'R²={r_value**2:.2f}, p={p_value:.2f}')

        plt.legend()
        plt.show()

        os.system("echo")

    # EVs per household income
    elif arg == "F":
        query = 'SELECT County, COUNT(*) AS "EV" FROM merged_df GROUP BY County ORDER BY COUNT(*) DESC'
        ev_per_county = sqldf(query, locals())

        query = 'SELECT County, Sum(Population) AS "Population" FROM (SELECT DISTINCT "Postal Code", County, Population FROM merged_df) GROUP BY County'
        county_pop = sqldf(query, locals())

        query = 'SELECT DISTINCT "Postal Code", County, "Household Income" FROM merged_df GROUP BY County ORDER BY County ASC'
        income_per_county = sqldf(query, locals())

        df = pd.merge(ev_per_county, county_pop, on="County")
        df = pd.merge(df, income_per_county, on="County")
        # some small zip codes have a negative household income as placeholder for privacy considerations
        # we will remove these from the analysis
        df = df[df["Household Income"] > 0]

        df["EV per Capita"] = df["EV"] / df["Population"] * 1000

        plt.scatter(df["Household Income"], df["EV per Capita"])
        plt.xlabel("Average Household Income (in USD)")
        plt.ylabel("EVs per capita (per 1000 people)")
        plt.title("Number of EVs vs Household Income by County")

        slope, intercept, r_value, p_value, _ = linregress(df["Household Income"], df["EV per Capita"])
        plt.plot(df["Household Income"], intercept + slope * df["Household Income"], 'r', label=f'R²={r_value**2:.2f}, p={p_value:.2f}')

        plt.legend()
        plt.show()

        os.system("echo")

    # EVs per area
    else:
        query = 'SELECT County, COUNT(*) AS "EV" FROM merged_df GROUP BY County ORDER BY COUNT(*) DESC'
        ev_per_county = sqldf(query, locals())

        query = 'SELECT County, Sum(Population) AS "Population" FROM (SELECT DISTINCT "Postal Code", County, Population FROM merged_df) GROUP BY County'
        county_pop = sqldf(query, locals())

        query = 'SELECT DISTINCT "Postal Code", County, "County Area" FROM merged_df GROUP BY County ORDER BY County ASC'
        area_per_county = sqldf(query, locals())

        df = pd.merge(ev_per_county, county_pop, on="County")
        df = pd.merge(df, area_per_county, on="County")

        df["EV per Capita"] = df["EV"] / df["Population"] * 1000
        df["Population Density"] = df["Population"] / (df["County Area"] / 1000000)

        plt.scatter(df["Population Density"], df["EV per Capita"])
        plt.xlabel("Population Density (people per square km)")
        plt.ylabel("EVs per capita (per 1000 people)")
        plt.title("Number of EVs vs Population Density by County")

        slope, intercept, r_value, p_value, _ = linregress(df["Population Density"], df["EV per Capita"])
        plt.plot(df["Population Density"], intercept + slope * df["Population Density"], 'r', label=f'R²={r_value**2:.2f}, p={p_value:.2f}')

        plt.legend()
        plt.show()

        os.system("echo")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script that accepts a terminal argument.")
    
    parser.add_argument(
        "arg",  # Name of the argument
        type=str,  # Data type
        help="The argument to process"
    )
    
    args = parser.parse_args()

    main(args.arg)