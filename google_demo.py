import sys, shutil
from datetime import datetime, timedelta
from pathlib import Path
from Google import Create_Service, RFC_time
from googleapiclient.http import MediaFileUpload


def itemsOlderThanAWeek():
    if(Path('cached_folder.txt').exists()):
        FOLDER_ID = open("cached_folder.txt", "r").readline()
        week_ago = datetime.today() - timedelta(days=7)
        week_ago = RFC_time(week_ago.year, week_ago.month, week_ago.day, week_ago.hour, week_ago.minute)
        items = service.files().list(q="createdTime <= '{0}' and '{1}' in parents".format(week_ago, FOLDER_ID), spaces='drive', fields='files(name, id)').execute()
        return items
    else:
        print("The cached folder ID doesn't yet exist.")

def generateFolderName():
    return "{}-{}-{} | {}:{}:{}".format(
        datetime.today().month,
        datetime.today().day,
        datetime.today().year,
        datetime.today().hour,
        datetime.today().minute,
        datetime.today().second
        )

def generateSubDirectory(drive_service, f_id):
    folder_meta = {
        'name' : generateFolderName(),
        'mimeType' : 'application/vnd.google-apps.folder',
        'parents' : [f_id]
    }
    f = drive_service.files().create(body=folder_meta, fields='id').execute()
    return f['id']

def populateSubDirectory(drive_service, target, parent_folder_id):
    if not Path("file_cache").exists():
        Path("file_cache").mkdir()
    for f in Path(target).iterdir():
        if f.is_file():
            f_name = str(f.name)
            mime = "text/plain"
            file_meta = {
                'name' : f_name,
                'mimeType' : mime,
                'parents' : [parent_folder_id]
            }
            print("Uploading {} to Drive. Please wait...".format(f_name))
            shutil.copyfile(str(f), 'file_cache/{}'.format(f_name))
            media = MediaFileUpload('file_cache/{}'.format(f_name))
            drive_service.files().create(body=file_meta, media_body=media).execute()
            print("Finished uploading {}.\n".format(f_name))


if __name__ == '__main__':
    console_args = sys.argv
    target_path = console_args[1]
    folder_name = console_args[2]

    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    FOLDER_PATH = Path("cached_folder.txt")
    FOLDER_ID = ""
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    # the file exists
    if FOLDER_PATH.exists():
        # the file exists but doesn't contain the folder ID
        if FOLDER_PATH.stat().st_size == 0:
            print("No folder ID exists. Retrieving folder: [{0}]'s ID from Google Drive.".format(folder_name))
            result = service.files().list(q="name='{0}'".format(folder_name), spaces='drive', fields='files(name, id)').execute()
            cached_id = open("cached_folder.txt", "w")
            cached_id.write(result.get('files')[0]['id'])
            cached_id.close()
            FOLDER_ID = result.get('files')[0]['id']

        # the file exists and contains the folder's ID
        elif FOLDER_PATH.stat().st_size > 0:
            print("Folder ID exists. Retrieving folder: [{0}]'s ID from cache.".format(folder_name))
            cached_id = open("cached_folder.txt", "r")
            FOLDER_ID = cached_id.readline()
            cached_id.close()

    # the file doesn't exist
    else:
        print("No folder ID exists. Caching folder: [{0}]'s ID from Google Drive to cached_folder.txt.".format(folder_name))
        cached_id = open("cached_folder.txt", "w")
        result = service.files().list(q="name='{0}'".format(folder_name), spaces='drive', fields='files(name, id, modifiedTime)').execute()
        FOLDER_ID = result.get('files')[0]['id']
        cached_id.write(FOLDER_ID)
        cached_id.close()

    res = itemsOlderThanAWeek()

    """
    We now have the target folder's ID and a collection of items older than a week.
    Now we are ready to add sub-directories with files within them.
    """

    folder = generateSubDirectory(service, FOLDER_ID)
    populateSubDirectory(service, target_path, folder)
    shutil.rmtree('file_cache')
