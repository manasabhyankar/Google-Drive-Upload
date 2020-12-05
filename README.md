# Google-Drive-Upload

A simple utility script leveraging the Google Drive v3 API to upload files to your personal Drive account.

You need to follow the instructions on [this](https://developers.google.com/drive/api/v3/quickstart/python) page to get set-up. Steps 3 and 4 are optional, as the helper Google.py file will conduct authentication and create a *token* file with your authentication details. However, Steps 1 and 2 are mandatory.

## How to use

To run the script, you can use it as a standard Python script run in your command line with arguments. **For example:**

`python google_demo.py <target_path> <folder_name_in_drive>`

**Here's an example usage of this script with real parameters:**

`python google_demo.py D:\python "random folder"`

**Here's an example of what to expect pop-up in your Drive:**


![This is a picture of what to expect in your Drive if you were to run the example command listed above.!](/images/example_usage.png "Example Usage")

### Note:

You will need to allow this app access to your Google Drive in order to upload files. The default scope of this program will be set to the root Drive folder, but it can be changed within the **SCOPES** variable within **google_demo.py**.

I would recommend that you hold onto your "credentials.json" that you should obtain from Step 1 of the link provided at the top of the page so that you don't have to constantly reauthenticate and generate new token, in addition to allowing the same app permission to your Drive repeatedly.

### TODO:

1. Add support for directories in addition to files.
2. Add support for removing sub-directories within the Drive's target folder that are older than a week (in the context of video game save files, a week can mean a lot of old progress that is now out-of-date).
3. Perhaps do some code refactoring...and pretty up the code.