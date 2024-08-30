import requests

url = "https://planefinder.net"

def get_airline_page(letter):
    u = f"{url}/data/airlines/{letter}"
    response = requests.get(url)
    print(response)
    return response.text

v = get_airline_page("A")
print("\n\n\n")
print(v)

