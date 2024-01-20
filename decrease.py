import csv
from collections import defaultdict
import math

# Read the CSV data
with open('all.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = list(csv_reader)

# Define the window size
window_size = 20

# Initialize dictionaries to store the sum and count for each iteration and gesture
sum_pot_value_1 = defaultdict(float)
sum_pot_value_2 = defaultdict(float)
count = defaultdict(int)

# Initialize a list to store the averaged values
averaged_values = []

# Iterate through the data and calculate the sum for each iteration and gesture
for i, row in enumerate(data):
    iteration = row['Iteration']
    gesture = row['Gesture']
    pot_value_1 = float(row['POT Value 1'])
    pot_value_2 = float(row['POT Value 2'])

    sum_pot_value_1[(iteration, gesture)] += pot_value_1
    sum_pot_value_2[(iteration, gesture)] += pot_value_2
    count[(iteration, gesture)] += 1

    # Calculate the average and reset the sum and count for every 9 rows
    if count[(iteration, gesture)] == window_size:
        avg_pot_value_1 = sum_pot_value_1[(iteration, gesture)] / window_size
        avg_pot_value_2 = sum_pot_value_2[(iteration, gesture)] / window_size

        averaged_values.append({
            'Iteration': iteration,
            'Gesture': gesture,
            'AVG POT VALUE 1': avg_pot_value_1,
            'AVG POT VALUE 2': avg_pot_value_2,
        })

        # Reset sum and count
        sum_pot_value_1[(iteration, gesture)] = 0
        sum_pot_value_2[(iteration, gesture)] = 0
        count[(iteration, gesture)] = 0

# Write the averaged results to a new CSV file
output_file = 'averaged_output.csv'
with open(output_file, 'w', newline='') as csv_output:
    fieldnames = ['Iteration', 'Gesture', 'AVG POT VALUE 1', 'AVG POT VALUE 2']
    csv_writer = csv.DictWriter(csv_output, fieldnames=fieldnames)

    csv_writer.writeheader()
    csv_writer.writerows(averaged_values)

print(f"Averaged results written to {output_file}")
