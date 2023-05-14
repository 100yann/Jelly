from pathlib import Path
import datetime as dt
import requests
import json
import os


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
        item_name = result['name'] # get name
        item_id = result['id'] # get id
        item_status = result['column_values'][0]['text'] # get status
        date_changed = result['column_values'][0]['additional_info'][55:65] # get date the status was changed
        if item_status == "PRE-EDITING":

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


