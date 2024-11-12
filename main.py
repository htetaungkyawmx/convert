from pymavlink import mavutil
import csv
import json

def convert_tlog_to_csv_json(tlog_path, output_path_csv=None, output_path_json=None):
    # Remove 'file:' prefix for Windows compatibility
    mavlog = mavutil.mavlink_connection(tlog_path)
    
    # Initialize CSV and JSON outputs if paths are provided
    if output_path_csv:
        csv_file = open(output_path_csv, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["timestamp", "message_name", "data"])  # CSV column headers

    if output_path_json:
        json_data = []  # Collects messages for JSON output

    # Parse messages from the TLOG file
    while True:
        msg = mavlog.recv_match()
        if msg is None:
            break  # End of TLOG file

        # Extract message details
        timestamp = msg._timestamp
        message_name = msg.get_type()
        data = msg.to_dict()

        # Write message to CSV
        if output_path_csv:
            csv_writer.writerow([timestamp, message_name, data])

        # Append message to JSON list
        if output_path_json:
            json_data.append({
                "timestamp": timestamp,
                "message_name": message_name,
                "data": data
            })

    # Save JSON data to file
    if output_path_json:
        with open(output_path_json, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

    # Close the CSV file if it was opened
    if output_path_csv:
        csv_file.close()

# Example usage with your specific TLOG file path
convert_tlog_to_csv_json(
    "C:/Users/ThinkBook/Documents/Mission Planner/logs/SITL/FIXED_WING/1/2024-11-12 14-49-35.tlog",  # Path to TLOG file
    "output.csv",  # Path to save CSV file
    "output.json"  # Path to save JSON file
)
