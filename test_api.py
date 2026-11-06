import requests

BASE_URL = "http://127.0.0.1:5000/todos"

try:
    # 1. Test POST (Create a todo)
    print("--- Testing POST ---")
    response = requests.post(BASE_URL, json={"title": "Complete project implementation"})
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # 2. Test GET (Fetch all todos)
    print("\n--- Testing GET ---")
    response = requests.get(BASE_URL)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

except Exception as e:
    print(f"An error occurred: {e}")