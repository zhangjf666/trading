# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/9/2 22:26
Desc: 同花顺-数据获取
"""
import os
import time
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer
from tqdm import tqdm
import demjson


def _get_js_path_ths(name: str = None, module_file: str = None) -> str:
    """
    获取 JS 文件的路径(从模块所在目录查找)
    :param name: 文件名
    :type name: str
    :param module_file: 模块路径
    :type module_file: str
    :return: 路径
    :rtype: str
    """
    module_folder = os.path.abspath(
        os.path.dirname(os.path.dirname(module_file)))
    module_json_path = os.path.join(module_folder, "api", name)
    return module_json_path


def _get_file_content_ths(file_name: str = "ase.min.js") -> str:
    """
    获取 JS 文件的内容
    :param file_name:  JS 文件名
    :type file_name: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_name = file_name
    setting_file_path = _get_js_path_ths(setting_file_name, __file__)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def _sleep(secend: int = 3):
    time.sleep(secend)


def stock_board_concept_name_ths() -> pd.DataFrame:
    """
    同花顺-板块-概念板块-概念
    http://q.10jqka.com.cn/gn/detail/code/301558/
    :return: 所有概念板块的名称和链接
    :rtype: pandas.DataFrame
    """
    url = "http://q.10jqka.com.cn/gn/index/field/addtime/order/desc/page/1/ajax/1/"
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call('v')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': f'v={v_code}'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    total_page = soup.find('span', attrs={'class': 'page_info'}).text.split('/')[1]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page)+1), leave=False):
        url = f"http://q.10jqka.com.cn/gn/index/field/addtime/order/desc/page/{page}/ajax/1/"
        js_code = py_mini_racer.MiniRacer()
        js_content = _get_file_content_ths("ths.js")
        js_code.eval(js_content)
        v_code = js_code.call('v')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': f'v={v_code}'
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        soup.find('table', attrs={'class': 'm-table m-pager-table'}).find('tbody')
        url_list = []
        for item in soup.find('table', attrs={'class': 'm-table m-pager-table'}).find('tbody').find_all('tr'):
            inner_url = item.find_all("td")[1].find('a')['href']
            url_list.append(inner_url)
        temp_df = pd.read_html(r.text)[0]
        temp_df['代码'] = url_list
        big_df = big_df.append(temp_df, ignore_index=True)
        _sleep()
    big_df = big_df[[
        '日期',
        '概念名称',
        '成分股数量',
        '代码'
    ]]
    big_df['日期'] = pd.to_datetime(big_df['日期']).dt.date
    big_df['成分股数量'] = pd.to_numeric(big_df['成分股数量'])
    return big_df


def stock_board_industry_name_ths() -> pd.DataFrame:
    """
    同花顺-板块-行业板块
    http://q.10jqka.com.cn/thshy/
    :return: 所有行业板块的名称和代码
    :rtype: pandas.DataFrame
    """
    url = "http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/1/ajax/1/"
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call('v')
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': f'v={v_code}'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    total_page = soup.find('span', attrs={
        'class': 'page_info'
    }).text.split('/')[1]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page) + 1), leave=False):
        url = f"http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/{page}/ajax/1/"
        js_code = py_mini_racer.MiniRacer()
        js_content = _get_file_content_ths("ths.js")
        js_code.eval(js_content)
        v_code = js_code.call('v')
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': f'v={v_code}'
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        soup.find('table', attrs={
            'class': 'm-table m-pager-table'
        }).find('tbody')
        url_list = []
        for item in soup.find('table',
                              attrs={
                                  'class': 'm-table m-pager-table'
                              }).find('tbody').find_all('tr'):
            inner_url = item.find_all("td")[1].find('a')['href']
            url_list.append(inner_url)
        temp_df = pd.read_html(r.text)[0]
        temp_df['url'] = url_list
        big_df = big_df.append(temp_df, ignore_index=True)
        _sleep()
    big_df = big_df[['板块', 'url']]
    big_df.rename(columns={'板块': '名称'}, inplace=True)
    big_df['代码'] = big_df['url'].map(lambda x: x.replace(
        'http://q.10jqka.com.cn/thshy/detail/code/', '')[0:-1])
    return big_df


def stock_board_concept_cons_ths(symbol: str = "301362") -> pd.DataFrame:
    """
    同花顺-板块-概念板块-成份股
    http://q.10jqka.com.cn/gn/detail/code/301558/
    :param symbol: 板块名称
    :type symbol: str
    :return: 成份股
    :rtype: pandas.DataFrame
    """
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call('v')
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': f'v={v_code}'
    }
    url = f'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/1/ajax/1/code/{symbol}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    try:
        page_num = int(
            soup.find_all('a', attrs={'class': 'changePage'})[-1]['page'])
    except IndexError as e:
        page_num = 1
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=False):
        v_code = js_code.call('v')
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': f'v={v_code}'
        }
        url = f'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{page}/ajax/1/code/{symbol}'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
        _sleep()
    big_df.rename(
        {
            "涨跌幅(%)": "涨跌幅",
            "涨速(%)": "涨速",
            "换手(%)": "换手",
            "振幅(%)": "振幅",
        },
        inplace=True,
        axis=1)
    del big_df['加自选']
    big_df['代码'] = big_df['代码'].astype(str).str.zfill(6)
    return big_df


def stock_board_concept_index_ths(symbol: str = None,
                                  start_year: str = None,
                                  end_year: str = None) -> pd.DataFrame:
    """
    同花顺-板块-概念板块-指数数据
    http://q.10jqka.com.cn/gn/detail/code/301558/
    :param start_year: 开始年份; e.g., 2019
    :type start_year: str
    :param symbol: 板块简介
    :type symbol: str
    :return: 板块简介
    :rtype: pandas.DataFrame
    """
    symbol_url = f'http://q.10jqka.com.cn/gn/detail/code/{symbol}/'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }
    r = requests.get(symbol_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    symbol_code = soup.find('div', attrs={
        'class': 'board-hq'
    }).find('span').text
    big_df = stock_board_industry_index_ths(symbol_code, start_year, end_year)
    return big_df


def stock_board_industry_index_ths(symbol: str = None,
                                   start_year: str = None,
                                   end_year: str = None) -> pd.DataFrame:
    """
    同花顺-板块-行业板块-指数数据
    http://q.10jqka.com.cn/gn/detail/code/301558/
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :param symbol: 指数数据
    :type symbol: str
    :return: 指数数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    for year in tqdm(range(int(start_year), int(end_year) + 1), leave=False):
        url = f'http://d.10jqka.com.cn/v4/line/bk_{symbol}/01/{year}.js'
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Referer': 'http://q.10jqka.com.cn',
            'Host': 'd.10jqka.com.cn'
        }
        r = requests.get(url, headers=headers)
        data_text = r.text
        try:
            demjson.decode(data_text[data_text.find('{'):-1])
        except:
            _sleep()
            continue
        temp_df = demjson.decode(data_text[data_text.find('{'):-1])
        temp_df = pd.DataFrame(temp_df['data'].split(';'))
        temp_df = temp_df.iloc[:, 0].str.split(',', expand=True)
        big_df = big_df.append(temp_df, ignore_index=True)
        _sleep()
    columns = ['日期', '开盘价', '最高价', '最低价', '收盘价', '成交量', '成交额']
    if(big_df.shape[1] >= 7):
        big_df = big_df.iloc[:, 0:7]
        big_df.columns = columns
    else:
        big_df = pd.DataFrame(columns=columns)
    big_df['日期'] = pd.to_datetime(big_df['日期']).dt.date
    big_df['开盘价'] = pd.to_numeric(big_df['开盘价'])
    big_df['最高价'] = pd.to_numeric(big_df['最高价'])
    big_df['最低价'] = pd.to_numeric(big_df['最低价'])
    big_df['收盘价'] = pd.to_numeric(big_df['收盘价'])
    big_df['成交量'] = pd.to_numeric(big_df['成交量'])
    big_df['成交额'] = pd.to_numeric(big_df['成交额'])
    return big_df


def stock_board_cons_ths(symbol: str = "885611") -> pd.DataFrame:
    """
    行业板块或者概念板块的成份股
    http://q.10jqka.com.cn/thshy/detail/code/881121/
    http://q.10jqka.com.cn/gn/detail/code/301558/
    :param symbol: 行业板块或者概念板块的代码
    :type symbol: str
    :return: 行业板块或者概念板块的成份股
    :rtype: pandas.DataFrame
    """
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call('v')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': f'v={v_code}'
    }
    url = f'http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/1/ajax/1/code/{symbol}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    try:
        page_num = int(soup.find_all('a', attrs={'class': 'changePage'})[-1]['page'])
    except IndexError as e:
        page_num = 1
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1), leave=False):
        v_code = js_code.call('v')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': f'v={v_code}'
        }
        url = f'http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/{page}/ajax/1/code/{symbol}'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
        _sleep()
    big_df.rename({"涨跌幅(%)": "涨跌幅",
                   "涨速(%)": "涨速",
                   "换手(%)": "换手",
                   "振幅(%)": "振幅",
                   }, inplace=True, axis=1)
    del big_df['加自选']
    big_df['代码'] = big_df['代码'].astype(str).str.zfill(6)
    return big_df
