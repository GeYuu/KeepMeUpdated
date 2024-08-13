import requests



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

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response text or convert it to JSON if it's in JSON format
        print(response.text)
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response text:", response.text)

# run and get cookie in arg
if __name__ == '__main__':
    import sys
    get(sys.argv[1])

