import trading.collector.stock_history as cl

stock_code = "sh.600519"
cl.query_history_k_data(
    stock_code,
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    "2018-01-01", "2019-06-30")
