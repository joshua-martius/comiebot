import requests
import json

class git():
    def exec(self):
        response = requests.get("https://api.github.com/repos/y0sh1DE/comiebot/issues")
        js = json.loads(response.text)

        bugs = []
        for key in js:
            for label in key["labels"]:
                if label["name"] == "bug":
                    bugs.append(key["title"])

        output = "Ich habe aktuell folgende Fehler:\n"
        for bug in bugs:
            output = output + "--> " + bug + "\n"

        return output
