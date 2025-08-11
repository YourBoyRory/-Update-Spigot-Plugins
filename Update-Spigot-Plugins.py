import urllib.request
import requests
import traceback
import os
import sys
import json

class UpdatePlugins:

    def __init__(self):
        template = {
            "(PLUGIN PATH)": {
                "URL": "(URL TO ROLLING PLUGIN DOWNLOAD OR GITHUB API)",
                "github": "(Use the github api. Optional - assumes false)"
            },
            "./plugins/Geyser-Spigot.jar": {
                "URL": "https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot"
            },
            "./plugins/Floodgate-Spigot.jar": {
                "URL": "https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot"
            },
            "./plugins/ViaVersion.jar": {
                "URL": "https://api.github.com/repos/ViaVersion/ViaVersion/releases/latest",
                "github": True
            }
        }

        file_path = 'update_plugins.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            with open(f"template_{file_path}", 'w') as f:
                json.dump(template, f, indent=2)

        for plugin, metaData in data.items():
            if "github" in metaData and metaData['github'] == True:
                self.downloadFile(
                    self.getGithubURL(metaData['URL']),
                    plugin
                )
            else:
                self.downloadFile(
                    metaData['URL'],
                    plugin
                )

    def getGithubURL(self, url):
        try:
            response = requests.get(url).json()
            print("[INFO] Connected to Github API.")
            return response["assets"][0]["browser_download_url"]
        except Exception as e:
            print("[ERROR] Github API Call Failed, Update Aborted. {e}")
            return None, None

    def downloadFile(self, url, file_path):
        filename = os.path.basename(file_path)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"[INFO] Updated Package {filename}.")
            return True
        except Exception as e:
            print(f"[ERROR] Download Failed, Updated of {filename} Aborted. {e}")
            return False


if __name__ == "__main__":
    UpdatePlugins()
