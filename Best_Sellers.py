#Dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

from pathlib import Path

#import data
coffee_data = Path('coffee-shop-sales-revenue.csv')

print(coffee_data)

#Read in the data
coffee_df = pd.read_csv(coffee_data, sep='|')

#Print out the first and last five rows
display(coffee_df.head(2))
display(coffee_df.tail(2))

#Clean the data

#Check for nulls
display(coffee_df.isnull().mean() * 100)

#remove nulls
coffee_df = coffee_df.dropna()

#Check for duplicates
display(coffee_df.duplicated().sum())

#Remove duplicates
coffee_df = coffee_df.drop_duplicates()

#Combine date and time columns into new column
coffee_df['salesdatetime'] = coffee_df['transaction_date'].astype(str) + ' ' + coffee_df['transaction_time'].astype(str)

#Convert new column to datetime
coffee_df['salesdatetime'] = pd.to_datetime(coffee_df['salesdatetime'])

#Check data types
display(coffee_df.dtypes)

#Print out the first and last five rows
display(coffee_df.head(2))
display(coffee_df.tail(2))

#Create a new column for total sales
coffee_df['totalsales'] = coffee_df['transaction_qty'] * coffee_df['unit_price']

#Create a new column for month
coffee_df['month'] = coffee_df['salesdatetime'].dt.month

#print(coffee_df['month'])
#print(coffee_df['salesdatetime'].dt.year)
#print(coffee_df['salesdatetime'].dt.day)
#Create a new column for the week of the year
coffee_df['weekofyear'] = pd.to_datetime(coffee_df['salesdatetime']).dt.strftime('%U')

#Create a new column for day of week
coffee_df['dayofweek'] = coffee_df['salesdatetime'].dt.dayofweek

#Create a new column for hour
coffee_df['hour'] = coffee_df['salesdatetime'].dt.hour

#Print out the first and last 2 rows
display(coffee_df.head(2))
display(coffee_df.tail(2))

#Create a dataframe for each store
store1_df = coffee_df.loc[coffee_df['store_id'] == 3]
store2_df = coffee_df.loc[coffee_df['store_id'] == 5]
store3_df = coffee_df.loc[coffee_df['store_id'] == 8]

#Reset the index for each store to sale datetime
store1_df = store1_df.set_index('salesdatetime')
store2_df = store2_df.set_index('salesdatetime')
store3_df = store3_df.set_index('salesdatetime')


#Print out the first and last 2 rows of each store
display(store1_df.head(2))
display(store1_df.tail(2))

display(store2_df.head(2))
display(store2_df.tail(2))

display(store3_df.head(2))
display(store3_df.tail(2))


#Create a custom function to sum total sales
def sum_totalsales(df):
    return df['totalsales'].sum()

#create a custom function to calculate average sales
def avg_totalsales(df):
    return df['totalsales'].mean()

#Create a dataframe for each store's total sales using the custom function by month
store1_totalsales = store1_df.groupby('month').apply(sum_totalsales)
store2_totalsales = store2_df.groupby('month').apply(sum_totalsales)
store3_totalsales = store3_df.groupby('month').apply(sum_totalsales)

#Dispalay the total sales for each store as a line graph
plt.plot(store1_totalsales, label='Astoria', color='blue')
plt.plot(store2_totalsales, label='Lower Manhattan', color='red')
plt.plot(store3_totalsales, label="Hell's Kitchen", color='green')


plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.title('Total Sales by Store')
plt.legend(loc='best')
plt.figure(figsize=(60,10))

plt.show()

#Create a dataframe for each store's average sales using the custom function by hour
store1_avgsales = store1_df.groupby('hour').apply(avg_totalsales)
store2_avgsales = store2_df.groupby('hour').apply(avg_totalsales)
store3_avgsales = store3_df.groupby('hour').apply(avg_totalsales)

#Dispalay the average sales for each store as a line graph
plt.plot(store1_avgsales, label='Astoria', color='blue')
plt.plot(store2_avgsales, label='Lower Manhattan', color='red')
plt.plot(store3_avgsales, label="Hell's Kitchen", color='green')

#Change the x axis to display hours as 12 hour time label starting at 6am and ending at 8pm
plt.xticks(np.arange(5, 21, 1))


plt.xlabel('Time of Day')
plt.ylabel('Average Sales')
plt.title('Average Hourly Sales by Store')
plt.legend(loc='best')
plt.figure(figsize=(60,10))

plt.show()

#Create a dataframe for each store's average sales using the custom function by day of week
store1_avgsales = store1_df.groupby('dayofweek').apply(avg_totalsales)
store2_avgsales = store2_df.groupby('dayofweek').apply(avg_totalsales)
store3_avgsales = store3_df.groupby('dayofweek').apply(avg_totalsales)

#Dispalay the average sales for each store as a line graph
plt.plot(store1_avgsales, label='Astoria', color='blue')
plt.plot(store2_avgsales, label='Lower Manhattan', color='red')
plt.plot(store3_avgsales, label="Hell's Kitchen", color='green')

#Change the x axis labels to day of week names
plt.xticks(np.arange(7), ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), rotation=45)

plt.xlabel('Day')
plt.ylabel('Average Sales')
plt.title('Average Sales by Store per Day of Week')
plt.legend(loc='best')
plt.figure(figsize=(60,10))

#Product analysis

#See what type of products are sold
#coffee_df['product_category'].unique()

#Count number of each product category sold for each store
product_type_totals_store1 = store1_df['product_category'].value_counts()
product_type_totals_store2 = store2_df['product_category'].value_counts()
product_type_totals_store3 = store3_df['product_category'].value_counts()

#New dataframe with these counts
product_type_totals_all_stores = pd.DataFrame({
    'Astoria': product_type_totals_store1,
    'Lower Manhattan': product_type_totals_store2,
    "Hell's Kitchen": product_type_totals_store3
})

#Plotting in a bar chat
product_type_totals_all_stores.plot(kind='bar')
plt.title('Product Category Total by Store')
plt.xlabel("Product Category")
plt.ylabel("Number sold")
plt.show()


# Based on the above graph, we can see that coffee is the most popular product category for all stores.
# Let's see what types of coffee products are the most popular for each store.
# First we will look at the number of each coffee product sold for each store.

# Function to get best coffee products for a given store
def get_best_coffee_products(store_df):
    coffee_products = store_df.loc[store_df['product_category'] == 'Coffee', ['product_type', 'transaction_qty']]
    grouped_coffee_products = coffee_products.groupby('product_type').sum()
    return grouped_coffee_products

# Get best coffee products for each store
best_coffee_store1 = get_best_coffee_products(store1_df)
best_coffee_store2 = get_best_coffee_products(store2_df)
best_coffee_store3 = get_best_coffee_products(store3_df)

print(f"Product Type sold at Astoria" + "\n" + str(best_coffee_store1))
print(f"Product Type sold at Lower Manhattan" + "\n" + str(best_coffee_store2))
print(f"Product Type sold at Hell's Kitchen" + "\n" + str(best_coffee_store3))


# Bar graph for each store
# Function to get best coffee products for a given store
def get_best_coffee_products(store_df):
    coffee_products = store_df.loc[store_df['product_category'] == 'Coffee', ['product_type', 'transaction_qty']]
    grouped_coffee_products = coffee_products.groupby('product_type').sum()
    return grouped_coffee_products

# Get best coffee products for each store
best_coffee_store1 = get_best_coffee_products(store1_df)
best_coffee_store2 = get_best_coffee_products(store2_df)
best_coffee_store3 = get_best_coffee_products(store3_df)

# Prepare data for a bar graph
store_names = ["Astoria", "Lower Manhattan", "Hell's Kitchen"]
dfs = [best_coffee_store1, best_coffee_store2, best_coffee_store3]

# Plotting in a bar chart
for store_name, best_coffee_products in zip(store_names, dfs):
    best_coffee_products.plot(kind='bar', legend=False)
    plt.title(f'Coffee Products Sold for {store_name}')
    plt.xlabel("Coffee Type")
    plt.ylabel("Number Sold")
    plt.show()

# Combined bar graph for all stores
def get_best_coffee_products(store_df):
    coffee_products = store_df.loc[store_df['product_category'] == 'Coffee', ['product_type', 'transaction_qty']]
    grouped_coffee_products = coffee_products.groupby('product_type').sum()
    return grouped_coffee_products

# Get best coffee products for each store
best_coffee_store1 = get_best_coffee_products(store1_df)
best_coffee_store2 = get_best_coffee_products(store2_df)
best_coffee_store3 = get_best_coffee_products(store3_df)

# Combine data for all stores into a single DataFrame
combined_data = pd.concat([best_coffee_store1, best_coffee_store2, best_coffee_store3], axis=1)
combined_data.columns = ["Astoria", "Lower Manhattan", "Hell's Kitchen"]

# Plotting in a single bar chart
combined_data.plot(kind='bar')
plt.title('Coffee Products Sold for All Stores')
plt.xlabel("Coffee Type")
plt.ylabel("Number Sold")
plt.legend(loc='best')
plt.show()

#Line graph for all stores
def get_best_coffee_products(store_df):
    coffee_products = store_df.loc[store_df['product_category'] == 'Coffee', ['product_type', 'transaction_qty']]
    grouped_coffee_products = coffee_products.groupby('product_type').sum()
    return grouped_coffee_products

# Get best coffee products for each store
best_coffee_store1 = get_best_coffee_products(store1_df)
best_coffee_store2 = get_best_coffee_products(store2_df)
best_coffee_store3 = get_best_coffee_products(store3_df)

# Combine data for all stores into a single DataFrame
combined_data = pd.concat([best_coffee_store1, best_coffee_store2, best_coffee_store3], axis=1)
combined_data.columns = ["Astoria", "Lower Manhattan", "Hell's Kitchen"]

# Plotting in a line chart
combined_data.plot(kind='line', marker='o', linestyle='-')

# Set the title and labels
plt.title('Best Coffee Products for All Stores')
plt.xlabel("Coffee Type")
plt.ylabel("Number Sold")
plt.legend(loc='best')
plt.xticks(rotation=45)
plt.show()

#We will now look at total sales for each coffee product for each store.
#Graph 2: product_category {'Coffee'}, then break down by product_type for each store
#Sales = #unit_price * transaction_qty
#Astoria, Lower Manhattan, Hell's Kitchen

# Function to get best coffee products for a given store and the total sales for each product
def get_best_coffee_products(store_df):
    coffee_products = store_df.loc[store_df['product_category'] == 'Coffee', ['product_type', 'transaction_qty', 'unit_price']]
    grouped_coffee_products = coffee_products.groupby('product_type').sum()
    grouped_coffee_products['totalsales'] = grouped_coffee_products['transaction_qty'] * grouped_coffee_products['unit_price']
    return grouped_coffee_products

# Get best coffee products for each store
best_coffee_store1 = get_best_coffee_products(store1_df)
best_coffee_store2 = get_best_coffee_products(store2_df)
best_coffee_store3 = get_best_coffee_products(store3_df)

# Print total sales for each product type for each store
print("Astoria:")
print(best_coffee_store1['totalsales']/ 1_000_000)

print("\nLower Manhattan:")
print(best_coffee_store2['totalsales']/ 1_000_000)

print("\nHell's Kitchen:")
print(best_coffee_store3['totalsales']/ 1_000_000)

def get_best_coffee_products(store_df):
    coffee_products = store_df.loc[store_df['product_category'] == 'Coffee', ['product_type', 'transaction_qty', 'unit_price']]
    grouped_coffee_products = coffee_products.groupby('product_type').sum()
    grouped_coffee_products['totalsales'] = grouped_coffee_products['transaction_qty'] * grouped_coffee_products['unit_price']
    return grouped_coffee_products

# Get best coffee products for each store
best_coffee_store1 = get_best_coffee_products(store1_df)
best_coffee_store2 = get_best_coffee_products(store2_df)
best_coffee_store3 = get_best_coffee_products(store3_df)

# Plot bar graphs for each store
fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# Store 1
axs[0].bar(best_coffee_store1.index, best_coffee_store1['totalsales'] / 1_000_000, color='blue')
axs[0].set_title('Astoria')
axs[0].set_ylabel('Total Sales (Millions)')
axs[0].set_xticks(best_coffee_store1.index)
axs[0].set_xticklabels(best_coffee_store1.index, rotation=45, ha='right')  # Rotate x-axis labels

# Store 2
axs[1].bar(best_coffee_store2.index, best_coffee_store2['totalsales'] / 1_000_000, color='green')
axs[1].set_title('Lower Manhattan')
axs[1].set_xlabel("Coffee Type")
axs[1].set_ylabel('Total Sales (Millions)')
axs[1].set_xticks(best_coffee_store2.index)
axs[1].set_xticklabels(best_coffee_store2.index, rotation=45, ha='right')  # Rotate x-axis labels

# Store 3
axs[2].bar(best_coffee_store3.index, best_coffee_store3['totalsales'] / 1_000_000, color='orange')
axs[2].set_title("Hell's Kitchen")
axs[2].set_xlabel("Coffee Type")
axs[2].set_ylabel('Total Sales (Millions)')
axs[2].set_xticks(best_coffee_store3.index)
axs[2].set_xticklabels(best_coffee_store3.index, rotation=45, ha='right')  # Rotate x-axis labels

plt.tight_layout()
plt.show()

#Combined bar graph for all stores

def get_best_coffee_products(store_df):
    coffee_products = store_df.loc[store_df['product_category'] == 'Coffee', ['product_type', 'transaction_qty', 'unit_price']]
    grouped_coffee_products = coffee_products.groupby('product_type').sum()
    grouped_coffee_products['totalsales'] = grouped_coffee_products['transaction_qty'] * grouped_coffee_products['unit_price']
    return grouped_coffee_products

# Get best coffee products for each store
best_coffee_store1 = get_best_coffee_products(store1_df)
best_coffee_store2 = get_best_coffee_products(store2_df)
best_coffee_store3 = get_best_coffee_products(store3_df)

# Combine data for all stores into a single DataFrame
combined_data = pd.concat([best_coffee_store1, best_coffee_store2, best_coffee_store3], axis=1)

#Legend labels
legend_labels = ["Astoria", "Lower Manhattan", "Hell's Kitchen"]

# Plotting in a single bar chart
combined_data.plot(kind='bar')
plt.title('Coffee Products Sold for All Stores')
plt.xlabel("Coffee Type")
plt.ylabel("Number Sold")
plt.legend(loc='best', labels=legend_labels)
plt.xticks(rotation=45)
plt.show()

#Line graph for all stores

def get_best_coffee_products(store_df):
    coffee_products = store_df.loc[store_df['product_category'] == 'Coffee', ['product_type', 'transaction_qty', 'unit_price']]
    grouped_coffee_products = coffee_products.groupby('product_type').sum()
    grouped_coffee_products['totalsales'] = grouped_coffee_products['transaction_qty'] * grouped_coffee_products['unit_price']
    return grouped_coffee_products

# Get best coffee products for each store
best_coffee_store1 = get_best_coffee_products(store1_df)
best_coffee_store2 = get_best_coffee_products(store2_df)
best_coffee_store3 = get_best_coffee_products(store3_df)

# Combine data for all stores into a single DataFrame
combined_data = pd.concat([best_coffee_store1, best_coffee_store2, best_coffee_store3], axis=1)

# Set legend labels
legend_labels = ["Astoria", "Lower Manhattan", "Hell's Kitchen"]

# Set line colors
line_colors = ['blue', 'green', 'orange']

# Plotting in a single line chart
ax = combined_data.plot(kind='line', marker='o', linestyle='-', color=line_colors)

# Set the title and labels
plt.title('Best Coffee Products for All Stores')
plt.xlabel("Coffee Type")
plt.ylabel("Number Sold")

# Set the legend with custom labels and colors
ax.legend(legend_labels, loc='best', handlelength=1.5, handleheight=1.5)

# Remove the horizontal line at 0 by setting y-axis limits
ax.set_ylim(bottom=0.1)  # Adjust the value as needed

plt.xticks(rotation=45)
plt.show()


