from flask import Flask
import requests



data={"name": "", "year":"2018","course":"Cardio","school":"Monastir"}
rq = requests.post("http://localhost:8080/data", json=data)

print(rq.text)