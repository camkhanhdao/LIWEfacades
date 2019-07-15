#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 01:36:39 2018
@author: camkhanhdao
NOTE: information can only be changed via modifying credentials.py file
"""

import drive_download
import credentials


# global variables
file_code = credentials.get_code()
file_id_dict = credentials.get_id()
file_name_dict = credentials.get_file()
path = credentials.get_path("path")
path_old = credentials.get_path("path_old")


class LoadData:

    def __init__(self, file, file_id, path_name=path):
        self.file = file
        self.file_id = file_id
        self.path_name = path_name

    def download(self):
        # download from drive
        filename = file_name_dict.get(self.file)
        file_id = file_id_dict.get(self.file_id)
        drive_download.download_file_from_google_drive(id=file_id, destination=self.path_name + filename)


def main():
    load_voltage_data = LoadData(1, 1).download()
    load_humidity_data = LoadData(2, 2).download()
    load_irradiance_data = LoadData(3, 3).download()


if __name__ == "__main__":
    main()
