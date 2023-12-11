import streamlit as st
#設定密碼
passwords_and_names = {
    "8311": "啟宏",
    "8497": "禮澤",
    "8661": "Gem林芝",
    "8927": "Amber虹儀",
    "8968": "Maggie玫君",
    "6045": "Grace芷瑄",
    "6197": "Ersha湘婷",
    "6230": "Iris沛晴",
    "8997": "Sinyi昕怡",
    "8156": "Wanju婉汝",
    "8837": "Grace洺瑱"
}
#標題 
st.title("權利金銷售情況")
# 在首頁輸入密碼
user_input = st.text_input("請輸入密碼:", type="password")

if user_input:    
    # 驗證密碼
    if user_input in passwords_and_names:
        # 獲取對應的名字
        user_name = passwords_and_names[user_input]
        st.success(f"Hi~{user_name}！密碼正確，已解鎖應用程序！")
        # 在這裡放置您的應用程序主要內容
        #前端介面輸入框
        '''僅第一次載入大量數據需要數秒，之後查詢會很快^^'''
        '''> STEP.1 匯入檔案(資安考量，從你電腦匯入檔案較安全喔) ↓ '''
        uploaded_file = st.file_uploader("上傳Excel文件", type=["xlsx"])
        
        if uploaded_file:
            '''> STEP.2 匯入檔案後，輸入條件查詢'''
            NUMBERorISBN = st.text_input("用合約詳編/ISBN查詢")
            NUMBERorISBN = NUMBERorISBN.upper()
        
            '''> STEP.3 自動分析~BOOM!!'''
        
            import pandas as pd
            sheet_name = "2014Q1-今【銷售明細_書籍】ALL項目"  #@指定分頁
        
            @st.cache_data(ttl=3600)  # 設定生存時間 (TTL) 為 3600 秒 (1 小時)
            def long_running_function(file_path):
                data = pd.read_excel(file_path,
                                     sheet_name=sheet_name,         #@指定分頁
                                     usecols=[0,1,2,3,5,7,9,10,11,12,13,14,15,16,20,21,22,23,24,37],  #@指定欄位
                                     # nrows=10,                      #@指定列數
                                     header = 0,                      #header = ?  >> 指定第?列為header(index)
                                     engine='openpyxl')
                return data
        
            # Call the function with the uploaded file
            data = long_running_function(uploaded_file)

            # -------------------------------------------▲ 資料處理完成，以下開始篩選 ▼-------------------------------------------------------
            #拆份季節&年分
            data[["年", "季"]] = data["季"].str.split("Q", expand=True)
            #篩選條件
            Filter_contract_number = data["合約詳編"] == NUMBERorISBN
            Filter_isbn = data["ISBN"] == NUMBERorISBN
            result = data[Filter_contract_number | Filter_isbn]
            
            '''# 以下是篩選後的權利金情形(可供下載)'''
            result.index = range(1,len(result)+1)
            st.dataframe(result)
            # ------------------------------------------- 重要資訊統計 ▼-------------------------------------------------------
            '''# 以下是銷售情況統計'''
            total = f"一、{NUMBERorISBN}採購案數共:" + str(len(result)) + "(非title數)"
            total 
            total_money = f"二、{NUMBERorISBN}單位歷年電子書內容收益總額:" + str(result["電子書內容收益"].sum() ) + "(新台幣)"
            total_money        
            pd_income_peryear = result.groupby(by=['年'])['電子書內容收益'].sum().reset_index()
            pd_income_peryear.index = range(1,len(pd_income_peryear)+1)
            pd_income_peryear
            # ------------------------------------------- 開始繪圖 ▼-------------------------------------------------------
            # --------------- 繪圖 ▼ 歷年收益(長條圖)-------------
            import plotly.express as px
            import pandas as pd
            fig = px.bar(pd_income_peryear, x='年', y='電子書內容收益', title='【歷年】電子書內容收益')
            # 調整 x 軸刻度為整數
            fig.update_xaxes(type='category')  # 將 x 軸型別設為類別型
            fig.update_xaxes(tickmode='linear')  # 使用線性刻度
            fig.update_xaxes(tick0=0)  # 刻度的起始點
            fig.update_xaxes(dtick=1)  # 刻度的間距

            # 在 Streamlit 中显示 Plotly 图表
            st.plotly_chart(fig)
            # --------------- 繪圖 ▼ 銷售市場-地區(pie圖)-------------
            # 按銷售地區分组并计算權利金总和
            x = result.groupby(by=['銷售地區'])['電子書內容收益'].sum().reset_index()
            fig = px.pie(x, values='電子書內容收益', names='銷售地區', title='【銷售市場】-地區佔比', 
                         hover_data=['電子書內容收益'],
                         )
            fig.update_layout(height=500, width=700)
            st.plotly_chart(fig)
            # --------------- 繪圖 ▼ 銷售客源(長條圖)-------------
            import plotly.express as px
            import pandas as pd
            x = result.groupby(by=['銷售單位'])['電子書內容收益'].sum().reset_index().sort_values(by='電子書內容收益', ascending=False).head(5)
            fig = px.bar(x, x='銷售單位', y='電子書內容收益', title='【銷售單位】排名前五')
            # 在 Streamlit 中显示 Plotly 图表
            st.plotly_chart(fig)

        else:
            st.warning("請上傳 Excel 文件。")
    else:
        st.warning("密碼錯誤。")
else:
    st.warning("尚未輸入密碼。")
