import requests

BASE = "http://127.0.0.1:5000/"


data = [{"name":"zero","views": 100, "likes": 15},
        {"name":"first","views": 125, "likes": 99},
        {"name":"second","views": 150, "likes": 45},
        {"name":"third","views": 175, "likes": 60}]

for i, entry in enumerate(data):
    response = requests.patch(BASE + "video/" + str(i), entry)
    print(response.json())
    
# response = requests.delete(BASE + "video/0")
# print(response)

response = requests.get(BASE + "video/1")
print(response.json())

response = requests.get(BASE + "video/6")
print(response.json())
    


# response = requests.put(BASE + "video" + "/1", {"name": "first","views":20, "likes":10})
# print(response.json())

# # input("Press Enter to continue.")

# response = requests.get(BASE + "video" + "/1")
# print(response.json())

# response = requests.delete(BASE + "video" + "/1")
# print(response.json())

# response = requests.delete(BASE + "video" + "/11")
# print(response.json())

# response = requests.put(BASE + "video" + "/1", {"name": "first","views":20, "likes":10})
# print(response.json())
# print("Success! ")