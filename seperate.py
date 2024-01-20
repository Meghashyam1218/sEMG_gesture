import csv
from collections import defaultdict
import math

# Read the CSV data
with open("all.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = list(csv_reader)

# Define the window size
window_size = 5  # You can adjust the window size as needed

# Initialize dictionaries to store the sum, squared sum, and count for each iteration and gesture
sum_pot_value_1 = defaultdict(float)
sum_pot_value_2 = defaultdict(float)
squared_sum_pot_value_1 = defaultdict(float)
squared_sum_pot_value_2 = defaultdict(float)
count = defaultdict(int)

# Initialize lists to store values for each window
window_values_1 = defaultdict(list)
window_values_2 = defaultdict(list)

# Initialize dictionaries to store the previous values for each iteration and gesture
prev_avg_pot_value_1 = defaultdict(float)
prev_avg_pot_value_2 = defaultdict(float)
prev_std_dev_1 = defaultdict(float)
prev_std_dev_2 = defaultdict(float)
prev_mad_1 = defaultdict(float)
prev_mad_2 = defaultdict(float)

# Iterate through the data and calculate the sum for each iteration and gesture
result_values = []
for i, row in enumerate(data):
    iteration = row["Iteration"]
    gesture = row["Gesture"]
    pot_value_1 = float(row["POT Value 1"])
    pot_value_2 = float(row["POT Value 2"])

    sum_pot_value_1[(iteration, gesture)] += pot_value_1
    squared_sum_pot_value_1[(iteration, gesture)] += pot_value_1**2
    sum_pot_value_2[(iteration, gesture)] += pot_value_2
    squared_sum_pot_value_2[(iteration, gesture)] += pot_value_2**2
    count[(iteration, gesture)] += 1

    # Add values to the window
    window_values_1[(iteration, gesture)].append(pot_value_1)
    window_values_2[(iteration, gesture)].append(pot_value_2)

    # Maintain the window size
    if len(window_values_1[(iteration, gesture)]) > window_size:
        removed_value_1 = window_values_1[(iteration, gesture)].pop(0)
        removed_value_2 = window_values_2[(iteration, gesture)].pop(0)

        sum_pot_value_1[(iteration, gesture)] -= removed_value_1
        squared_sum_pot_value_1[(iteration, gesture)] -= removed_value_1**2
        sum_pot_value_2[(iteration, gesture)] -= removed_value_2
        squared_sum_pot_value_2[(iteration, gesture)] -= removed_value_2**2
        count[(iteration, gesture)] -= 1

    # Calculate the average, standard deviation, and mean absolute deviation
    avg_pot_value_1 = (
        sum_pot_value_1[(iteration, gesture)] / count[(iteration, gesture)]
    )
    avg_pot_value_2 = (
        sum_pot_value_2[(iteration, gesture)] / count[(iteration, gesture)]
    )

    std_dev_1 = math.sqrt(
        (squared_sum_pot_value_1[(iteration, gesture)] / count[(iteration, gesture)])
        - (avg_pot_value_1**2)
    )
    std_dev_2 = math.sqrt(
        (squared_sum_pot_value_2[(iteration, gesture)] / count[(iteration, gesture)])
        - (avg_pot_value_2**2)
    )

    mad_1 = (
        sum(
            abs(pot_value_1 - avg_pot_value_1)
            for pot_value_1 in window_values_1[(iteration, gesture)]
        )
        / count[(iteration, gesture)]
    )
    mad_2 = (
        sum(
            abs(pot_value_2 - avg_pot_value_2)
            for pot_value_2 in window_values_2[(iteration, gesture)]
        )
        / count[(iteration, gesture)]
    )

    # Calculate the delta (difference) from the previous values
    delta_avg_pot_value_1 = avg_pot_value_1 - prev_avg_pot_value_1[(iteration, gesture)]
    delta_avg_pot_value_2 = avg_pot_value_2 - prev_avg_pot_value_2[(iteration, gesture)]

    delta_std_dev_1 = std_dev_1 - prev_std_dev_1[(iteration, gesture)]
    delta_std_dev_2 = std_dev_2 - prev_std_dev_2[(iteration, gesture)]

    delta_mad_1 = mad_1 - prev_mad_1[(iteration, gesture)]
    delta_mad_2 = mad_2 - prev_mad_2[(iteration, gesture)]
    if(gesture!="left"):
        result_values.append(
            {
                "Iteration": iteration,
                "Gesture": gesture,
                "AVG POT VALUE 1": avg_pot_value_1,
                "AVG POT VALUE 2": avg_pot_value_2,
                "STD DEV 1": std_dev_1,
                "STD DEV 2": std_dev_2,
                "MAD 1": mad_1,
                "MAD 2": mad_2,
                "DELTA AVG POT VALUE 1": delta_avg_pot_value_1,
                "DELTA AVG POT VALUE 2": delta_avg_pot_value_2,
                "DELTA STD DEV 1": delta_std_dev_1,
                "DELTA STD DEV 2": delta_std_dev_2,
                "DELTA MAD 1": delta_mad_1,
                "DELTA MAD 2": delta_mad_2,
            }
        )

    # Update the previous values
    prev_avg_pot_value_1[(iteration, gesture)] = avg_pot_value_1
    prev_avg_pot_value_2[(iteration, gesture)] = avg_pot_value_2
    prev_std_dev_1[(iteration, gesture)] = std_dev_1
    prev_std_dev_2[(iteration, gesture)] = std_dev_2
    prev_mad_1[(iteration, gesture)] = mad_1
    prev_mad_2[(iteration, gesture)] = mad_2

# Write the results to a new CSV file
output_file = "output2.csv"
with open(output_file, "w", newline="") as csv_output:
    fieldnames = [
        "Iteration",
        "Gesture",
        "AVG POT VALUE 1",
        "AVG POT VALUE 2",
        "STD DEV 1",
        "STD DEV 2",
        "MAD 1",
        "MAD 2",
        "DELTA AVG POT VALUE 1",
        "DELTA AVG POT VALUE 2",
        "DELTA STD DEV 1",
        "DELTA STD DEV 2",
        "DELTA MAD 1",
        "DELTA MAD 2",
    ]
    csv_writer = csv.DictWriter(csv_output, fieldnames=fieldnames)

    csv_writer.writeheader()
    csv_writer.writerows(result_values)

print(f"Results written to {output_file}")
