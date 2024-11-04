## Instruction - Usage

First, let's start editing `Info.txt` with the relevant infomation

Sencond, set up Gmail API:

a. Go to [Google Cloud Console](https://console.cloud.google.com).

b. Create a new project or select an existing one.

c. Enable the [Gmail API](https://console.cloud.google.com/apis/api/gmail.googleapis.com/metrics) for your project.

d. Choose "User data" for the Gmail API data you will be accessing to.

e. Create credentials (OAuth client ID) for a Desktop application.

f. Download the JSON client secret configuration and save it as `credentials.json` in the same directory as this script.

g. Publish the Google app.

Then, install the python dependencies with pip

```console
pip install -r requirements.txt
```

Finally, run the script

```console
python send-2.py # v2 is now the recommand one
```

https://github.com/AppNinjaMarketing/AppNinja-Marketing-Tools/raw/refs/heads/main/Python/EmailMarketer/setup-starting-usaging-send-script.mp4


## Disclaimer (TO READ BEFORE ANY USAGE)

You MUST NOT use this in violation of any laws or terms of service of any online services.

YOU are solely responsible for your use of this product and MUST NOT use it for illegal purposes or to spam users. Neither the script nor its creator can be held responsible in any way for your use of this product.
