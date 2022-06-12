import pandas as pd  # importing pandas

# loading in the data as pandas DataFrame
prices = pd.read_csv("data/prices-split-adjusted.csv")
fun = pd.read_csv("data/fundamentals.csv")
sec = pd.read_csv("data/securities.csv")

# utilizing the three columns needed
curRatio = fun[['Ticker Symbol', 'Current Ratio', 'Period Ending']]


sec_prices = pd.merge(
    sec,
    curRatio,
    how='inner',
    left_on=['Ticker symbol'],
    right_on=['Ticker Symbol'])  # merging two DataFrames
# subsetting the DataFrame
avg_cur_ratio = sec_prices[['Period Ending', 'Current Ratio', 'GICS Sector']]
# Extracting the year out of date
avg_cur_ratio['year'] = avg_cur_ratio['Period Ending'].str[0:4]
# taking the mean of Current Ratio by sectors and year
avg_cur_ratio = avg_cur_ratio.groupby(
    ['GICS Sector', 'year'], as_index=False).mean()

avg_cur_ratio['year'] = pd.to_numeric(
    avg_cur_ratio['year'])  # converting the column to numeric

# taking into account only data between 2012 and 2016
avg_cur_ratio = avg_cur_ratio[avg_cur_ratio['year'] <= 2016]
avg_cur_ratio = avg_cur_ratio[avg_cur_ratio['year'] >= 2012]

avg_cur_ratio = avg_cur_ratio.pivot(
    index="year",
    columns="GICS Sector",
    values="Current Ratio").reset_index()

avg_cur_ratio.to_csv('data/cur_ratio.csv', index=False)  # saving as csv file


# utilizing the three columns needed
cashRatio = fun[['Ticker Symbol', 'Cash Ratio', 'Period Ending']]
sec_prices = pd.merge(
    sec,
    cashRatio,
    how='inner',
    left_on=['Ticker symbol'],
    right_on=['Ticker Symbol'])  # merging two DataFrames
# subsetting the DataFrame
avg_cashRatio = sec_prices[['Period Ending', 'Cash Ratio', 'GICS Sector']]
# Extracting the year out of date
avg_cashRatio['year'] = avg_cashRatio['Period Ending'].str[0:4]
# taking the mean of Current Ratio by sectors and year
avg_cashRatio = avg_cashRatio.groupby(
    ['GICS Sector', 'year'], as_index=False).mean()

avg_cashRatio['year'] = pd.to_numeric(
    avg_cashRatio['year'])  # converting the column to numeric

# taking into account only data between 2012 and 2016
avg_cashRatio = avg_cashRatio[avg_cashRatio['year'] <= 2016]
avg_cashRatio = avg_cashRatio[avg_cashRatio['year'] >= 2012]

avg_cashRatio = avg_cashRatio.pivot(
    index="year",
    columns="GICS Sector",
    values="Cash Ratio").reset_index()

avg_cashRatio.to_csv('data/cash_ratio.csv', index=False)  # saving as csv file
