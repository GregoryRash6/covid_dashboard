def scrape_info():
    # Dependencies
    import pandas as pd
    import requests
    import datetime as dt
    from dotenv import load_dotenv
    import os
    from sqlalchemy import create_engine

    # Load Dot Env
    load_dotenv()

    # Save Password
    password = os.getenv("password")

    # Set Connection String
    connection_string = f"postgres:{password}@localhost:5432/covid_db"

    # Set Engine
    engine = create_engine(f'postgresql://{connection_string}')

    # URL for Covid API
    url = f"https://covidtracking.com/api/v1/states/daily.json"

    # Set Empty Lists toHold Values
    date = []
    state = []
    positive = []
    negative = []
    death = []
    positive_increase = []
    negative_increase = []
    death_increase = []
    hospitalized_currently = []
    recovered = []

    # Save Response
    response = requests.get(url).json()

    # Append Each Response to the Respective List
    for x in range(len(response)):
        date.append(response[x]["date"])
        state.append(response[x]["state"])
        positive.append(response[x]["positive"])
        negative.append(response[x]["negative"])
        death.append(response[x]["death"])
        positive_increase.append(response[x]["positiveIncrease"])
        negative_increase.append(response[x]["negativeIncrease"])
        death_increase.append(response[x]["deathIncrease"])
        hospitalized_currently.append(response[x]["hospitalizedCurrently"])
        recovered.append(response[x]["recovered"])

    # Create Dictionary out of Values
    states_dict = {
        "date": date,
        "state": state,
        "positive": positive,
        "negative": negative,
        "death": death,
        "positive_increase": positive_increase,
        "negative_increase": negative_increase,
        "death_increase": death_increase,
        "hospitalized_currently": hospitalized_currently,
        "recovered": recovered
    }

    # Create DataFrame from Dictionary
    my_data = pd.DataFrame(states_dict)

    # Read in Population Data
    state_populations = pd.read_csv(f"state_populations.csv")

    # Make Copy
    us_population = state_populations[["State", "Pop"]].copy()

    # Rename Columns
    us_population.columns = ["state", "population"]

    # State Abbreviations
    state_ab = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    # State Names
    states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
      "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
      "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
      "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
      "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
      "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
      "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
      "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

    # Create DataFrame from Names and Abbreviations
    df = pd.DataFrame(list(zip(state_ab, states)), columns =['state_ab', "state"]) 

    # Merge Data
    data_complete = pd.merge(us_population, df, how="inner", on=["state", "state"])

    # Create DataFrame
    population = pd.DataFrame(data_complete)

    # Rename Columns
    population.columns = ["full_name", "population", "state"]

    # Merge Data
    complete = pd.merge(my_data, population, how="inner", on=["state", "state"])

    # Create DataFrame
    data = pd.DataFrame(complete)

    # Save Increase Rate
    data['increase_rate'] = data["positive_increase"] / data["population"]

    # Save Positive Percentage
    data['positive_percentage'] = data["positive"] / data["population"]

    # Read 2020 Presidential Data
    presidential_data = pd.read_csv ("2020_presidential.csv")

    # Merge Data
    data = data.merge(presidential_data, left_on='full_name', right_on='full_name')

    # Rename Columns
    data.columns = ['date', 'state', 'positive', 'negative', 'death', 'positive_increase',
           'negative_increase', 'death_increase', 'hospitalized_currently', 'recovered', 'full_name', 'population',
           'increase_rate', 'positive_percentage', 'presidential_result']

    # Save Dates as Strings
    data['date'] = data['date'].astype(str)

    # Assign Date Column to a Variable
    all_dates = data["date"]

    # Convert All Dates to a Datetime 
    [dt.datetime.strptime(x, "%Y%m%d") for x in all_dates]

    # Replace Date Column with Datetime Values
    data["date"] = pd.to_datetime(all_dates)

    # Fill NA's
    data = data.fillna(0)

    # Empty List to Hold Dates
    all_dates = []

    # Append Dates to List
    for x in range(len(data)):
        all_dates.append(str(data["date"][x])[0:10])

    # Save List for Dates
    data['date'] = all_dates

    # Fill Covid Table
    data.to_sql(name='covid_data', con=engine, if_exists='append', index=False)