from pathlib import Path
import shutil
import datetime as dt
import requests
import json
import os

SOURCE_FOLDER = Path('FOLDER_STRUCTURE/CREXXXS0E000_NAMEOFEPISODE')
monday_api_key = os.environ.get('MONDAY_API')
api_url = 'https://api.monday.com/v2'
headers = {'Authorization': monday_api_key}

def get_items():
    query = '''
    {
        items_by_multiple_column_values(
            board_id: 1374526431,
            column_id: "person",
            column_values: "Stoyan Kolev") {
                name
                id
                column_values(ids: "status") {
                    text additional_info
            }     
        }
    }

    '''
    data = {'query' : query}
    response = requests.post(url=api_url, json=data, headers=headers)

    results = json.loads(response.text)['data']['items_by_multiple_column_values']

    today = dt.date.today()
    pulses_to_return = {}
    for result in results:
        item_status = result['column_values'][0]['text'] # get status
        if item_status== "PRE-EDITING":
            date_changed = result['column_values'][0]['additional_info'][55:65] # get date the status was changed
            if date_changed == str(today):
                item_name = result['name'] # get name
                item_id = result['id'] # get id

                new_query = '''
                {boards (ids: 1374526431) {
                    items(ids: %s) {
                        column_values(ids: ["dropdown", "text5", "text0"]) {
                            text
                        }
                    }
                }
            }
                '''%item_id

                new_data = {'query': new_query} 
                new_response = requests.post(url=api_url, json=new_data, headers=headers) # make a new query only for the items that pass the check
                new_results = json.loads(new_response.text)['data']['boards'][0]['items'][0]['column_values'] # get final layer of data
                creator_name = new_results[0]['text'].split(' - ')
                creator_id = creator_name[1] # get the creator ID
                season_number = new_results[1]['text'] # get the season number
                episode_number = new_results[2]['text'] # get the episode number
                pulses_to_return[item_name] = dict(cre_id = creator_id, season_num = season_number, ep_num = episode_number)
    return pulses_to_return


def make_folders(path):
    new_pulses = get_items() # call the function that will return the needed items from Monday
    if new_pulses:
        created_folders = []
        creator_folder = Path(path)
        for key, value in new_pulses.items(): # build the necessary file_ids by iterring through the returned monday items
            name = key.split()
            updated_name = ""
            for word in name:
                updated_name += word.title()
            id = value['cre_id']
            season = value['season_num']
            episode = value['ep_num']
            prod_id = f"CRE{id}S{season}E{episode}"
            file_id = f"{prod_id}_{updated_name[0:17]}"
            

            subdirectories = [subdir for subdir in creator_folder.iterdir() if subdir.is_dir()]
            if subdirectories and creator_folder/f"SEASON_{season}" in subdirectories: # check if the "SEASON_X" folder already exists
                    try:
                        creation_path = creator_folder / f"SEASON_{season}"
                        copySourceFolder(file_id, creation_path)
                    except FileExistsError:
                        print(f'The folder {file_id} already exists')
            else: # if it doesn't exist - create a season folder
                create_season = creator_folder / f"SEASON_{season}"
                create_season.mkdir()
                creation_path = creator_folder / f"SEASON_{season}"
                copySourceFolder(file_id, creation_path)
            created_folders.append([file_id, creation_path])
        return created_folders
    else:
        return 0


def copySourceFolder(file_id, path):
    temp_source = SOURCE_FOLDER
    shutil.copytree(SOURCE_FOLDER, path / file_id)
    print(Path(path / file_id / '2_PROJECTS' / '1_PREMIERE_PROJECT' / 'CREXXXS0E000_NAMEOFEPISODE.prproj'))
    rename_premiere = Path(path / file_id / '2_PROJECTS' / '1_PREMIERE_PROJECT' / 'CREXXXS0E000_NAMEOFEPISODE.prproj')
    rename_premiere.rename(Path(rename_premiere.parent, f'{file_id}.prproj'))
    rename_photoshop = Path(path / file_id / '2_PROJECTS' / '2_PHOTOSHOP_PROJECT')
    for file in rename_photoshop.iterdir():
        filename = file.name.replace('CREXXXS0E000_NAMEOFEPISODE', file_id)
        file.rename(Path(file.parent, filename))

    


    
                        


