import json

# Define department codes and their corresponding names
department_codes = {
    "732": "Civil",
    "733": "CSE",
    "734": "EEE",
    "735": "ECE",
    "736": "Mech",
    "737": "IT",
    "748": "AIML"  # Updated department code for AIML
}

# Function to generate roll numbers for each department, year-wise
def generate_roll_numbers():
    roll_numbers_by_year = {}

    # Initialize dictionary with years and department names
    for year in range(2020, 2025):  # 2020 to 2024 for five years
        roll_numbers_by_year[str(year)] = {}

        for department_code, department_name in department_codes.items():
            roll_numbers_by_year[str(year)][department_name] = []

    # Define the range for the unique IDs (001 to 194 for each department)
    for year in range(2020, 2025):  # 2020 to 2024 for five years
        year_suffix = str(year)[2:]  # Get the last two digits of the year (e.g., 20 for 2020)

        for department_code, department_name in department_codes.items():
            for unique_id in range(1, 195):  # Generating IDs from 001 to 194 for each department
                # Format the roll number as "1602-XX-XXX-XXX"
                roll_number = f"1602-{year_suffix}-{department_code}-{str(unique_id).zfill(3)}"
                # Append the roll number to the respective department and year
                roll_numbers_by_year[str(year)][department_name].append(roll_number)

    # Write the structured roll numbers to a JSON file
    with open("college_ids.json", "w") as file:
        json.dump(roll_numbers_by_year, file, indent=4)

# Call the function to generate the roll numbers
generate_roll_numbers()
