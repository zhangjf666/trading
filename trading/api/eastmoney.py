# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/9/2 22:26
Desc: 东方财富网-数据获取
"""
import requests
import pandas as pd
import demjson
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# 设置重试次数
requests.adapters.DEFAULT_RETRIES = 3


def _sleep(secend: int = 1):
    time.sleep(secend)


def stock_zh_a_spot_em() -> pd.DataFrame:
    """
    东方财富-A股-实时行情
    http://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "http://35.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df.columns = ["_",
                       "最新价",
                       "涨跌幅",
                       "涨跌额",
                       "成交量",
                       "成交额",
                       "振幅",
                       "换手率",
                       "市盈率-动态",
                       "量比",
                       "_",
                       "代码",
                       "_",
                       "名称",
                       "最高",
                       "最低",
                       "今开",
                       "昨收",
                       "总市值",
                       "流通市值",
                       "_",
                       "市净率",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       ]
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.rename(columns={'index': "序号"}, inplace=True)
    temp_df = temp_df[[
        "序号",
        "代码",
        "名称",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "最高",
        "最低",
        "今开",
        "昨收",
        "量比",
        "换手率",
        "总市值",
        "流通市值",
        "市盈率-动态",
        "市净率",
    ]]
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors='coerce')
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors='coerce')
    temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'], errors='coerce')
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'], errors='coerce')
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'], errors='coerce')
    temp_df['振幅'] = pd.to_numeric(temp_df['振幅'], errors='coerce')
    temp_df['最高'] = pd.to_numeric(temp_df['最高'], errors='coerce')
    temp_df['最低'] = pd.to_numeric(temp_df['最低'], errors='coerce')
    temp_df['今开'] = pd.to_numeric(temp_df['今开'], errors='coerce')
    temp_df['昨收'] = pd.to_numeric(temp_df['昨收'], errors='coerce')
    temp_df['量比'] = pd.to_numeric(temp_df['量比'], errors='coerce')
    temp_df['换手率'] = pd.to_numeric(temp_df['换手率'], errors='coerce')
    temp_df['总市值'] = pd.to_numeric(temp_df['总市值'], errors='coerce')
    temp_df['流通市值'] = pd.to_numeric(temp_df['流通市值'], errors='coerce')
    temp_df['市盈率-动态'] = pd.to_numeric(temp_df['市盈率-动态'], errors='coerce')
    temp_df['市净率'] = pd.to_numeric(temp_df['市净率'], errors='coerce')
    return temp_df


def bond_cov_comparison() -> pd.DataFrame:
    """
    东方财富网-行情中心-债券市场-可转债比价表
    http://quote.eastmoney.com/center/fullscreenlist.html#convertible_comparison
    :return: 可转债比价表数据
    :rtype: pandas.DataFrame
    """
    url = "http://16.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f243",
        "fs": "b:MK0354",
        "fields": "f1,f152,f2,f3,f12,f13,f14,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f26,f243",
        "_": "1590386857527",
    }
    r = requests.get(url, params=params)
    text_data = r.text
    json_data = demjson.decode(text_data)
    temp_df = pd.DataFrame(json_data["data"]["diff"])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        "序号",
        "_",
        "转债最新价",
        "转债涨跌幅",
        "转债代码",
        "_",
        "转债名称",
        "上市日期",
        "_",
        "纯债价值",
        "_",
        "正股最新价",
        "正股涨跌幅",
        "_",
        "正股代码",
        "_",
        "正股名称",
        "转股价",
        "转股价值",
        "转股溢价率",
        "纯债溢价率",
        "回售触发价",
        "强赎触发价",
        "到期赎回价",
        "开始转股日",
        "申购日期",
    ]
    temp_df = temp_df[
        [
            "序号",
            "转债代码",
            "转债名称",
            "转债最新价",
            "转债涨跌幅",
            "正股代码",
            "正股名称",
            "正股最新价",
            "正股涨跌幅",
            "转股价",
            "转股价值",
            "转股溢价率",
            "纯债溢价率",
            "回售触发价",
            "强赎触发价",
            "到期赎回价",
            "纯债价值",
            "开始转股日",
            "上市日期",
            "申购日期",
        ]
    ]
    return temp_df


def stock_em_jgdy_tj(start_date: str = "2021-01-01") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研统计
    http://data.eastmoney.com/jgdy/tj.html
    :param start_date: 开始时间
    :type start_date: str
    :return: 机构调研统计
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'sortColumns': 'RECEIVE_START_DATE,SUM,NOTICE_DATE,SECURITY_CODE',
        'sortTypes': '1,-1,-1,1',
        'pageSize': '500',
        'pageNumber': '1',
        'reportName': 'RPT_ORG_SURVEYNEW',
        'columns': 'ALL',
        'quoteColumns': 'f2~01~SECURITY_CODE~CLOSE_PRICE,f3~01~SECURITY_CODE~CHANGE_RATE',
        'source': 'WEB',
        'client': 'WEB',
        'filter': f"""(NUMBERNEW="1")(IS_SOURCE="1")(RECEIVE_START_DATE>'{start_date}')"""
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json['result']['pages']
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page+1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json['result']['data'])
        big_df = big_df.append(temp_df)
    big_df.reset_index(inplace=True)
    big_df["index"] = list(range(1, len(big_df) + 1))
    big_df.columns = [
        "序号",
        "_",
        "代码",
        "名称",
        "_",
        "公告日期",
        "接待日期",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "接待地点",
        "_",
        "接待方式",
        "_",
        "接待人员",
        "_",
        "_",
        "_",
        "_",
        "_",
        "接待机构数量",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "涨跌幅",
        "最新价",
    ]
    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "接待机构数量",
            "接待方式",
            "接待人员",
            "接待地点",
            "接待日期",
            "公告日期",
        ]
    ]
    big_df['最新价'] = pd.to_numeric(big_df['最新价'], errors="coerce")
    big_df['涨跌幅'] = pd.to_numeric(big_df['涨跌幅'], errors="coerce")
    big_df['接待机构数量'] = pd.to_numeric(big_df['接待机构数量'], errors="coerce")
    big_df['接待日期'] = pd.to_datetime(big_df['接待日期']).dt.date
    big_df['公告日期'] = pd.to_datetime(big_df['公告日期']).dt.date
    return big_df


def stock_em_ggyb(start_date: str = "2022-01-01", end_date: str = "2052-12-31") -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-个股研报
    https://data.eastmoney.com/report/stock.jshtml
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 个股研报
    :rtype: pandas.DataFrame
    """
    url = "https://reportapi.eastmoney.com/report/list"
    params = {
        'cb': 'datatable7502912',
        'industryCode': '*',
        'pageSize': '50',
        'industry': '*',
        'rating': '',
        'ratingChange': '',
        'beginTime': start_date,
        'endTime': end_date,
        'pageNo': 1,
        'fields': '',
        'qType': 0,
        'orgCode': '',
        'code': '*',
        'rcode': '',
        'p': 1,
        'pageNum': 1,
        'pageNumber': 1,
        '_': 1642943357737
    }
    r = requests.get(url, params=params)
    data_text = r.text
    try:
        demjson.decode(data_text[data_text.find('{'):-1])
    except BaseException:
        return
    temp_df = demjson.decode(data_text[data_text.find('{'):-1])
    total_page = temp_df['TotalPage']
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page+1), leave=False):
        params.update({"pageNo": page, "pageNumber": page, "p": page, "pageNum": page, "pageNumber": page})
        r = requests.get(url, params=params)
        data_text = r.text
        try:
            demjson.decode(data_text[data_text.find('{'):-1])
        except BaseException:
            continue
        temp_df = demjson.decode(data_text[data_text.find('{'):-1])
        temp_df = pd.DataFrame(temp_df['data'])
        summary_list = []
        download_list = []
        source_list = []
        for index in temp_df.index:
            row = temp_df.iloc[index, :]
            encode_url = getattr(row, 'encodeUrl')
            source_url = "https://data.eastmoney.com/report/zw_macresearch.jshtml?encodeUrl=" + encode_url
            r = requests.get(source_url)
            soup = BeautifulSoup(r.text, "lxml")
            summary = soup.find('div', attrs={'class': 'ctx-content'}).text
            summary_list.append(summary)
            download_url = soup.find('a', attrs={'class': 'pdf-link'})['href']
            download_list.append(download_url)
            source_list.append(source_url)
        temp_df['summary'] = summary_list
        temp_df['downloadUrl'] = download_list
        temp_df['sourceUrl'] = source_list
        big_df = big_df.append(temp_df)
        _sleep()
    big_df = big_df[
        [
            'encodeUrl',
            'title',
            'attachPages',
            'count',
            'emRatingName',
            'stockName',
            'stockCode',
            'orgCode',
            'orgName',
            'orgSName',
            'publishDate',
            'predictThisYearEps',
            'predictThisYearPe',
            'predictNextYearEps',
            'predictNextYearPe',
            'predictNextTwoYearEps',
            'predictNextTwoYearPe',
            'industryCode',
            'industryName',
            'indvInduCode',
            'indvInduName',
            'researcher',
            'sRatingName',
            'summary',
            'sourceUrl',
            'downloadUrl',
            'market'
        ]
    ]
    return big_df


def stock_em_hyyb(start_date: str = "2022-01-01", end_date: str = "2052-12-31") -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-行业研报
    https://data.eastmoney.com/report/industry.jshtml
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 行业研报
    :rtype: pandas.DataFrame
    """
    url = "https://reportapi.eastmoney.com/report/list"
    params = {
        'cb': 'datatable6339771',
        'industryCode': '*',
        'pageSize': '50',
        'industry': '*',
        'rating': '*',
        'ratingChange': '*',
        'beginTime': start_date,
        'endTime': end_date,
        'pageNo': 1,
        'fields': '',
        'qType': 1,
        'orgCode': '',
        'code': '',
        'rcode': '',
        'p': 1,
        'pageNum': 1,
        'pageNumber': 1,
        '_': 1643025359466
    }
    r = requests.get(url, params=params)
    data_text = r.text
    try:
        demjson.decode(data_text[data_text.find('{'):-1])
    except BaseException:
        return
    temp_df = demjson.decode(data_text[data_text.find('{'):-1])
    total_page = temp_df['TotalPage']
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page+1), leave=False):
        params.update({"pageNo": page, "pageNumber": page, "p": page, "pageNum": page, "pageNumber": page})
        r = requests.get(url, params=params)
        data_text = r.text
        try:
            demjson.decode(data_text[data_text.find('{'):-1])
        except BaseException:
            continue
        temp_df = demjson.decode(data_text[data_text.find('{'):-1])
        temp_df = pd.DataFrame(temp_df['data'])
        summary_list = []
        download_list = []
        source_list = []
        for index in temp_df.index:
            row = temp_df.iloc[index, :]
            encode_url = getattr(row, 'encodeUrl')
            source_url = "https://data.eastmoney.com/report/zw_macresearch.jshtml?encodeUrl=" + encode_url
            r = requests.get(source_url)
            soup = BeautifulSoup(r.text, "lxml")
            summary = soup.find('div', attrs={'class': 'ctx-content'}).text
            summary_list.append(summary)
            download_url = soup.find('a', attrs={'class': 'pdf-link'})['href']
            download_list.append(download_url)
            source_list.append(source_url)
        temp_df['summary'] = summary_list
        temp_df['downloadUrl'] = download_list
        temp_df['sourceUrl'] = source_list
        big_df = big_df.append(temp_df)
        _sleep()
    big_df = big_df[
        [
            'encodeUrl',
            'title',
            'attachPages',
            'count',
            'emRatingName',
            'stockName',
            'stockCode',
            'orgCode',
            'orgName',
            'orgSName',
            'publishDate',
            'predictThisYearEps',
            'predictThisYearPe',
            'predictNextYearEps',
            'predictNextYearPe',
            'predictNextTwoYearEps',
            'predictNextTwoYearPe',
            'industryCode',
            'industryName',
            'indvInduCode',
            'indvInduName',
            'researcher',
            'sRatingName',
            'summary',
            'sourceUrl',
            'downloadUrl',
            'market'
        ]
    ]
    return big_df


def stock_em_clyb(start_date: str = "2022-01-01", end_date: str = "2052-12-31") -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-策略研报
    https://data.eastmoney.com/report/strategyreport.jshtml
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 策略研报
    :rtype: pandas.DataFrame
    """
    url = "https://reportapi.eastmoney.com/report/jg"
    params = {
        'cb': 'datatable6052118',
        'pageSize': '50',
        'beginTime': start_date,
        'endTime': end_date,
        'pageNo': 1,
        'fields': '',
        'qType': 2,
        'orgCode': '',
        'author': '',
        'rcode': '',
        'p': 1,
        'pageNum': 1,
        'pageNumber': 1,
        '_': 1643025620100
    }
    r = requests.get(url, params=params)
    data_text = r.text
    try:
        demjson.decode(data_text[data_text.find('{'):-1])
    except BaseException:
        return
    temp_df = demjson.decode(data_text[data_text.find('{'):-1])
    total_page = temp_df['TotalPage']
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page+1), leave=False):
        params.update({"pageNo": page, "pageNumber": page, "p": page, "pageNum": page, "pageNumber": page})
        r = requests.get(url, params=params)
        data_text = r.text
        try:
            demjson.decode(data_text[data_text.find('{'):-1])
        except BaseException:
            continue
        temp_df = demjson.decode(data_text[data_text.find('{'):-1])
        temp_df = pd.DataFrame(temp_df['data'])
        summary_list = []
        download_list = []
        source_list = []
        for index in temp_df.index:
            row = temp_df.iloc[index, :]
            encode_url = getattr(row, 'encodeUrl')
            source_url = "https://data.eastmoney.com/report/zw_macresearch.jshtml?encodeUrl=" + encode_url
            r = requests.get(source_url)
            soup = BeautifulSoup(r.text, "lxml")
            summary = soup.find('div', attrs={'class': 'ctx-content'}).text
            summary_list.append(summary)
            download_url = soup.find('a', attrs={'class': 'pdf-link'})['href']
            download_list.append(download_url)
            source_list.append(source_url)
        temp_df['summary'] = summary_list
        temp_df['downloadUrl'] = download_list
        temp_df['sourceUrl'] = source_list
        big_df = big_df.append(temp_df)
        _sleep()
    big_df = big_df[
        [
            'encodeUrl',
            'title',
            'count',
            'orgCode',
            'orgName',
            'orgSName',
            'publishDate',
            'industryCode',
            'industryName',
            'researcher',
            'summary',
            'sourceUrl',
            'downloadUrl',
            'market'
        ]
    ]
    return big_df


def stock_em_hgyb(start_date: str = "2022-01-01", end_date: str = "2052-12-31") -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-宏观研报
    https://data.eastmoney.com/report/macresearch.jshtml
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 宏观研报
    :rtype: pandas.DataFrame
    """
    url = "https://reportapi.eastmoney.com/report/jg"
    params = {
        'cb': 'datatable4839298',
        'pageSize': '50',
        'beginTime': start_date,
        'endTime': end_date,
        'pageNo': 1,
        'fields': '',
        'qType': 3,
        'orgCode': '',
        'author': '',
        'rcode': '',
        'p': 1,
        'pageNum': 1,
        'pageNumber': 1,
        '_': 1643025810644
    }
    r = requests.get(url, params=params)
    data_text = r.text
    try:
        demjson.decode(data_text[data_text.find('{'):-1])
    except BaseException:
        return
    temp_df = demjson.decode(data_text[data_text.find('{'):-1])
    total_page = temp_df['TotalPage']
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page+1), leave=False):
        params.update({"pageNo": page, "pageNumber": page, "p": page, "pageNum": page, "pageNumber": page})
        r = requests.get(url, params=params)
        data_text = r.text
        try:
            demjson.decode(data_text[data_text.find('{'):-1])
        except BaseException:
            continue
        temp_df = demjson.decode(data_text[data_text.find('{'):-1])
        temp_df = pd.DataFrame(temp_df['data'])
        summary_list = []
        download_list = []
        source_list = []
        for index in temp_df.index:
            row = temp_df.iloc[index, :]
            encode_url = getattr(row, 'encodeUrl')
            source_url = "https://data.eastmoney.com/report/zw_macresearch.jshtml?encodeUrl=" + encode_url
            r = requests.get(source_url)
            soup = BeautifulSoup(r.text, "lxml")
            summary = soup.find('div', attrs={'class': 'ctx-content'}).text
            summary_list.append(summary)
            download_url = soup.find('a', attrs={'class': 'pdf-link'})['href']
            download_list.append(download_url)
            source_list.append(source_url)
        temp_df['summary'] = summary_list
        temp_df['downloadUrl'] = download_list
        temp_df['sourceUrl'] = source_list
        big_df = big_df.append(temp_df)
        _sleep()
    big_df = big_df[
        [
            'encodeUrl',
            'title',
            'count',
            'orgCode',
            'orgName',
            'orgSName',
            'publishDate',
            'industryCode',
            'industryName',
            'researcher',
            'summary',
            'sourceUrl',
            'downloadUrl',
            'market'
        ]
    ]
    return big_df


if __name__ == "__main__":
    df = stock_em_hgyb(start_date="2022-01-24", end_date="2022-01-24")
    print(df)
