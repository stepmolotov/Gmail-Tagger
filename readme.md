**Gmail Auto Tagger**

Retrieves the latest emails from your inbox and extracts keywords and the main topic from them.
It uses the Gmail API to retrieve the emails and the Marvin to extract the keywords and the main topic.

In order to have access to the Gmail API, you need to have a project in the Google Cloud Console and enable the Gmail API for it. After that, you need to create a set of credentials and download the json file.
For more information, check the following link: https://developers.google.com/gmail/api/troubleshoot-authentication-authorization

**Installation**

To install the requirements in a new conda environment, run the following command:
```bash
conda create -n gmail python=3.11
conda activate gmail
pip install -r requirements.txt
```

Make sure to have the following environment variables set:
```bash
OA_KEY=your_openai_key
```

**Usage**

Run the following command to see it in action:
```bash
python3 -m src.main
```

The first time you run it, it will ask you to authenticate with your gmail account. 
After that, it will retrieve the latest emails and feed them to the model in order to extract the keywords and the main topic.
