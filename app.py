from flask import Flask, request, jsonify
import requests
import urllib.request, urllib.error, urllib.parse
import json

bearer = "YOUR_ACCESS_TOKEN"

def sendSparkGET(url):
    request = urllib.request.Request(url,
                             headers={"Accept" : "application/json",
                                      "Content-Type":"application/json",
                                      "Authorization": "Bearer "+bearer})
    contents = urllib.request.urlopen(request)
    return contents

app = Flask(__name__) #Flask constructor

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        if 'files' in webhook['data']:
            for file_url in webhook['data']['files']:
                response = sendSparkGET(file_url)
                content_disp = response.headers.get('Content-Disposition', None)
                if content_disp is not None:
                    filename = content_disp.split("filename=")[1]#split on the string "filename=", then save the second item as name
                    filename = filename.replace('"', '')
                    with open(filename, 'wb') as f:
                        f.write(response.read())
                        f.close()
                        print(('Saved-', filename))
                else:
                    print("Cannot save file- no Content-Disposition header received.")
        else:
            print("No files attached to retrieve!")

    return "True"

if __name__ == '__main__':
    app.run("0.0.0.0", port=16180, debug=True)
