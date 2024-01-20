import csv

# Open the CSV file
with open('new.csv', 'r') as file:
    # Create a CSV reader
    reader = csv.DictReader(file)
    
    # Specify the column to find the maximum value
    column_name = 'POT Value 1'
    
    # Initialize max_value to the minimum possible value
    max_value = float('-inf')
    
    # Iterate through rows and find the maximum value in the specified column
    for row in reader:
        current_value = float(row[column_name])
        if current_value > max_value:
            max_value = current_value

# Print the result
print(f"The maximum value in '{column_name}' column is: {max_value}")

with open('new.csv', 'r') as file:
    # Create a CSV reader
    reader = csv.DictReader(file)
    
    # Specify the column to find the maximum value
    column_name = 'POT Value 2'
    
    # Initialize max_value to the minimum possible value
    max_value = float('-inf')
    
    # Iterate through rows and find the maximum value in the specified column
    for row in reader:
        current_value = float(row[column_name])
        if current_value > max_value:
            max_value = current_value

# Print the result
print(f"The maximum value in '{column_name}' column is: {max_value}")
