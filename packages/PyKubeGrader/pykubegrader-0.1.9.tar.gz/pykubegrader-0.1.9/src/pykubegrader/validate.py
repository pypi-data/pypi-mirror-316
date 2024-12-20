import base64
import json
import os
import re
import sys
from datetime import datetime

import nacl.public
import numpy as np
import requests
from requests.auth import HTTPBasicAuth


def validate_logfile(
    filepath: str,
    assignment_id: str,
    question_max_scores: dict[int, int],
    free_response_questions=0,
    username="student",
    password="capture",
    post_url="https://engr-131-api.eastus.cloudapp.azure.com/upload-score",
    login_url="https://engr-131-api.eastus.cloudapp.azure.com/login",
) -> None:
    login_data = {
        "username": username,
        "password": password,
    }

    with open("server_private_key.bin", "rb") as priv_file:
        server_private_key_bytes = priv_file.read()
    server_priv_key = nacl.public.PrivateKey(server_private_key_bytes)

    with open("client_public_key.bin", "rb") as pub_file:
        client_public_key_bytes = pub_file.read()
    client_pub_key = nacl.public.PublicKey(client_public_key_bytes)

    box = nacl.public.Box(server_priv_key, client_pub_key)

    with open(filepath, "r") as logfile:
        encrypted_lines = logfile.readlines()

    data_: list[str] = []
    for line in encrypted_lines:
        if "Encrypted Output: " in line:
            trimmed = line.split("Encrypted Output: ")[1].strip()
            decoded = base64.b64decode(trimmed)
            decrypted = box.decrypt(decoded).decode()
            data_.append(decrypted)

    # Decoding the log file
    # data_: list[str] = drexel_jupyter_logger.decode_log_file(self.filepath, key=key)
    _loginfo = str(data_)

    # Where possible, we should work with this reduced list of relevant entries
    data_reduced = [
        entry
        for entry in data_
        if re.match(r"info,", entry) or re.match(r"q\d+_\d+,", entry)
    ]

    # For debugging; to be commented out
    with open(".output_reduced.log", "w") as f:
        f.writelines(f"{item}\n" for item in data_reduced)

    # Initialize the question scores and max scores
    question_max_scores = question_max_scores
    question_scores = {key: 0 for key in question_max_scores}

    # Parsing the data to find the last entries for required fields
    # This gets the student name etc.
    last_entries: dict[str, str | float] = {}
    for entry in data_reduced:
        parts = [part.strip() for part in entry.split(",")]
        if parts[0] == "info" and len(parts) == 4:
            field_name = parts[1]
            field_value = parts[2]
            last_entries[field_name] = field_value

    # For debugging; to be commented out
    # print(f"Keys in last_entries dict: {last_entries.keys()}")

    # Check if the assignment id is in the log file
    if "assignment" not in last_entries or assignment_id != last_entries["assignment"]:
        sys.exit(
            "Your log file is not for the correct assignment. Please submit the correct log file."
        )

    required_student_info = ["drexel_id", "first_name", "last_name", "drexel_email"]

    for field in required_student_info:
        if last_entries.get(field) is None:
            sys.exit(
                "You must submit your student information before you start the exam. Please submit your information and try again."
            )

    # Initialize code and data lists
    code: list[str] = []
    data: list[str] = []

    # Splitting the data into code and responses
    for entry in data_:
        # Splitting the data into code and responses
        if "code run:" in entry:
            code.append(entry)
        else:
            data.append(entry)

    # Checks to see if the drexel_jupyter_logger is in the code
    # If it is, the student might have tried to look at the solutions
    # Commenting this out, since we're switching to asymmetric encryption
    # flag = any("drexel_jupyter_logger" in item for item in code)

    # Extracting timestamps and converting them to datetime objects
    timestamps = [
        datetime.strptime(row.split(",")[-1].strip(), "%Y-%m-%d %H:%M:%S")
        for row in data_reduced
    ]

    # Getting the earliest and latest times
    last_entries["start_time"] = min(timestamps).strftime("%Y-%m-%d %H:%M:%S")
    last_entries["end_time"] = max(timestamps).strftime("%Y-%m-%d %H:%M:%S")
    delta = max(timestamps) - min(timestamps)
    minutes_rounded = round(delta.total_seconds() / 60, 2)
    last_entries["elapsed_minutes"] = minutes_rounded
    # last_entries["flag"] = flag

    # Collect student info dict
    student_information = {key.upper(): value for key, value in last_entries.items()}

    # Write info dict to info.json
    with open("info.json", "w") as file:
        print("Writing to info.json")
        json.dump(student_information, file)

    def get_last_entry(data: list[str], field_name: str) -> str:
        for entry in data[::-1]:
            parts = [part.strip() for part in entry.split(",")]
            if parts[0] == field_name:
                return entry
        return ""

    def get_entries_len(data: list[str], question_number: int) -> int:
        """function to get the unique entries by length

        Args:
            data (list): list of all the data records
            question_number (int): question number to evaluate

        Returns:
            int: length of the unique entries
        """

        # Set for unique qN_* values
        unique_qN_values = set()

        for entry in data:
            if entry.startswith(f"q{question_number}_"):
                # Split the string by commas and get the value part
                parts = [part.strip() for part in entry.split(",")]
                # The value is the third element after splitting (?)
                value = parts[0].split("_")[1]
                unique_qN_values.add(value)

        return len(unique_qN_values) + 1

    # Modified list comprehension to filter as per the criteria
    free_response = [
        entry
        for entry in data_
        if entry.startswith("q")
        and entry.split("_")[0][1:].isdigit()
        and int(entry.split("_")[0][1:]) > free_response_questions
    ]

    # Initialize a dictionary to hold question entries.
    q_entries = []

    # Iterate over the number of free response questions.
    for i in range(1, free_response_questions + 1):
        # Collect entries for each question in a list.
        entries = [
            entry
            for j in range(1, get_entries_len(data, i))
            if (entry := get_last_entry(data, f"q{i}_{j}")) != ""
        ]

        # Store the list of entries in the dictionary, keyed by question number.
        q_entries += entries

    q_entries += free_response

    # Parse the data
    parsed_data: list[list[str]] = [
        [part.strip() for part in line.split(",")] for line in q_entries
    ]

    unique_question_IDs = set(row[0] for row in parsed_data)

    # Initialize a dictionary to hold the maximum score for each unique value
    max_scores = {unique_value: 0 for unique_value in unique_question_IDs}

    # Loop through each row in the data
    for score_entry in parsed_data:
        unique_value = score_entry[0]
        score = int(score_entry[1])
        # possible_score = float(row[3])
        # Update the score if it's higher than the current maximum
        if score > max_scores[unique_value]:
            max_scores[unique_value] = score

    # Loop through the max_scores dictionary and sum scores for each question
    for unique_value, score in max_scores.items():
        # Extract question number (assuming it's the number immediately after 'q')
        question_number = int(unique_value.split("_")[0][1:])
        question_scores[question_number] += score

    # Sorting the dictionary by keys
    question_max_scores = {
        key: int(np.round(question_max_scores[key]))
        for key in sorted(question_max_scores)
    }

    # Sorting the dictionary by keys
    question_scores = {
        key: int(np.round(question_scores[key])) for key in sorted(question_scores)
    }

    # Creating the dictionary structure
    result_structure: dict[str, list[dict]] = {
        "tests": [],
    }

    # Adding entries for each question
    for question_number in question_scores.keys():
        question_entry = {
            "name": f"Question {question_number}",
            "score": question_scores[question_number],
            "max_score": question_max_scores[question_number],
            # "visibility": "visible",
            # "output": "",
        }
        result_structure["tests"].append(question_entry)

    # Write results dict to results.json
    with open("results.json", "w") as file:
        print("Writing to results.json")
        json.dump(result_structure, file, indent=4)

    verify_login(login_data, login_url)

    # The file to be uploaded. Ensure the path is correct.
    file_path = "results.json"

    # Construct data payload as a dict
    final_data = {
        "assignment": assignment_id,
        "student_email": last_entries.get("drexel_email"),
        # "original_file_name": file_path,
        "start_time": last_entries["start_time"],
        "end_time": last_entries["end_time"],
        # "flag": last_entries["flag"],
        # "submission_mechanism": "jupyter_notebook",
        # "log_file": loginfo,
        "scores": result_structure["tests"],
    }

    # Files to be uploaded. The key should match the name expected by the server.
    _files = {
        "file": (file_path, open(file_path, "rb")),
    }

    # Make the POST request with data and files
    response = requests.post(
        url=post_url,
        json=final_data,
        # files=files,
        auth=HTTPBasicAuth(login_data["username"], login_data["password"]),
    )

    # Print messages for the user
    submission_message(response)


#
# Helper functions
#


def submission_message(response) -> None:
    if response.status_code == 200:
        print("Data successfully uploaded to the server")
        print(response.text)
    else:
        print(f"Failed to upload data. Status code: {response.status_code}")
        print(response.text)
        print(
            "There is something wrong with your log file or your submission. Please contact an instructor for help."
        )

    if os.path.exists("results.json"):
        # os.remove("results.json")
        # Let's keep results.json for now, for debugging
        pass
    else:
        print("results.json was not present")


def verify_login(login_data, login_url):
    login_response = requests.post(
        login_url, auth=HTTPBasicAuth(login_data["username"], login_data["password"])
    )

    if login_response.status_code == 200:
        print("Login successful")
    else:
        Exception("Login failed")
