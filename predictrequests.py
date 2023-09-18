import requests as r

# Change the variables that store the dictionary information needed to get a prediction. 
zip = 9900
rooms = 6
live = 455.0
plot = 20.0
stype = "house"
condi = "just renovated"
facades = 1
province = "Antwerpen"

# The dictionary that gets sent with the houses info.
predictx = {
    "Zip code": zip, 
    "subtype": stype, 
    "bedrooms": rooms, 
    "Living area": live, 
    "landplot": plot, 
    "facades": facades, 
    "condition": condi, 
    "province": province
    }

# Prints the required format to get a prediction. Includes status code.
print("\n",r.get('https://fastimmopredict.onrender.com/').text)
print("Status Code from GET request:", r.get('https://fastimmopredict.onrender.com/').status_code, "\n")

# Prints the prediction from the API by sending the dictionary in json format. Includes status code.
print(r.post('https://fastimmopredict.onrender.com/predict/', json=predictx).text)
print("Status Code from POST request:", r.post('https://fastimmopredict.onrender.com/predict/', json=predictx).status_code)
