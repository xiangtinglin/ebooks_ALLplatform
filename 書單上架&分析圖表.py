import pipes
import streamlit as st
#前端介面輸入框
st.title("書單上架情況(已授權&建檔)")
'''僅第一次載入大量數據需要數秒，之後查詢會很快^^'''
'''> STEP.1 匯入檔案(資安考量，從你電腦匯入檔案較安全喔)'''
uploaded_file = st.file_uploader("上傳Excel文件", type=["xlsx"])

path = st.text_input('*請輸入你檔案的完整路徑')
# 確保檔案路徑格式正確
path = path.replace("\\", "\\\\")  # 將單一反斜線替換為雙反斜線
path = path.replace('"', '')
path = path.strip()  # 移除前後的空白

'''> STEP.2 匯入檔案後，輸入條件查詢'''
contract_number = st.text_input('用合約詳編查詢')
contract_number = contract_number.upper()
isbn = st.text_input('或用ISBN查詢')

'''> STEP.3 自動分析~BOOM!!'''

import pandas as pd
sheet_name = "總經銷書單"
# file_path = r"C:\Users\A11197\Desktop\WORK\資料處理jupyter\.streamlit\原資料檔案\(NEW)總經銷書單.xlsx"

@st.cache_data(ttl=3600)  # 設定生存時間 (TTL) 為 3600 秒 (1 小時)
def long_running_function():
  data = pd.read_excel(uploaded_file,
                     sheet_name = sheet_name,         #@指定分頁
                     usecols=[0,2,3,8,17,19,23,25,29,31,36,38,42,44,48,50,54,56,60,62,66,68,72,74,78,80,84,86,90,92,96,98],  #@指定欄位
                     # nrows=10,                      #@指定列數
                     # header = 3,                      #header = ?  >> 指定第?列為header(index)
                     )
  return data
#將讀取資料的方式變成function
#再利用st.cache()將資料放進快取內
data = long_running_function()

# 指定要查找和替换的内容
replacement_dict = {
    "R": "已提報",
    "W": "近期準備提報",
    "O": "O已上架",
    "P": "無法提報、下架",
    "P1": "此電子書已無授權",
    "P2": "不符平台提報規格",
    "P3": "重複上架(版權衝突)",
    "P4": "問題件"
    # 添加更多的查找和替换项
}
# 使用pandas的replace函数进行替换
data.replace(replacement_dict, inplace=True) 

# -------------------------------------------▲ 資料處理完成，以下開始篩選 ▼-------------------------------------------------------

#篩選條件
Filter_contract_number = data["合約編號"] == contract_number
Filter_isbn = data["ISBN"] == isbn
result = data[Filter_contract_number | Filter_isbn]
# ------------------------------------------- 重要資訊統計 ▼-------------------------------------------------------
'''*以下是書單上架情況統計'''
total = "總共建檔數:" + str(len(result))
total 
'''*以下是上進度架情況表(可供下載)'''
result.index = range(1,len(result)+1)
st.dataframe(result)
# #匯出檔案
# result.to_excel(r"C:\Users\User'''\.streamlit\輸出檔案\金尉.xlsx")  

# ------------------------------------------- 開始繪圖 ▼-------------------------------------------------------

'''**開始繪圖(請耐心等候....但其實很快^^ XD)'''
#繪圖_顯示特殊字形
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# Solve the issue with displaying Chinese characters
plt.rcParams['axes.unicode_minus'] = False

# #新增欄位
# result.insert(0, column="佔比", value=1)
# result = result.groupby(by=['書名']).apply(lambda x:x[x.columns]).plot(
#     kind='pie', y="佔比")

# plt.title('【統計至2023.11】',color='r',size=18)
# plt.xlabel("(分類依據：)",color='gray',size=10)
# plt.ylabel("佔比(%)",color='blue')
# plt.legend(loc='lower right')
# plt.show()
## 導入套件

import plotly.graph_objs as go
from plotly.subplots import make_subplots

## 構建一個2X2的大圖
fig = make_subplots(rows = 2, cols = 2)

## 構建子圖
## 子圖1
fig.add_trace(
  go.Scatter(x = [8, 2, 6, 10, 14, 18], y = [18, 14, 12, 20, 24, 28], mode = 'markers', name = 'Scatter'),
  row = 1,
  col = 1
)

## 子圖2
fig.add_trace(
  go.Scatter(x = [8, 2, 6, 10, 14, 18], y = [18, 14, 12, 20, 24, 28], mode = 'lines', name = 'Lines'),
  row = 1,
  col = 2
)

## 子圖3
fig.add_trace(
  go.Bar(x = [8, 2, 6, 10, 14, 18], y = [18, 14, 12, 20, 24, 28], name = 'Bar'),
  row = 2,
  col = 1
)

## 子圖1
fig.add_trace(
  go.Histogram(x = [8, 2, 6, 10, 14, 18], y = [18, 14, 12, 20, 24, 28], name = 'Histogram'),
  row = 2,
  col = 2
)

## 顯示圖片
# fig.show() #會額外跳出視窗

#streamlit頁面顯示分析圖
st.plotly_chart(fig)

from streamlit_echarts import st_echarts
 
# 定义ECharts的配置
option = {
    "title": {"text": "ECharts示例"},
    "tooltip": {},
    "xAxis": {
        "data": ["平台1", "平台2", "平台3", "平台4", "平台5", "平台6"]
    },
    "yAxis": {},
    "series": [
        {
            "name": "销量",
            "type": "bar",
            "data": [5, 20, 36, 10, 10, 20]
        }
    ]
}

# 在Streamlit应用中展示ECharts图表
st_echarts(options=option)