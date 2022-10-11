from os import path
import pandas as pd
from yt_stats import YTstats
from tqdm import tqdm
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def get_views():
    API_KEY = 'AIzaSyBeEE1qWFn8irWyxP5lexdEPSH5dPs8VHY'

    df = pd.read_excel("youtube_video_channel_ID.xlsx")

    current_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    for x, y in tqdm(zip(df["Video ID"], df["Channel ID"])):

        if not path.exists(f"{x}.xlsx"):
            df2 = pd.DataFrame(columns=['CREATED AT', 'VIEWS'])
            # df2.to_excel(f"{x}.xlsx")
        else:
            df2 = pd.read_excel(f"{x}.xlsx")
        channel_id = y
        video_id = x
        part = 'statistics'
        yt = YTstats(API_KEY, channel_id)
        a = yt._get_single_video_data(video_id, part)
        data = {'CREATED AT': current_date_and_time, 'VIEWS': a['viewCount']}
        new_df = pd.DataFrame([data])
        df2 = pd.concat([df2, new_df], axis=0, ignore_index=True)
        df2.to_excel(f"{x}.xlsx", index=False)
        df2 = pd.DataFrame(None)


scheduler = BlockingScheduler()
scheduler.add_job(get_views, 'interval', hour=24)
scheduler.start()
