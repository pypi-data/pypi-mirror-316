from os import sep
import pandas as pd
from ...utils.convert_timestamp import *
import warnings

warnings.filterwarnings("ignore")

from datetime import datetime, timedelta


def get_previous_date(date_str: str) -> str:
    try:
        # Convert the input string to a datetime object
        date = datetime.strptime(date_str, "%Y-%m-%d")
        # Subtract one day using timedelta
        previous_date = date - timedelta(days=1)
        # Convert the previous date back to a string
        return previous_date.strftime("%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Please use 'YYYY-MM-DD'."


def date_str_to_datetime(date_str):
    split = date_str.split(" ")
    if len(split) > 2:
        date_str = split[0] + " " + split[1]

    if "/" in date_str:
        dd = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S.%f')
    elif "-" in date_str:
        dd = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
    else:
        dd = np.nan
    return dd

def day_str_to_datetime(date_str):
    split = date_str.split(" ")
    if len(split) > 2:
        date_str = split[0] + " " + split[1]

    if "/" in date_str:
        dd = datetime.strptime(date_str, '%m/%d/%Y')
    elif "-" in date_str:
        dd = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        dd = np.nan
    return dd

def find_indices(my_list, element):
    return [i for i, x in enumerate(my_list) if x == element]


class Found(Exception):
    pass


def trim_two_lists(foreground_indices, background_indices):
    # Initialize new lists for trimmed indices
    foreground_indices_new = []
    background_indices_new = []

    # Handle edge cases where any list is empty
    if len(foreground_indices) == 0 or len(background_indices) == 0:
        return foreground_indices_new, background_indices_new, None

    j = 0
    try:
        for i in range(len(foreground_indices)):
            if i == len(foreground_indices) - 1:
                f_idx = foreground_indices[i]
                if j > len(background_indices) - 1:
                    break
                b_idx = background_indices[j]
                if b_idx > f_idx:
                    foreground_indices_new.append(f_idx)
                    background_indices_new.append(b_idx)
                else:
                    continue
            else:
                f_idx = foreground_indices[i]
                f2_idx = foreground_indices[i + 1]
                b_idx = background_indices[j]
                while f_idx > b_idx:
                    j += 1
                    if j > len(background_indices) - 1:
                        raise Found
                    b_idx = background_indices[j]
                if b_idx < f2_idx:
                    foreground_indices_new.append(f_idx)
                    background_indices_new.append(b_idx)
                    j += 1
                    if j > len(background_indices) - 1:
                        break
                else:
                    continue
    except Found:
        pass

    return foreground_indices_new, background_indices_new


def parse_raw_df(df_hour_raw, time_zone):
    columns_names = ["LOG_TIME", "LAST_HOUR_TIMESTAMP", "CURRENT_HOUR_TIMESTAMP", "APP_PACKAGE_NAME", "EVENT_TIMESTAMP",
                     "APP_EVENT"]
    if df_hour_raw.shape[0] > 0:
        df_hour_raw.fillna('-1', inplace=True)
        df_hour_raw.columns = columns_names
        df_hour_raw['LOG_TIME'] = [x + " " + time_zone for x in df_hour_raw['LOG_TIME']]
        df_hour_raw['LAST_HOUR_TIME'] = convert_timestamp_int_list_to_readable_time(df_hour_raw['LAST_HOUR_TIMESTAMP'],
                                                                                    time_zone)
        df_hour_raw['CURRENT_HOUR_TIME'] = convert_timestamp_int_list_to_readable_time(
            df_hour_raw['CURRENT_HOUR_TIMESTAMP'],
            time_zone)
        df_hour_raw['EVENT_TIME'] = convert_timestamp_int_list_to_readable_time(df_hour_raw['EVENT_TIMESTAMP'],
                                                                                time_zone)
        df_hour_raw = df_hour_raw[
            ["LOG_TIME", "LAST_HOUR_TIMESTAMP", 'LAST_HOUR_TIME', "CURRENT_HOUR_TIMESTAMP", 'CURRENT_HOUR_TIME',
             "APP_PACKAGE_NAME", "EVENT_TIMESTAMP", 'EVENT_TIME', "APP_EVENT"]]
    return df_hour_raw


# def create_gap_time_list(df_usage_t_a):
#     gap_time_list = []
#     # First, find indices of foreground, indices of background
#     foreground_indices = find_indices(df_usage_t_a.APP_EVENT, "MOVE_TO_FOREGROUND")
#     background_indices = find_indices(df_usage_t_a.APP_EVENT, "MOVE_TO_BACKGROUND")
#
#     # trim two lists
#     foreground_indices_new, background_indices_new = trim_two_lists(foreground_indices, background_indices)
#
#     # compute the gaps
#     for i in range(len(foreground_indices_new)):
#         usage_start_t = df_usage_t_a.loc[foreground_indices_new[i], "EVENT_TIME_DT"]
#         usage_stop_t = df_usage_t_a.loc[background_indices_new[i], "EVENT_TIME_DT"]
#         if pd.isna(usage_start_t) or pd.isna(usage_stop_t):
#             continue
#             # print(usage_stop_t)
#         gap_time_list.append((usage_stop_t - usage_start_t).total_seconds() / 60)
#     return gap_time_list


def get_start_end_time(df_participant_a, current_date_dt):
    start_time_a_list = []
    end_time_a_list = []

    # First, find indices of foreground, indices of background
    foreground_indices = find_indices(df_usage_t_a.APP_EVENT, "MOVE_TO_FOREGROUND")
    background_indices = find_indices(df_usage_t_a.APP_EVENT, "MOVE_TO_BACKGROUND")

    # trim two lists
    foreground_indices_new, background_indices_new = trim_two_lists(foreground_indices, background_indices)

    # compute the gaps
    for i in range(len(foreground_indices_new)):
        usage_start_t = df_usage_t_a.loc[foreground_indices_new[i], "EVENT_TIME_DT"]
        usage_stop_t = df_usage_t_a.loc[background_indices_new[i], "EVENT_TIME_DT"]
        # skip yesterday's app usage and record from the first app usage ends at today
        if usage_stop_t < current_date_dt:
            continue
        start_time_a_list.append(df_usage_t_a.loc[foreground_indices_new[i], "EVENT_TIME"])
        end_time_a_list.append(df_usage_t_a.loc[background_indices_new[i], "EVENT_TIME"])

    return start_time_a_list, end_time_a_list


def get_foreground_matrix(df_participant_currentday_path, df_participant_yesterday_path, date):
    df_foreground = pd.DataFrame()

    # get foreground start and end time, organized by app
    app_package_list = []
    start_time_list = []
    end_time_list = []

    # combine both today and yesterday's intermediate app usage csv
    df_participant_currentday = pd.read_csv(df_participant_currentday_path)
    df_participant_yesterday = pd.read_csv(df_participant_yesterday_path)
    df_participant = pd.concat([df_participant_yesterday, df_participant_currentday], ignore_index=True)
    df_participant = df_participant[df_participant.APP_EVENT.isin(['MOVE_TO_FOREGROUND', 'MOVE_TO_BACKGROUND'])]
    df_participant["EVENT_TIME_DT"] = df_participant.EVENT_TIME.apply(lambda x: date_str_to_datetime(x))
    current_date_dt = day_str_to_datetime(date)

    for app_package in df_participant.APP_PACKAGE_NAME.unique():
        df_participant_a = df_participant[df_participant.APP_PACKAGE_NAME == app_package]
        df_participant_a.reset_index(inplace=True, drop=True)

        # gap_time_list = create_gap_time_list(df_participant_a)
        start_time_a_list, end_time_a_list = get_start_end_time(df_participant_a, current_date_dt)
        app_package_a_list = [app_package] * len(start_time_a_list)
        app_package_list.extend(app_package_a_list)
        start_time_list.extend(start_time_a_list)
        end_time_list.extend(end_time_a_list)

    # dataframe
    # pid
    pid_text = df_participant.loc[0, "PARTICIPANT_ID_TEXT"]
    pid_numeric = df_participant.loc[0, "PARTICIPANT_ID_NUMERIC"]

    list_len = len(start_time_list)
    df_foreground["PARTICIPANT_ID_TEXT"] = [pid_text] * list_len
    df_foreground["PARTICIPANT_ID_NUMERIC"] = [pid_numeric] * list_len
    df_foreground["APP_PACKAGE_NAME"] = app_package_list
    df_foreground["EVENT_START_TIME"] = start_time_list
    df_foreground["EVENT_END_TIME"] = end_time_list

    return df_foreground

#
# def get_foreground_matrix_minute(df_foreground):
#     return df_foreground_minute
#
#
# def get_foreground_matrix_hour(df_foreground_minute):
#     return df_foreground_hour
#
#
# def get_foreground_matrix_day(df_foreground_hour):
#     return df_foreground_day


if __name__ == "__main__":
    target_file = "Battery.020000000000-Battery.2020-06-02-02-00-25-506-M0400.event.csv"
    hour_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\data-watch\2020-06-02\02-EDT"
    target_file_path = hour_folder_path + sep + target_file
    output_file_path = r"C:\Users\jixin\Desktop\temp\temp_file.csv"
    p_id = "aditya4_internal@timestudy_com"

    df_hour_raw = pd.read_csv(target_file_path)
    print(df_hour_raw)
    df_hour_parsed = parse_raw_df(df_hour_raw)
    df_hour_parsed.to_csv(output_file_path, index=False)
