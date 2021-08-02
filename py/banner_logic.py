"""
Collection of functions for logic on which banners to display
"""


import pandas as pd
from datetime import datetime as dt

t_ind = 4

dat_path = "D:\\Projects\\Data_eng\\py\\data\\csv\\csv\\"

clicks_df = pd.read_csv(dat_path + f"{t_ind}\\clicks_{t_ind}.csv")
conv_df = pd.read_csv(dat_path + f"{t_ind}\\conversions_{t_ind}.csv")
imp_df = pd.read_csv(dat_path + f"{t_ind}\\impressions_{t_ind}.csv")

# X is the number of banners with conversions within a campaign
# X>10

conv_click_df = pd.merge(conv_df, clicks_df, how='outer', on='click_id')


def get_banners(imp_df, conv_click_df, camp_id):
    camp_frame = conv_click_df[conv_click_df['campaign_id'] == camp_id]

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
            dummy_series = imp_df[(imp_df['campaign_id'] == camp_id) & (~imp_df['banner_id'].isin(dummy_list))]['banner_id']
            dummy_list.append(list(dummy_series.sample(5-len(dummy_list)).values))

        return list(pd.core.common.flatten(dummy_list))