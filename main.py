import os
import datetime as dt
from datetime import timedelta
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import requests
import json


# os.getcwd() - get current directory
# os.chdir() - change directory to specified path
# os.listdir() - list all files and subdirectories
# os.remove(file) - removes file in current directory
# os.path.getctime(file dir) - returns time of creation of specified file

# root=tk.Tk()
# root.geometry('1280x720')
# root.config(pady=50)
# options_label = tk.Label(
#     text='Choose an option'
# )
# options_label.pack()

monday_api_key = os.environ.get('MONDAY_API')
api_url = 'https://api.monday.com/v2'
headers = {'Authorization': monday_api_key}
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
for result in results:
    item_id = result['id'] # get id
    item_status = result['column_values'][0]['text'] # get status
    date_changed = result['column_values'][0]['additional_info'][55:65] # get date the status was changed
    if item_status == "PRE-EDITING" and date_changed == str(today):

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
        prod_id = f"CRE{creator_id}S{season_number}E{episode_number}"




# def del_files():
#     file_path = filedialog.askdirectory()
#     options_label.destroy()
#     del_exports.destroy()
#     instructions = tk.Label(
#         root,
#         text='Files older than X days should be deleted'
#     )
#     instructions.pack()
#     user_input = tk.Entry(
#         root,
#         width=100
#     )
#     user_input.pack()


#     def init_delete():
#         root_dir = Path(file_path)
#         for subdir in root_dir.iterdir():
#             if 'SEASON' in subdir.name:
#                 open_season = root_dir.joinpath(subdir)
#                 for episode in open_season.iterdir():
#                     if 'CREXXX' not in episode.name:
#                         final_dir = root_dir / subdir / episode / '1_EXPORTS' / '1_MASTERS' / '3_FACEBOOK'
#                         try:
#                             for export in final_dir.iterdir():
#                                 creation_date = os.path.getctime(final_dir/export)
#                                 readable_date = dt.datetime.fromtimestamp(creation_date).date()
#                                 if readable_date <= dt.date.today() - timedelta(days=int(user_input.get())):
#                                     os.remove(final_dir/export)
#                         except FileNotFoundError:
#                             pass
                            
#     delete = tk.Button(
#         text='Delete',
#         command=init_delete
#     ).pack()




# del_exports = tk.Button(
#     text='Delete Exported Files',
#     command=del_files
# )
# del_exports.pack()


# root.mainloop()
