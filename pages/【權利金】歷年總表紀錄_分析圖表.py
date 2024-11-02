
# import套件 #   
import streamlit as st
import pandas as pd
#設定密碼
passwords_and_names = {
    "1234": "Hello! '測試者'，您好～",
    "6197": "Ersha湘婷",
}
#標題 
st.title("權利金銷售情況")

# 在首頁輸入密碼
user_input = st.text_input("請輸入密碼（測試用：1234）:", type="password")

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
        pre_data = None  # 預設為 None，後續會根據按鈕或上傳狀態進行賦值      

        # 上傳檔案的選項
        with st.expander("請上傳Excel文件:【權利金】歷年總表紀錄 "):
            uploaded_file = st.file_uploader("p.s.第一次載入大量數據需要數秒，之後查詢會很快^^，匯入後檔案預設存效4小時", type=["xlsx"])

            # 如果上傳了檔案，則加載上傳的檔案
            @st.cache_data(ttl=3600*4)  # 設定生存時間 (TTL) 為 3600*4 秒 (4 小時)
            def fist_loading(file):
                return pd.read_excel(
                    file,
                    sheet_name="2014Q1-今【銷售明細_書籍】ALL項目",
                    usecols=["單位名稱","合約簡編","ISBN","合約詳編","出版年","電子書內容收益","拆帳比例","權利金","銷售單位","季","銷售地區"],
                    engine='openpyxl'
                )

            if uploaded_file:
                pre_data = fist_loading(uploaded_file)
                st.success("已成功加載上傳的檔案！")
                
        #### 自動載入測試檔案的按鈕 ###
        if st.button("使用內嵌測試檔案"):
            # 指定測試檔案路徑
            file_path = "pages/test_file.xlsx"
            # 加載資料
            try:
                pre_data = pd.read_excel(
                    file_path,
                    sheet_name="2014Q1-今【銷售明細_書籍】ALL項目",
                    usecols=["單位名稱","合約簡編","ISBN","合約詳編","出版年","電子書內容收益","拆帳比例","權利金","銷售單位","季","銷售地區"],
                    engine='openpyxl'
                )
                st.success("測試檔案已成功加載！")
            except FileNotFoundError:
                st.error("無法找到測試檔案，請確認檔案已正確放置在指定路徑。")
            except Exception as e:
                st.error(f"加載測試檔案時出現錯誤: {e}")

            ## 同時也下載檔案##
                response = requests.get(file_url)
            if response.status_code == 200:
                # 使用 st.download_button 讓用戶下載檔案
                st.download_button(
                    label="點擊下載檔案",
                    data=response.content,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("檔案下載失敗，請確認連結是否正確。")
                
        # 如果資料已經成功加載，進行後續資料處理
        if pre_data is not None:
            data = pre_data
            # ------------------ 原始資料加工 ▼------------------------
            #拆份季節&年分
            data[["年", "季"]] = data["季"].str.split("Q", expand=True)
            # ------------------ ▼【功能】第2區 ｜STEP.2 _電子書收益總覽 ↓  ▼------------------------
            st.markdown('<span style="color:red; font-weight:bold; font-size:22px;"> ｜ STEP.2 _電子書收益總覽 ↓</span>', unsafe_allow_html=True)
            with st.expander("請選擇條件"):
                view_option = st.selectbox("相同合約簡編旗下的品牌合併計算", ["歷年加總", "近3年"])
    
                # Display selected view
                if view_option == "歷年加總":
                    total_rank = data.groupby("合約簡編")[["電子書內容收益", "權利金"]].sum().round(0).reset_index()
                    total_rank = total_rank.sort_values('電子書內容收益',ascending=False)
                    total_rank.index = range(1, len(total_rank) + 1)
                    st.dataframe(total_rank)
            
                elif view_option == "近3年":
                    # Assuming '年' is the column representing years
                    recent_3_years = sorted(data['年'].unique())[-3:]
                    recent_3years_data = data[data['年'].isin(recent_3_years)]
                    # recent_3years_data = data[data['年'].isin(data['年'].unique()[-3:])]
                    recent_3years_rank = recent_3years_data.groupby(by=['合約簡編'])[['電子書內容收益','權利金']].sum().round(0).reset_index().sort_values(
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
