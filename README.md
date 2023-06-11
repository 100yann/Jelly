# Jelly AutoMate

A program that I created for work that helps me delete old video exports and with automating the task of creating new folders for new items with the proper naming convention.

![Untitled-1](https://github.com/100yann/Jelly/assets/111984273/4dbe47c8-d70d-429d-84f7-75b2cf1b8140)


When deleting exports, it has to go through multiple folders, each containing a long path of folders, to get to any potential exports. Then it compares their creation date to a time frame specified by the user - for example delete all files older than 30 days.
To create a new folder, I used Monday API to check for all items assigned to a user, and if any are started today, it will copy the folder structure to the user-specified path and rename all necessary files and subfolders as per our naming convention.

Libraries used:
- [CustomTkinter](https://customtkinter.tomschimansky.com/documentation/), courtesy of Tom Schimansky
- Requests to connect to Monday's API
- Pathlib to go through directories

The Monday API Key is stored in an Environment Variable so to use this, you'd need your own key.
