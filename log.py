import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2NTEyMzAxLCJpYXQiOjE3NDY1MTE3MDEsImp0aSI6ImQxOTMxY2ZiODA4MzQ0MjE5OTQ1NmQ4M2FjMjc2OWFkIiwidXNlcl9pZCI6IjRjOTgzMmNmLTI4ZTMtNDNjZS1hNWU5LTJlMmYzNTg1ZTM5ZiJ9.LBrr-3c0T48YEOtconR32qdA9f4sz4VVrBW24ou4SKU",
    "Content-Type": "application/json"
}
data = {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjU5ODEwMSwiaWF0IjoxNzQ2NTExNzAxLCJqdGkiOiI5M2YwZjlmZWYxODc0OWNjYWRjNDc1OTI1MjE3MjY4YiIsInVzZXJfaWQiOiI0Yzk4MzJjZi0yOGUzLTQzY2UtYTVlOS0yZTJmMzU4NWUzOWYifQ.1GzMaN6a3EoLDj5TWAWL78Rsdp1whXnyk8EtAptvzi8"
}


response = requests.post("http://127.0.0.1:8000/api/logout/", json=data, headers=headers)
print(response.status_code, response.json())