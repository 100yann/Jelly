import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import datetime as dt
from datetime import timedelta
import os


def deleteExports(path, date):
    root_dir = Path(path)
    removed_files = []
    for subdir in root_dir.iterdir():
        if 'SEASON' in subdir.name:
            open_season = root_dir.joinpath(subdir)
            for episode in open_season.iterdir():
                if 'CREXXX' not in episode.name:
                    final_dir = root_dir / subdir / episode / '1_EXPORTS' / '1_MASTERS' / '3_FACEBOOK'
                    try:
                        for export in final_dir.iterdir():
                            try:
                                creation_date = os.path.getctime(final_dir/export)
                                readable_date = dt.datetime.fromtimestamp(creation_date).date()
                                if readable_date <= dt.date.today() - timedelta(days=int(date)):
                                    os.remove(final_dir/export)
                                    removed_files.append(export)
                            except PermissionError:
                                pass
                    except FileNotFoundError:
                        pass
    if len(removed_files) == 0:
        print('No matching files were found')
    else:
        for file in removed_files:
            print(f"Deleted {file}")