import requests
import json
import datetime
import glob
import os


def get(cookie):
    # Define the URL
    url = 'https://apiff14risingstones.web.sdo.com/api/home/userInfo/getUserInfo'

    # Define the headers
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Parse the JSON response
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return
    data = response.json()

    # TEST: Open the JSON file with UTF-8 encoding
    # with open('../.data/test.json', encoding='utf-8') as sampleresponse:
    #     data = json.load(sampleresponse)


    character_name = data['data']['character_name']
    server_name = data['data']['group_name']

    # Compare data and get differences
    Diff = compare(data['data'])

    # Log the differences or note that there are none
    diff_file = f'../.data/{server_name}-{character_name}-diff.json'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if Diff:
        diff_entry = {timestamp: Diff}
    else:
        diff_entry = {timestamp: "No diff"}

    # If the diff file exists, update it; otherwise, create a new one
    if os.path.exists(diff_file):
        with open(diff_file, 'r+', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_data.update(diff_entry)
            f.seek(0)
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
    else:
        with open(diff_file, 'w', encoding='utf-8') as f:
            json.dump(diff_entry, f, ensure_ascii=False, indent=4)

    # Save the response to a new file
    file_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    with open(f'../.data/{server_name}-{character_name}-{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def compare(data):
    FYI = {}

    character_name = data['character_name']
    server_name = data['group_name']

    # Get the latest file created
    latest_files = glob.glob(f'../.data/{server_name}-{character_name}-*.json')

    # If there are no previous files, return an empty dict
    if not latest_files:
        return FYI

    latest_file = max(latest_files, key=os.path.getctime)

    # Open the latest file and compare the data
    with open(latest_file, encoding='utf-8') as f:
        prv_data = json.load(f)['data']

    # Compare the relevant fields and store differences
    if data['characterDetail'][0]['kill_times'] != prv_data['characterDetail'][0]['kill_times']:
        FYI['kill_times'] = f"{prv_data['characterDetail'][0]['kill_times']} -> {data['characterDetail'][0]['kill_times']}"
    if data['characterDetail'][0]['play_time'] != prv_data['characterDetail'][0]['play_time']:
        FYI['play_time'] = f"{prv_data['characterDetail'][0]['play_time']} -> {data['characterDetail'][0]['play_time']}"

    return FYI


# Run and get cookie in arg
if __name__ == '__main__':
    import sys
    get(sys.argv[1])
