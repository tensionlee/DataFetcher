from tasks import routine_task
from db import db
import datetime


def run(db):
    # fetch last track date, move 1 day forward
    try:
        result = db.track_date.find()
        for item in result:
            current_date = item["date"]

        next_date = (datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime(
            "%Y-%m-%d")
        print(next_date)
    except Exception as e:
        print(e)

    # execute routine task
    try:
        daily_result, std_result = routine_task.daily_task(current_date)
        monthly_result = routine_task.monthly_task(current_date)
    except Exception as e:
        print(e)

    # save into mongodb
    save_monthly(db, monthly_result)
    save_daily(db, daily_result, std_result, current_date)


def save_daily(db, df, std_df, current_date):
    dates = df.columns
    for date in dates:
        if date.strftime('%Y-%m-%d') == current_date:
            continue
        entry = {
            'date': date.strftime('%Y-%m-%d'),
            'guozhai_1m': df[date]['M1004677'],
            'guozhai_1y': df[date]['M1001646'],
            'guozhai_10y': df[date]['M1001654'],
            'qiyezhai_3a_1y': df[date]['S0059771'],
            'qi_xian_li_cha': df[date]['M1001654'] - df[date]['M1001646'],
            'xin_yong_li_cha': df[date]['S0059771'] - df[date]['M1001646'],
            'jinjia_9995': df[date]['S0035818'],
            'jinjia_9999': df[date]['S0035819'],
            'jinjia_100g': df[date]['S0035820'],
            'std_6m': std_df[date.strftime('%Y-%m-%d')]['stdDev6M'],
            'std_1y': std_df[date.strftime('%Y-%m-%d')]['stdDev1Y'],
            'std_2y': std_df[date.strftime('%Y-%m-%d')]['stdDev2Y'],
            'std_3y': std_df[date.strftime('%Y-%m-%d')]['stdDev3Y'],
        }
        db.daily_data.insert(entry)

    # update track_date
    db.track_date.update({'date': {'$gt': ''}}, {'$set': {'date': date.strftime('%Y-%m-%d')}})


def save_monthly(db, df):
    dates = df.columns
    for date in dates:
        # if date exist in monthly_data, then continue
        count = db.monthly_data.count_documents({"date": date.strftime('%Y-%m-%d')})
        if count > 0:
            continue
        entry = {
            'date': date.strftime('%Y-%m-%d'),
            'ppi_tongbi': df[date]['M0001227'],
            'ppi_huanbi': df[date]['M0049160'],
            'cpi_tongbi': df[date]['M0000612'],
            'cpi_huanbi': df[date]['M0000705'],
            'pmi': df[date]['M0017126'],
            'maoyichae_yimeiyuan': df[date]['M0000610']
        }
        db.monthly_data.insert(entry)


def main():
    run(db.mongo)


if __name__ == "__main__":
    main()
