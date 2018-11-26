from tasks import w
import datetime
import pandas as pd
from tasks import DataAPI


def build_df(o):
    df = pd.DataFrame(o.Data)
    if len(o.Times) == 1:
        df = df.T
    df.columns = o.Times
    df.index = o.Codes
    print(df)
    return df


def daily_task(start=None):
    '''
    国债收益率（1月，1年，10年）、3A企业债收益率1年
    M1004677 - 中债国债到期收益率1个月
    M1001646 - 国债到期收益率1年
    M1001654 - 国债到期收益率10年
    S0059771 - 中债企业债到期收益率1年
    S0035818 - 金价现货9995
    S0035819 - 金价现货9999
    S0035820 - 金价现货100g
    '''
    daily_result = w.wsd("M1004677,M1001646,M1001654,S0059771,S0035818,S0035819,S0035820", 'close', start)
    df = build_df(daily_result)
    yesterday = (datetime.datetime.strptime(start, '%Y-%m-%d') + + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    std_data = DataAPI.MktIdxPerformanceGet(SecID=u"",ticker=u"000001",beginDate=yesterday,endDate=u"",field=u"tradeDate,stdDev6M,stdDev1Y,stdDev2Y,stdDev3Y",pandas="1")
    std_data.index = std_data['tradeDate'].tolist()
    return df, std_data.T


def monthly_task(start=None):
    '''
    经济指标
    M0000610 - 贸易差额（亿美元）
    M0049160 - PPI环比
    M0001227 - PPI同比
    M0017126 - PMI
    M0000705 - CPI环比
    M0000612 - CPI同比
    '''
    monthly_result = w.wsd("M0000610,M0049160,M0001227,M0017126,M0000705,M0000612", 'close', start)
    return build_df(monthly_result)


if __name__ == "__main__":
    daily_task('2018-11-20')
