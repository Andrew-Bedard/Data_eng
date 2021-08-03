"""
Collection of functions for logic on which banners to display
"""


import pandas as pd
from datetime import datetime as dt
import os

def dat_check(dat_path, log_path):

    import collections

    """
    Simple data sanity checks (duplicates)

    :param dat_path: STR, path to bottom level csv directory
    :return:
    """

    file_list = []
    ext_list = ['.csv']  # hard coded, for now

    for path, subdirs, files in os.walk(dat_path):
        for name in files:
            file_list.append(name)

    # Remove any files that may not have an expected extension associated with them
    file_list = [file for file in file_list if file[-4:] in ext_list]

    # Check file_list for duplicates
    dupe_list = [item for item, count in collections.Counter(file_list).items() if count > 1]

    # If duplicates, write to log file
    if len(dupe_list) > 0:
        with open(log_path, 'a') as log_file:
            log_file.write(f'WARNING: Duplicate file entries: {dupe_list}, {dt.now()}, extension of newest files '
                           f'modified with ~ to prevent conflicts. \n')

        # Change extension of older files to mask them from loading function

        for file in dupe_list:
            full_dupe_path = []
            for path, subdirs, files in os.walk(dat_path):
                for name in files:
                    if name == file:
                        full_dupe_path.append(os.path.join(path, name))
                        # Remove any files that may not have an expected extension associated with them

                        file_age = [os.stat(file).st_mtime for file in full_dupe_path]
                        min_index = file_age.index(min(file_age))

                        [os.rename(i, i + '_DUPE') for i in full_dupe_path if full_dupe_path.index(i) != min_index]

    return

def load_frames(dat_path):

    """
    Tidy load of clicks, conversions and impression dataframes. Dataframes are selected base don time

    :param dat_path: STR, path to bottom level csv directory
    :return:
    """

    current_minute = dt.now().minute

    if current_minute in range(16):
        t_ind = 1
    elif current_minute in range(16, 31):
        t_ind = 2
    elif current_minute in range(31, 46):
        t_ind = 3
    else:
        t_ind = 4

    clicks = pd.read_csv(dat_path + f"{t_ind}\\clicks_{t_ind}.csv")
    conv = pd.read_csv(dat_path + f"{t_ind}\\conversions_{t_ind}.csv")
    imp = pd.read_csv(dat_path + f"{t_ind}\\impressions_{t_ind}.csv")

    return clicks, conv, imp


def get_banners(imp_df, conv_click_df, camp_id, banner_blacklist=None):

    """
    Get banners based on impressions, conversions and clicks for specific campaign

    :param imp_df: DATAFRAME, impressions dataframe
    :param conv_click_df: DATAFRAME, outer join of conversion and clicks dataframe joined on click_id
    :param camp_id: INT, campaign id number
    :param banner_blacklist: LIST of INT, list of banner ids that are removed from pool of possible banners to be shown
    :return:
    """

    if banner_blacklist is None:
        banner_blacklist = []
    if not type(camp_id) == int:
        camp_id = int(camp_id)

    camp_frame = conv_click_df[conv_click_df['campaign_id'] == camp_id]

    # TODO: this logic is a little silly, figure out a better way of filtering out 'black list' banners
    camp_frame = camp_frame[~camp_frame['banner_id'].isin(banner_blacklist)]
    imp_frame = imp_df[~imp_df['banner_id'].isin(banner_blacklist)]


    if len(camp_frame[~camp_frame['conversion_id'].isna()]['banner_id'].unique()) >= 10:
        # If >= 10, get list of top 10 by revenue
        dummy = camp_frame.groupby(['banner_id']).sum()['revenue']

        return list(dummy.sort_values(axis=0, ascending=False)[0:10].index)

    elif len(camp_frame[~camp_frame['conversion_id'].isna()]['banner_id'].unique()) in range(5, 10):
        # If in range(5, 10), get list of top revenue
        banner_conv_num = len(camp_frame[~camp_frame['conversion_id'].isna()]['banner_id'].unique())
        dummy = camp_frame.groupby(['banner_id']).sum()['revenue']
        return list(dummy.sort_values(axis=0, ascending=False)[0:banner_conv_num].index)

    elif len(camp_frame[~camp_frame['conversion_id'].isna()]['banner_id'].unique()) in range(1, 5):
        # If range (1, 5), get top x, plus top 5-x with most clicks
        banner_conv_num = len(camp_frame[~camp_frame['conversion_id'].isna()]['banner_id'].unique())
        dummy = camp_frame.groupby(['banner_id']).sum()['revenue']
        dummy_list = list(dummy.sort_values(axis=0, ascending=False)[0:banner_conv_num].index)

        # Get banners with most clicks
        dummy = camp_frame.groupby(['banner_id']).count()['click_id']
        dummy_list.append(list(dummy.sort_values(axis=0, ascending=False)[0:5 - banner_conv_num].index))

        return list(pd.core.common.flatten(dummy_list))  # Flatten list before returning in case of nested lists from
        # append

    else:

        dummy = camp_frame.groupby(['banner_id']).count()['click_id']
        dummy_list = list(dummy.sort_values(axis=0, ascending=False).index)

        if len(dummy_list) < 5:
            dummy_series = imp_frame[(imp_df['campaign_id'] == camp_id) & (~imp_frame['banner_id'].isin(dummy_list))]['banner_id']
            dummy_list.append(list(dummy_series.sample(5-len(dummy_list)).values))

        return list(pd.core.common.flatten(dummy_list))




# dat_path = "D:\\Projects\\Data_eng\\py\\data\\csv\\csv\\"
#
# clicks_df, conv_df, imp_df = load_frames(dat_path)
#
# conv_click_df = pd.merge(conv_df, clicks_df, how='outer', on='click_id')
#
# thing = get_banners(imp_df, conv_click_df, camp_id)

