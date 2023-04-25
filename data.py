# %%
import tushare as ts
import pandas as pd
# 设置 Tushare 的 API Token
token = "c576df5b626df4f37c30bae84520d70c7945a394d7ee274ef2685444"
ts.set_token(token)

# %%
# 定义股票代码列表
tickers = ['000009.SZ', '000012.SZ', '000021.SZ','000027.SZ','000031.SZ']

# %%
# 生成日期序列
start_date = '2014-12-31'
end_date = '2022-12-30'
date_index = pd.date_range(start=start_date, end=end_date, freq='B')
prices = pd.DataFrame(index=date_index)
market_prices = pd.DataFrame(index=date_index)

# %%
for ticker in tickers:
    df = ts.pro_bar(ts_code=ticker, adj='qfq', start_date=start_date, end_date=end_date)
    df = df.set_index(pd.to_datetime(df['trade_date']))
    prices = prices.join(df.close).rename(columns = {'close':ticker})

# %%
prices = prices.dropna()

# %%
import tushare as ts
result = ts.get_zz500s()
result

# %%
import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login()
rs = bs.query_history_k_data_plus("sz.000905",
    "date,code,open,high,low,close,preclose,volume,amount,pctChg",
    start_date='2014-12-31', end_date='2022-12-30', frequency="d")
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

# %%
result = result.set_index(pd.to_datetime(result['date']))
market_prices = market_prices.join(result.close).rename(columns = {'close':'csi500'})

# %%
market_prices = market_prices.dropna()

# %%
pro = ts.pro_api()

# %%
mcaps = {}
for ticker in tickers:
    df = pro.bak_daily(ts_code=ticker,start_date=start_date, end_date=end_date,fields='trade_date,ts_code,name,total_mv')
    mcaps[ticker] = df.iloc[-1,3]
