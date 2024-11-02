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
        
        # 自動載入測試檔案的按鈕
        data = None  # 預設為 None，後續會根據按鈕或上傳狀態進行賦值
        if st.button("使用內嵌測試檔案"):
            # 指定測試檔案路徑
            file_path = "pages/test_file.xlsx"
            # 加載資料
            try:
                data = pd.read_excel(
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
                data = fist_loading(uploaded_file)
                st.success("已成功加載上傳的檔案！")

        # 如果資料已經成功加載，進行後續資料處理
        if data is not None:
            # 拆分季節&年分
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
                    recent_3_years = sorted(data['年'].unique())[-3:]
                    recent_3years_data = data[data['年'].isin(recent_3_years)]
                    recent_3years_rank = recent_3years_data.groupby(by=['合約簡編'])[['電子書內容收益','權利金']].sum().round(0).reset_index().sort_values(
                        by='電子書內容收益', ascending=False)
                    recent_3years_rank.index = range(1, len(recent_3years_rank) + 1)
                    st.dataframe(recent_3years_rank)
                    
            # 其餘的資料處理和分析步驟...（如匯入檔案後查詢和自動分析等）
        else:
            st.warning("請上傳 Excel 文件或點擊使用測試檔案。") 
    else:
        st.warning("密碼錯誤。")
else:
    st.warning("尚未輸入密碼。")
