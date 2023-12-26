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
        success_message = st.success(f"Hi~{user_name}！密碼正確，已解鎖應用程序！")
        import time
        time.sleep(0.9)
        success_message.empty()
# ------------------------------------------- 在這裡放置您的應用程序主要內容 ▼-------------------------------------------------------
        # ------------------ ▼【功能】第一區 ｜STEP.1 _匯入檔案 ▼------------------------
        st.markdown('<span style="color:red; font-weight:bold; font-size:22px;"> ｜STEP.1 _匯入檔案(目前檔案無資料庫化，因此需從你電腦匯入檔案) ↓</span>', unsafe_allow_html=True)
        
        with st.expander( "請上傳Excel文件:【權利金】歷年總表紀錄 "):
            uploaded_file = st.file_uploader("p.s.第一次載入大量數據需要數秒，之後查詢會很快^^，匯入後檔案預設存效4小時", type=["xlsx"])
            # ------------------ 暫存函式 ▼------------------------
            import pandas as pd
            sheet_name = "2014Q1-今【銷售明細_書籍】ALL項目"  #@指定分頁
        
            @st.cache_data(ttl=3600*4)  # 設定生存時間 (TTL) 為 3600*4 秒 (4 小時)
            def fist_loading(file_path):
                data = pd.read_excel(file_path,
                                     sheet_name=sheet_name,         #@指定分頁
                                     usecols=[0,1,2,3,5,7,9,10,11,12,13,14,15,16,20,21,22,23,24,37],  #@指定欄位
                                     # nrows=10,                      #@指定列數
                                     header = 0,                      #header = ?  >> 指定第?列為header(index)
                                     engine='openpyxl')
                return data
            # Call the function with the uploaded file
        if uploaded_file:
            data = fist_loading(uploaded_file)
            # ------------------ 原始資料加工 ▼------------------------
            #拆份季節&年分
            data[["年", "季"]] = data["季"].str.split("Q", expand=True)
            # ------------------ ▼【功能】第2區 ｜STEP.2 _電子書收益總覽 ↓  ▼------------------------
            st.markdown('<span style="color:red; font-weight:bold; font-size:22px;"> ｜ STEP.2 _電子書收益總覽 ↓</span>', unsafe_allow_html=True)
            with st.expander("請選擇條件"):
                view_option = st.selectbox("相同合約簡編旗下的品牌合併計算", ["歷年加總", "近3年"])
    
                # Display selected view
                if view_option == "歷年加總":
                    
                    # 將相同的合約簡編分為同類，後加總收益
                    total_rank = data.groupby(["合約簡編", "單位名稱"]).agg({'電子書內容收益': 'sum'}).reset_index()
                    # 列出的欄位
                    total_rank = total_rank.groupby("合約簡編").agg({
                         '單位名稱': lambda x: ','.join(x),  
                        '電子書內容收益': 'sum'
                    }).reset_index().sort_values(by='電子書內容收益', ascending=False)
                    # 重新排序欄位順序
                    total_rank = total_rank[['合約簡編', '單位名稱', '電子書內容收益']]
                    total_rank
                    total_rank.index = range(1, len(total_rank) + 1)
                    st.dataframe(total_rank)
            
                elif view_option == "近3年":
                    # Assuming '年' is the column representing years
                    recent_3years_data = data[data['年'].isin(data['年'].unique()[-3:])]
                    recent_3years_rank = recent_3years_data.groupby(by=['合約簡編'])['電子書內容收益'].sum().reset_index().sort_values(
                        by='電子書內容收益', ascending=False)
                    recent_3years_rank.index = range(1, len(recent_3years_rank) + 1)
                    st.dataframe(recent_3years_rank)  
            # ------------------------------------- 【功能】第3區_STEP.3 匯入檔案後，輸入條件查詢 ▼-------------------------                    
            st.markdown('<span style="color:red; font-weight:bold; font-size:22px;"> ｜ STEP.3 _匯入檔案後，輸入條件查詢 ↓</span>', unsafe_allow_html=True)
            INPUT_TEXT = st.text_input("輸入:合約簡編/ISBN/單位名稱查詢")
            INPUT_TEXT = INPUT_TEXT.upper()
        
            # -------------------------------------------▲ 資料處理完成，以下開始篩選 ▼-------------------------------------------------------
            # ---------------- ▼-【功能】第4區 STEP.4 自動分析~BOOM!! ▼-------------------
            if INPUT_TEXT :
                st.markdown('<span style="color:red; font-weight:bold; font-size:22px;"> ｜ STEP.4 _自動分析~BOOM!! ↓</span>', unsafe_allow_html=True)
                with st.expander("STEP.3 _的條件會自動代入，拋出結果"):
                    #篩選條件
                    Filter_contract_number_simple = data["合約簡編"] == INPUT_TEXT
                    Filter_isbn = data["ISBN"] == INPUT_TEXT
                    Filter_publisher = data["單位名稱"].str.contains(INPUT_TEXT)
                    result = data[Filter_contract_number_simple | Filter_isbn | Filter_publisher]
                    
                    # -----------------------------'''# 以下是篩選後的權利金情形(可供下載)'''--------------------------------------
                    styled_text = f'<span style="color:blue; font-size:20px;"> 【一、以下是篩選後的權利金情形(可供下載)】 </span>'
                    st.markdown(styled_text, unsafe_allow_html=True)
                    result.index = range(1,len(result)+1)
                    st.dataframe(result)
                    # -------------------------- 重要資訊統計 ▼---------------------------------
                    #------'''# 以下是銷售情況統計'''------
                    styled_text = f'<span style="color:blue; font-size:20px;"> 【二、以下是銷售情況統計】 </span>'
                    st.markdown(styled_text, unsafe_allow_html=True)
                    total = f"(一){INPUT_TEXT}銷售訂單件數共 : " + str(len(result)) + "(非title數)"
                    total 
                    total_money = f"(二){INPUT_TEXT}單位歷年電子書銷售單位(客戶)總數 : " + str(result["銷售單位"].nunique()) + "(個)"
                    total_money 
                    total_money = f"(三){INPUT_TEXT}單位歷年電子書內容收益總額 : " + str(result["電子書內容收益"].sum() ) + "(新台幣)"
                    total_money        
                    pd_income_peryear = result.groupby(by=['年'])['電子書內容收益'].sum().reset_index()
                    pd_income_peryear.index = range(1,len(pd_income_peryear)+1)
                    pd_income_peryear
                    # ------------------------------------------- 開始繪圖 ▼-------------------------------------------------------
                    # --------------- 繪圖 ▼ 歷年收益(長條圖)-------------
                    styled_text = f'<span style="color:blue; font-size:20px;"> 【三、開始繪圖】 </span>'
                    st.markdown(styled_text, unsafe_allow_html=True)
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
                    fig = px.pie(x, values='電子書內容收益', names='銷售地區', title='【銷售市場】-海內/外收益佔比', 
                                 hover_data=['電子書內容收益'],
                                 )
                    fig.update_layout(height=500, width=700)
                    st.plotly_chart(fig)
                    # --------------- 繪圖 ▼ 銷售客源前五(長條圖)-------------
                    import plotly.express as px
                    import pandas as pd
                    x = result.groupby(by=['銷售單位'])['電子書內容收益'].sum().reset_index().sort_values(by='電子書內容收益', ascending=False).head(5)
                    # 計算總額
                    total_sales = result['電子書內容收益'].sum()
                    # 計算各單位銷售佔總額的比例
                    x['百分比'] = ( (x['電子書內容收益'] / total_sales) * 100 ).round(2).astype(str) + '%\n(佔總收益)'
                    fig = px.bar(x, x='銷售單位', y='電子書內容收益',text='百分比', title='【銷售單位】排名前五')
                    # 在 Streamlit 中显示 Plotly 图表
                    st.plotly_chart(fig)
                    x = result.groupby(by=['銷售單位'])['電子書內容收益'].sum().reset_index().sort_values(by='電子書內容收益', ascending=False).head(5)
                    # --------------- 繪圖 ▼ 【出版品出版年】銷售收益前五(長條圖)-------------
                    import plotly.express as px
                    import pandas as pd
                    total_sales = result['電子書內容收益'].sum()
                    x = result
                    x['出版年'] = result['出版年'].replace('\s', '', regex=True)  # 去除所有空格
                    x = result.groupby(by=['出版年'])['電子書內容收益'].sum().reset_index().sort_values(by='電子書內容收益', ascending=False).head(5)
                    # 計算各單位銷售佔總額的比例
                    x['出版年收益百分比'] = ( (x['電子書內容收益'] / total_sales) * 100 ).round(2).astype(str) + '%\n(佔總收益)'
                    fig = px.bar(x, x='出版年', y='電子書內容收益',text='出版年收益百分比', title='【出版品出版年】銷售收益前五')
                    fig.update_xaxes(type='category')  # 將 x 軸型別設為類別型
                    fig.update_xaxes(tickmode='linear')  # 使用線性刻度
                    fig.update_xaxes(tick0=0)  # 刻度的起始點
                    fig.update_xaxes(dtick=1)  # 刻度的間距
            
                    # 在 Streamlit 中显示 Plotly 图表
                    st.plotly_chart(fig)
            else:
                st.warning("請輸入正確合約簡編/ISBN/單位名稱查詢") 
                
        else:
            st.warning("請上傳 Excel 文件。") 
    else:
        st.warning("密碼錯誤。")
else:
    st.warning("尚未輸入密碼。")
