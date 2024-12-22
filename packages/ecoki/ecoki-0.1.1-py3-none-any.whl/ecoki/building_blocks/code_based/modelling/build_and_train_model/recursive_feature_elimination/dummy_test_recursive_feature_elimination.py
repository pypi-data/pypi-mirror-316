# Retry with a different approach
# Creating a DataFrame from the given list of German formatted currency values
import pandas as pd

data = {
    'amount': [
        "4.854,00", "8.728,20", "-970,50", "-4.841,00", "-7.739,20", "10.621,60", 
        "-961,70", "-1.925,80", "-2.892,30", "-4.815,50", "11.520,00", "-959,10", 
        "-2.876,70", "-2.875,20", "-4.787,50", "11.460,00", "-955,80", "-1.912,00", 
        "-3.818,80", "-4.761,50", "4.899,50", "-4.912,50", "11.704,80", "-1.954,00", 
        "-3.906,00", "-5.853,60", "12.665,90", "-2.920,50", "-3.893,60", "-5.841,60", 
        "9.686,00", "-3.870,40", "-5.814,60", "6.759,90", "-6.747,30", "6.755,70", 
        "-6.750,80", "6.746,60", "-6.745,20", "6.724,90", "-6.729,10", "6.712,30", 
        "-6.713,00", "6.707,40", "-6.685,00", "7.633,60", "-7.626,40", "7.616,00", 
        "-7.608,80", "7.673,60", "-7.664,0", "7.654,0", "-7.632,0"
    ]
}

# Read the content of the CSV file as plain text
file_path = '/mnt/data/2024-05-24_14-24-39_ScalableCapital-Broker-Transactions.csv'

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Display the first few lines to understand the structure
content_lines = content.split('\n')
content_lines[:5]


df_currency = pd.DataFrame(data)

# Convert the 'amount' column from German format to numeric
df_currency['amount'] = df_currency['amount'].str.replace('.', '').str.replace(',', '.').astype(float)

# Calculate the sum
sum_currency = df_currency['amount'].sum()
print(sum_currency)
