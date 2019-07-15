#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 01:36:39 2018
@author: camkhanhdao

"""
import pandas as pd
import datetime
import numpy as np
import credentials

""" NOTE: information can only be changed via modifying credentials.py file """
file_name_dict = credentials.get_file()
path = credentials.get_path("path")
path_old = credentials.get_path("path_old")
sorted_path = credentials.get_path("sorted_path")

file_code = credentials.get_code()
R1 = credentials.get_resistant()  # Resistant 1
R2 = credentials.get_resistant(2)  # Resistant 2

PV_dict = {1: 'v1', 2: 'v2', 3: 'v3', 4: 'v4'}
month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
              5: 'May', 6: 'June', 7: 'July', 8: 'August',
              9: 'September', 10: 'October', 11: 'November', 12: 'December'}
error = 'coerce'  # when set datetime, invalid parsing will be set as NaT


class ReadData:

    def __init__(self, file, path_name=path_old):
        self.file = file
        self.path_name = path_name

    def read_file(self):
        filename = file_name_dict.get(self.file)
        try:
            df = pd.read_csv(self.path_name + filename, header=None, delimiter=',',
                             error_bad_lines=False, engine='c')  # skip the odd line
        except Exception:
            df = pd.read_csv(self.path_name + filename, header=None, delimiter=',',
                             error_bad_lines=False, engine='python')  # skip the odd line
        df = pd.DataFrame(df)
        return df

    def read_voltage(self):
        df = ReadData.read_file(self)
        df.columns = ['Datetime', 'Volt1', 'Volt2', 'Volt3', 'Volt4', 'Temperature']  # change str to date time
        columns = ['Volt1', 'Volt2', 'Volt3', 'Volt4']
        # change all value of the columns to numeric
        df['Volt1'] = pd.to_numeric(df['Volt1'], errors=error)
        df['Volt2'] = pd.to_numeric(df['Volt2'], errors=error)
        df['Volt3'] = pd.to_numeric(df['Volt3'], errors=error)
        df['Volt4'] = pd.to_numeric(df['Volt4'], errors=error)
        df['Datetime'] = pd.to_datetime(df['Datetime'], errors=error).values.astype('<M8[s]')
        df = df.set_index(df['Datetime']).drop(labels='Datetime', axis=1).dropna(axis=0, how='any')
        for column in columns:
            r = (R1 + R2) / R2
            df = df.drop(df[df[column] >= 5].index)  # iterate through the columns, and drop the rows where voltage >5
            df[column] = df[column] * r

        return df.drop_duplicates()

    def read_humidity(self):
        df = ReadData.read_file(self)
        df.columns = ['Datetime', 'Humidity']
        df['Humidity'] = df['Humidity'].str.replace(r"\(.*\)", "")
        df['Humidity'] = pd.to_numeric(df['Humidity'], errors=error)
        df['Datetime'] = pd.to_datetime(df['Datetime'], errors=error).values.astype('<M8[s]')
        df = df.set_index('Datetime').dropna(axis=0, how='any')
        return df.drop_duplicates()

    def read_irradiance(self):
        df = ReadData.read_file(self)
        df.columns = ['Datetime', 'Irradiance(W)']
        df['Irradiance(W)'] = df['Irradiance(W)'].str.replace(r"\(.*\)", "")
        df['Irradiance(W)'] = pd.to_numeric(df['Irradiance(W)'], errors=error)
        df['Datetime'] = pd.to_datetime(df['Datetime'], errors=error).values.astype('<M8[s]')
        df = df.set_index('Datetime').dropna(axis=0, how='any')
        return df.drop_duplicates()


class CleanData:

    def __init__(self, dataframe, file, year=2018, path_name=sorted_path):
        self.dataframe = dataframe
        self.file = file
        self.path_name = path_name
        self.year = year

    def get_folder(self):
        folder = file_code.get(self.file)
        return self.path_name + folder + '/'

    # normalization
    def normalization(self, day, month):
        """This function normalized the data of each day by grouped and
        calculate the mean of measurement data in every minute. """
        str_month = month_dict.get(month)
        df = self.dataframe[self.dataframe.index.date == datetime.date(self.year, month, day)]
        for i in range(0, 24):
            try:
                output = df[df.index.hour == i]
                output = round(output.resample("1Min").mean(), 2)

                folder = CleanData.get_folder(self) + str_month + '/'
                with open(folder + (str_month + str(day) + '.csv'), 'a+') as f:
                    output.to_csv(f, header=False)
                f.close()
            except ValueError:
                pass

    def iteration(self, month):
        """iterate through all day of the month and normalize the data
        this function will fill the folder of each month with daily data
        in which each data point is normalized"""
        for day in range(1, 32):
            try:
                CleanData.normalization(self, day, month)
            except ValueError:
                pass

    def month_data(self, month):
        """ This function accumulates all the daily data of a month
        and stores in a csv file"""
        str_month = month_dict.get(month)
        folder = CleanData.get_folder(self) + str_month + '/'
        for day in range(1, 32):
            try:
                f = pd.read_csv(folder + (str_month + str(day) + '.csv'), header=None)
                f = pd.DataFrame(f)
                with open(folder + str_month + '.csv', 'a+') as file:
                    f.to_csv(file, header=False)
            except (pd.errors.EmptyDataError, FileNotFoundError):
                pass

    def clean_data(self):
        for month in range(6, 12):
            try:
                CleanData.iteration(self, month)
                CleanData.month_data(self, month)
            except FileNotFoundError:
                pass


class ReadNormalized:

    def __init__(self, file, year=2018):
        self.file = file
        self.path_name = path_name
        self.year = year

    def read_month(self, month):
        str_month = month_dict.get(month)
        folder = CleanData.get_folder(self) + str_month + '/'
        df = pd.read_csv(folder + str_month + '.csv', header=None, index_col=0)
        if self.file == 1:
            df.columns = ['index', 'v1', 'v2', 'v3', 'v4', 'T']

        elif self.file == 2:
            df.columns = ['index', 'hum']

        elif self.file == 3:
            df.columns = ['index', 'irr']

        df['index'] = pd.to_datetime(df['index'], errors='coerce').values.astype('<M8[s]')
        df.set_index('index', drop=True, inplace=True)
        return df

    def merger(month):
        full = pd.merge((pd.merge(ReadNormalized(1).read_month(month),
                        ReadNormalized(3).read_month(month), left_index=True, right_index=True)),
                        ReadNormalized(2).read_month(month), left_index=True, right_index=True)
        return full


def main_merge():
    df_list = []
    for month in range(6, 12):
        try:
            df_list.append(ReadNormalized.merger(month))
        except FileNotFoundError:
            pass

    df = pd.concat(df_list)
    df['irr'] = df['irr'].apply(lambda x: x * 0.1)
    df['irr_index'] = round(df['irr'], -1)
    df['hum_index'] = round(df['hum'], -1)
    df['T_index'] = round(df['T'].astype(np.float64), -1)

    df = df[df.irr_index < 120]
    df = df[df.hum >= 0]
    df = df[df.hum <= 100]
    return df



