import urllib.request
import traceback
import re
import os
import sys
import json

class UpdatePlugins:

    def __init__(self):
        template = {
            "(PLUGIN PATH)": {
                "URL": "(URL TO ROLLING PLUGIN DOWNLOAD OR GITHUB API)",
                "github": "(Parses the github api instead of expecting a direct download. Optional - assumes false)"
                "file_index": "( GITHUB ONLY: The index of which file to download. Optional - assumes 0 (The first package))"
                "file_regex": "( GITHUB ONLY: Regex to match which file to download. Optional - Overrides file_index))"
            },
            "./plugins/EssentialsX.jar": {
                "URL": "https://api.github.com/repos/EssentialsX/Essentials/releases/latest",
                "github": True,
                "file_regex": "EssentialsX-.*.jar"
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
                    self.getGithubURL(metaData['URL'], metaData.get('file_regex', None), metaData.get('file_index', 0)),
                    plugin
                )
            else:
                self.downloadFile(
                    metaData['URL'],
                    plugin
                )

    def getGithubURL(self, url, file_regex=None, file_index=0):
        try:
            with urllib.request.urlopen(url) as resp:
                data = json.load(resp)
            print("[PLUGIN UPDATE INFO] Connected to Github API.")

            if file_regex:
                pattern = re.compile(file_regex)
                for file in data["assets"]:
                    if pattern.match(file['name']):
                        url = file["browser_download_url"]
                        break
            else:
                url = data["assets"][file_index]["browser_download_url"]
            return url
        except Exception as e:
            print(f"[PLUGIN UPDATE ERROR] Github API Call Failed, Update Aborted. {e}")
            return None, None

    def downloadFile(self, url, file_path):
        filename = os.path.basename(file_path)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp, open(file_path, 'wb') as out_file:
                out_file.write(resp.read())
            print(f"[PLUGIN UPDATE INFO] Updated Package {filename}.")
            return True
        except Exception as e:
            print(f"[PLUGIN UPDATE ERROR] Download Failed, Updated of {filename} Aborted. {e}")
            return False


if __name__ == "__main__":
    UpdatePlugins()
