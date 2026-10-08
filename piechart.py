import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
# Replace 'data.csv' with the actual filename in your repository
df = pd.read_csv('data.csv')

# Example: Assume the CSV has columns "Category" and "Value"
# Adjust column names based on your CSV structure
categories = df['Category']
values = df['Value']

# Plot pie chart
plt.figure(figsize=(8, 8))
plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
plt.title('Pie Chart from CSV Data')
plt.show()
