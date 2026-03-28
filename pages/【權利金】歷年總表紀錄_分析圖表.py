
# # # import套件 #   
# # import streamlit as st
# # import pandas as pd
# # import requests

# # #設定密碼
# # passwords_and_names = {
# #     "1234": "Hello! '測試者'，您好～",
# #     "6197": "Ersha湘婷",
# # }
# # #標題 
# # st.title("權利金銷售情況")

# # # 在首頁輸入密碼
# # user_input = st.text_input("請輸入密碼（測試用：1234）:", type="password")

# # if user_input:    
# #     # 驗證密碼
# #     if user_input in passwords_and_names:
# #         # 獲取對應的名字
# #         user_name = passwords_and_names[user_input]
# #         success_message = st.success(f"Hi~{user_name}！密碼正確，已解鎖應用程序！")
# #         import time
# #         time.sleep(0.9)
# #         success_message.empty()

# # # ------------------------------------------- 在這裡放置您的應用程序主要內容 ▼-------------------------------------------------------
# #         # ------------------ ▼【功能】第一區 ｜STEP.1 _匯入檔案 ▼------------------------
# #         st.markdown('<span style="color:red; font-weight:bold; font-size:22px;"> ｜STEP.1 _匯入檔案(目前檔案無資料庫化，因此需從你電腦匯入檔案) ↓</span>', unsafe_allow_html=True)
# #         pre_data = None  # 預設為 None，後續會根據按鈕或上傳狀態進行賦值      

# #         # 上傳檔案的選項
# #         with st.expander("請上傳Excel文件:【權利金】歷年總表紀錄 "):
# #             uploaded_file = st.file_uploader("p.s.第一次載入大量數據需要數秒，之後查詢會很快^^，匯入後檔案預設存效4小時", type=["xlsx"])

# #             # 如果上傳了檔案，則加載上傳的檔案
# #             @st.cache_data(ttl=3600*4)  # 設定生存時間 (TTL) 為 3600*4 秒 (4 小時)
# #             def fist_loading(file):
# #                 return pd.read_excel(
# #                     file,
# #                     sheet_name="2014Q1-今【銷售明細_書籍】ALL項目",
# #                     usecols=["單位名稱","合約簡編","ISBN","合約詳編","出版年","電子書內容收益","拆帳比例","權利金","銷售單位","季","銷售地區"],
# #                     engine='openpyxl'
# #                 )

# #             if uploaded_file:
# #                 pre_data = fist_loading(uploaded_file)
# #                 st.success("已成功加載上傳的檔案！")
        
        
# #         import io
# #         #### 自動載入測試檔案的按鈕 ###
# #         if st.button("使用內嵌測試檔案"):
# #             # 指定測試檔案路徑
# #             file_path = "pages/test_file.xlsx"
            
# #             # 加載資料
# #             try:
# #                 pre_data = pd.read_excel(
# #                     file_path,
# #                     sheet_name="2014Q1-今【銷售明細_書籍】ALL項目",
# #                     usecols=["單位名稱","合約簡編","ISBN","合約詳編","出版年","電子書內容收益","拆帳比例","權利金","銷售單位","季","銷售地區"],
# #                     engine='openpyxl'
# #                 )
# #                 st.success("測試檔案已成功加載！")
        
# #                 # 準備檔案內容為二進位格式，以供下載
# #                 buffer = io.BytesIO()
# #                 with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
# #                     pre_data.to_excel(writer, index=False, sheet_name="2014Q1-今【銷售明細_書籍】ALL項目")
# #                 buffer.seek(0)  # 將緩衝指標移至開始位置
        
# #                 # 顯示下載按鈕，讓使用者點擊下載
# #                 st.download_button(
# #                     label="下載測試檔案",
# #                     data=buffer,
# #                     file_name="test_file.xlsx",
# #                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #                 )
        
# #             except FileNotFoundError:
# #                 st.error("無法找到測試檔案，請確認檔案已正確放置在指定路徑。")
# #             except Exception as e:
# #                 st.error(f"加載測試檔案時出現錯誤: {e}")
                

                
# #         # 如果資料已經成功加載，進行後續資料處理
# #         if pre_data is not None:
# #             data = pre_data
# #             # ------------------ 原始資料加工 ▼------------------------
# #             #拆份季節&年分
# #             data[["年", "季"]] = data["季"].str.split("Q", expand=True)
# #             # ------------------ ▼【功能】第2區 ｜STEP.2 _電子書收益總覽 ↓  ▼------------------------
# #             st.markdown('<span style="color:red; font-weight:bold; font-size:22px;"> ｜ STEP.2 _電子書收益總覽 ↓</span>', unsafe_allow_html=True)
# #             with st.expander("請選擇條件"):
# #                 view_option = st.selectbox("相同合約簡編旗下的品牌合併計算", ["歷年加總", "近3年"])
    
# #                 # Display selected view
# #                 if view_option == "歷年加總":
# #                     total_rank = data.groupby("合約簡編")[["電子書內容收益", "權利金"]].sum().round(0).reset_index()
# #                     total_rank = total_rank.sort_values('電子書內容收益',ascending=False)
# #                     total_rank.index = range(1, len(total_rank) + 1)
# #                     st.dataframe(total_rank)
            
# #                 elif view_option == "近3年":
# #                     # Assuming '年' is the column representing years
# #                     recent_3_years = sorted(data['年'].unique())[-3:]
# #                     recent_3years_data = data[data['年'].isin(recent_3_years)]
# #                     # recent_3years_data = data[data['年'].isin(data['年'].unique()[-3:])]
# #                     recent_3years_rank = recent_3years_data.groupby(by=['合約簡編'])[['電子書內容收益','權利金']].sum().round(0).reset_index().sort_values(
# #                         by='電子書內容收益', ascending=False)
# #                     recent_3years_rank.index = range(1, len(recent_3years_rank) + 1)
# #                     st.dataframe(recent_3years_rank)  
# #             # ------------------------------------- 【功能】第3區_STEP.3 匯入檔案後，輸入條件查詢 ▼-------------------------                    
# #             st.markdown('<span style="color:red; font-weight:bold; font-size:22px;"> ｜ STEP.3 _匯入檔案後，輸入條件查詢 ↓</span>', unsafe_allow_html=True)
# #             INPUT_TEXT = st.text_input("輸入:合約簡編/ISBN/單位名稱查詢")
# #             INPUT_TEXT = INPUT_TEXT.upper()
        
# #             # -------------------------------------------▲ 資料處理完成，以下開始篩選 ▼-------------------------------------------------------
# #             # ---------------- ▼-【功能】第4區 STEP.4 自動分析~BOOM!! ▼-------------------
# #             if INPUT_TEXT :
# #                 st.markdown('<span style="color:red; font-weight:bold; font-size:22px;"> ｜ STEP.4 _自動分析~BOOM!! ↓</span>', unsafe_allow_html=True)
# #                 with st.expander("STEP.3 _的條件會自動代入，拋出結果"):
# #                     #篩選條件
# #                     Filter_contract_number_simple = data["合約簡編"] == INPUT_TEXT
# #                     Filter_isbn = data["ISBN"] == INPUT_TEXT
# #                     Filter_publisher = data["單位名稱"].str.contains(INPUT_TEXT)
# #                     result = data[Filter_contract_number_simple | Filter_isbn | Filter_publisher]
                    
# #                     # -----------------------------'''# 以下是篩選後的權利金情形(可供下載)'''--------------------------------------
# #                     styled_text = f'<span style="color:blue; font-size:20px;"> 【一、以下是篩選後的權利金情形(可供下載)】 </span>'
# #                     st.markdown(styled_text, unsafe_allow_html=True)
# #                     result.index = range(1,len(result)+1)
# #                     st.dataframe(result)
# #                     # -------------------------- 重要資訊統計 ▼---------------------------------
# #                     #------'''# 以下是銷售情況統計'''------
# #                     styled_text = f'<span style="color:blue; font-size:20px;"> 【二、以下是銷售情況統計】 </span>'
# #                     st.markdown(styled_text, unsafe_allow_html=True)
# #                     total = f"(一){INPUT_TEXT}銷售訂單件數共 : " + str(len(result)) + "(非title數)"
# #                     total 
# #                     total_money = f"(二){INPUT_TEXT}單位歷年電子書銷售單位(客戶)總數 : " + str(result["銷售單位"].nunique()) + "(個)"
# #                     total_money 
# #                     total_money = f"(三){INPUT_TEXT}單位歷年電子書內容收益總額 : " + str(result["電子書內容收益"].sum() ) + "(新台幣)"
# #                     total_money        
# #                     pd_income_peryear = result.groupby(by=['年'])['電子書內容收益'].sum().reset_index()
# #                     pd_income_peryear.index = range(1,len(pd_income_peryear)+1)
# #                     pd_income_peryear
# #                     # ------------------------------------------- 開始繪圖 ▼-------------------------------------------------------
# #                     # --------------- 繪圖 ▼ 歷年收益(長條圖)-------------
# #                     styled_text = f'<span style="color:blue; font-size:20px;"> 【三、開始繪圖】 </span>'
# #                     st.markdown(styled_text, unsafe_allow_html=True)
# #                     import plotly.express as px
# #                     import pandas as pd
# #                     fig = px.bar(pd_income_peryear, x='年', y='電子書內容收益', title='【歷年】電子書內容收益')
# #                     # 調整 x 軸刻度為整數
# #                     fig.update_xaxes(type='category')  # 將 x 軸型別設為類別型
# #                     fig.update_xaxes(tickmode='linear')  # 使用線性刻度
# #                     fig.update_xaxes(tick0=0)  # 刻度的起始點
# #                     fig.update_xaxes(dtick=1)  # 刻度的間距
            
# #                     # 在 Streamlit 中显示 Plotly 图表
# #                     st.plotly_chart(fig)
# #                     # --------------- 繪圖 ▼ 銷售市場-地區(pie圖)-------------
# #                     # 按銷售地區分组并计算權利金总和
# #                     x = result.groupby(by=['銷售地區'])['電子書內容收益'].sum().reset_index()
# #                     fig = px.pie(x, values='電子書內容收益', names='銷售地區', title='【銷售市場】-海內/外收益佔比', 
# #                                  hover_data=['電子書內容收益'],
# #                                  )
# #                     fig.update_layout(height=500, width=700)
# #                     st.plotly_chart(fig)
# #                     # --------------- 繪圖 ▼ 銷售客源前五(長條圖)-------------
# #                     import plotly.express as px
# #                     import pandas as pd
# #                     x = result.groupby(by=['銷售單位'])['電子書內容收益'].sum().reset_index().sort_values(by='電子書內容收益', ascending=False).head(5)
# #                     # 計算總額
# #                     total_sales = result['電子書內容收益'].sum()
# #                     # 計算各單位銷售佔總額的比例
# #                     x['百分比'] = ( (x['電子書內容收益'] / total_sales) * 100 ).round(2).astype(str) + '%\n(佔總收益)'
# #                     fig = px.bar(x, x='銷售單位', y='電子書內容收益',text='百分比', title='【銷售單位】排名前五')
# #                     # 在 Streamlit 中显示 Plotly 图表
# #                     st.plotly_chart(fig)
# #                     x = result.groupby(by=['銷售單位'])['電子書內容收益'].sum().reset_index().sort_values(by='電子書內容收益', ascending=False).head(5)
# #                     # --------------- 繪圖 ▼ 【出版品出版年】銷售收益前五(長條圖)-------------
# #                     import plotly.express as px
# #                     import pandas as pd
# #                     total_sales = result['電子書內容收益'].sum()
# #                     x = result
# #                     x['出版年'] = result['出版年'].replace('\s', '', regex=True)  # 去除所有空格
# #                     x = result.groupby(by=['出版年'])['電子書內容收益'].sum().reset_index().sort_values(by='電子書內容收益', ascending=False).head(5)
# #                     # 計算各單位銷售佔總額的比例
# #                     x['出版年收益百分比'] = ( (x['電子書內容收益'] / total_sales) * 100 ).round(2).astype(str) + '%\n(佔總收益)'
# #                     fig = px.bar(x, x='出版年', y='電子書內容收益',text='出版年收益百分比', title='【出版品出版年】銷售收益前五')
# #                     fig.update_xaxes(type='category')  # 將 x 軸型別設為類別型
# #                     fig.update_xaxes(tickmode='linear')  # 使用線性刻度
# #                     fig.update_xaxes(tick0=0)  # 刻度的起始點
# #                     fig.update_xaxes(dtick=1)  # 刻度的間距
            
# #                     # 在 Streamlit 中显示 Plotly 图表
# #                     st.plotly_chart(fig)
# #             else:
# #                 st.warning("請輸入正確合約簡編/ISBN/單位名稱查詢") 
                
# #         else:
# #             st.warning("請上傳 Excel 文件。") 
# #     else:
# #         st.warning("密碼錯誤。")
# # else:
# #     st.warning("尚未輸入密碼。")


# # import套件
# import streamlit as st
# import pandas as pd
# import requests
# import io
# import plotly.express as px

# # ----------------------------
# # 基本設定
# # ----------------------------
# st.set_page_config(page_title="權利金銷售情況", layout="wide")

# # 設定密碼
# passwords_and_names = {
#     "1234": "Hello! '測試者'，您好～",
#     "6197": "Ersha湘婷",
# }

# # 初始化 session state
# if "pre_data" not in st.session_state:
#     st.session_state.pre_data = None

# if "data_source" not in st.session_state:
#     st.session_state.data_source = None

# # 標題
# st.title("權利金銷售情況")

# # ----------------------------
# # 快取讀檔函式
# # ----------------------------
# @st.cache_data(ttl=3600 * 4)  # 4小時
# def first_loading(file):
#     return pd.read_excel(
#         file,
#         sheet_name="2014Q1-今【銷售明細_書籍】ALL項目",
#         usecols=[
#             "單位名稱", "合約簡編", "ISBN", "合約詳編", "出版年",
#             "電子書內容收益", "拆帳比例", "權利金", "銷售單位", "季", "銷售地區"
#         ],
#         engine="openpyxl"
#     )

# @st.cache_data(ttl=3600 * 4)
# def load_builtin_file(file_path):
#     return pd.read_excel(
#         file_path,
#         sheet_name="2014Q1-今【銷售明細_書籍】ALL項目",
#         usecols=[
#             "單位名稱", "合約簡編", "ISBN", "合約詳編", "出版年",
#             "電子書內容收益", "拆帳比例", "權利金", "銷售單位", "季", "銷售地區"
#         ],
#         engine="openpyxl"
#     )

# # ----------------------------
# # 密碼區
# # ----------------------------
# user_input = st.text_input("請輸入密碼（測試用：1234）:", type="password")

# if user_input:
#     if user_input in passwords_and_names:
#         user_name = passwords_and_names[user_input]
#         st.success(f"Hi~{user_name}！密碼正確，已解鎖應用程序！")

#         # -------------------------------------------
#         # STEP.1 匯入檔案
#         # -------------------------------------------
#         st.markdown(
#             '<span style="color:red; font-weight:bold; font-size:22px;">'
#             ' ｜STEP.1 _匯入檔案(目前檔案無資料庫化，因此需從你電腦匯入檔案) ↓'
#             '</span>',
#             unsafe_allow_html=True
#         )

#         with st.expander("請上傳Excel文件:【權利金】歷年總表紀錄"):
#             uploaded_file = st.file_uploader(
#                 "p.s.第一次載入大量數據需要數秒，之後查詢會很快^^，匯入後資料快取4小時",
#                 type=["xlsx"]
#             )

#             if uploaded_file is not None:
#                 try:
#                     st.session_state.pre_data = first_loading(uploaded_file)
#                     st.session_state.data_source = "uploaded"
#                     st.success("已成功加載上傳的檔案！")
#                 except Exception as e:
#                     st.error(f"上傳檔案讀取失敗：{e}")

#         # ----------------------------
#         # 內嵌測試檔案按鈕
#         # ----------------------------
#         col1, col2 = st.columns([1, 2])

#         with col1:
#             if st.button("使用內嵌測試檔案"):
#                 file_path = "pages/test_file.xlsx"
#                 try:
#                     st.session_state.pre_data = load_builtin_file(file_path)
#                     st.session_state.data_source = "builtin"
#                     st.success("測試檔案已成功加載！")
#                 except FileNotFoundError:
#                     st.error("無法找到測試檔案，請確認檔案已正確放置在指定路徑。")
#                 except Exception as e:
#                     st.error(f"加載測試檔案時出現錯誤：{e}")

#         with col2:
#             if st.session_state.data_source == "builtin" and st.session_state.pre_data is not None:
#                 try:
#                     buffer = io.BytesIO()
#                     with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
#                         st.session_state.pre_data.to_excel(
#                             writer,
#                             index=False,
#                             sheet_name="2014Q1-今【銷售明細_書籍】ALL項目"
#                         )
#                     buffer.seek(0)

#                     st.download_button(
#                         label="下載測試檔案",
#                         data=buffer,
#                         file_name="test_file.xlsx",
#                         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                     )
#                 except Exception as e:
#                     st.error(f"產生測試檔案下載按鈕時發生錯誤：{e}")

#         # -------------------------------------------
#         # 如果資料已經成功加載，進行後續資料處理
#         # -------------------------------------------
#         if st.session_state.pre_data is not None:
#             data = st.session_state.pre_data.copy()

#             # ------------------ 原始資料加工 ------------------------
#             data["季"] = data["季"].astype(str)
#             split_result = data["季"].str.split("Q", expand=True)

#             if split_result.shape[1] >= 2:
#                 data["年"] = split_result[0]
#                 data["季"] = split_result[1]
#             else:
#                 data["年"] = ""
#                 data["季"] = data["季"]

#             # 去除前後空白
#             data["年"] = data["年"].astype(str).str.strip()
#             data["季"] = data["季"].astype(str).str.strip()

#             # -------------------------------------------
#             # STEP.2 電子書收益總覽
#             # -------------------------------------------
#             st.markdown(
#                 '<span style="color:red; font-weight:bold; font-size:22px;">'
#                 ' ｜ STEP.2 _電子書收益總覽 ↓</span>',
#                 unsafe_allow_html=True
#             )

#             with st.expander("請選擇條件"):
#                 view_option = st.selectbox("相同合約簡編旗下的品牌合併計算", ["歷年加總", "近3年"])

#                 if view_option == "歷年加總":
#                     total_rank = (
#                         data.groupby("合約簡編")[["電子書內容收益", "權利金"]]
#                         .sum()
#                         .round(0)
#                         .reset_index()
#                         .sort_values("電子書內容收益", ascending=False)
#                     )
#                     total_rank.index = range(1, len(total_rank) + 1)
#                     st.dataframe(total_rank, use_container_width=True)

#                 elif view_option == "近3年":
#                     valid_years = sorted([y for y in data["年"].dropna().unique() if str(y).strip() != ""])
#                     recent_3_years = valid_years[-3:] if len(valid_years) >= 3 else valid_years

#                     recent_3years_data = data[data["年"].isin(recent_3_years)]

#                     recent_3years_rank = (
#                         recent_3years_data.groupby("合約簡編")[["電子書內容收益", "權利金"]]
#                         .sum()
#                         .round(0)
#                         .reset_index()
#                         .sort_values("電子書內容收益", ascending=False)
#                     )
#                     recent_3years_rank.index = range(1, len(recent_3years_rank) + 1)
#                     st.dataframe(recent_3years_rank, use_container_width=True)

#             # -------------------------------------------
#             # STEP.3 輸入條件查詢
#             # -------------------------------------------
#             st.markdown(
#                 '<span style="color:red; font-weight:bold; font-size:22px;">'
#                 ' ｜ STEP.3 _匯入檔案後，輸入條件查詢 ↓</span>',
#                 unsafe_allow_html=True
#             )

#             input_text = st.text_input("輸入:合約簡編/ISBN/單位名稱查詢")
#             input_text = input_text.strip().upper()

#             # -------------------------------------------
#             # STEP.4 自動分析
#             # -------------------------------------------
#             if input_text:
#                 st.markdown(
#                     '<span style="color:red; font-weight:bold; font-size:22px;">'
#                     ' ｜ STEP.4 _自動分析~BOOM!! ↓</span>',
#                     unsafe_allow_html=True
#                 )

#                 with st.expander("STEP.3 的條件會自動代入，拋出結果", expanded=True):
#                     # 篩選條件
#                     filter_contract_number_simple = (
#                         data["合約簡編"].astype(str).str.strip().str.upper() == input_text
#                     )
#                     filter_isbn = (
#                         data["ISBN"].astype(str).str.strip().str.upper() == input_text
#                     )
#                     filter_publisher = (
#                         data["單位名稱"].astype(str).str.strip().str.upper().str.contains(input_text, na=False)
#                     )

#                     result = data[
#                         filter_contract_number_simple | filter_isbn | filter_publisher
#                     ].copy()

#                     # -----------------------------
#                     # 一、表格結果
#                     # -----------------------------
#                     st.markdown(
#                         '<span style="color:blue; font-size:20px;">'
#                         '【一、以下是篩選後的權利金情形(可供下載)】</span>',
#                         unsafe_allow_html=True
#                     )

#                     result.index = range(1, len(result) + 1)
#                     st.dataframe(result, use_container_width=True)

#                     if not result.empty:
#                         csv_data = result.to_csv(index=False).encode("utf-8-sig")
#                         st.download_button(
#                             label="下載查詢結果 CSV",
#                             data=csv_data,
#                             file_name=f"{input_text}_查詢結果.csv",
#                             mime="text/csv"
#                         )

#                     # -----------------------------
#                     # 二、統計資訊
#                     # -----------------------------
#                     st.markdown(
#                         '<span style="color:blue; font-size:20px;">'
#                         '【二、以下是銷售情況統計】</span>',
#                         unsafe_allow_html=True
#                     )

#                     st.write(f"(一) {input_text} 銷售訂單件數共：{len(result)}（非 title 數）")

#                     if not result.empty:
#                         st.write(f"(二) {input_text} 單位歷年電子書銷售單位(客戶)總數：{result['銷售單位'].nunique()}（個）")
#                         st.write(f"(三) {input_text} 單位歷年電子書內容收益總額：{result['電子書內容收益'].sum()}（新台幣）")
#                     else:
#                         st.warning("查無符合條件的資料。")

#                     # -----------------------------
#                     # 三、繪圖
#                     # -----------------------------
#                     if not result.empty:
#                         st.markdown(
#                             '<span style="color:blue; font-size:20px;">'
#                             '【三、開始繪圖】</span>',
#                             unsafe_allow_html=True
#                         )

#                         # 1. 歷年收益長條圖
#                         pd_income_peryear = (
#                             result.groupby("年")["電子書內容收益"]
#                             .sum()
#                             .reset_index()
#                             .sort_values("年")
#                         )

#                         fig1 = px.bar(
#                             pd_income_peryear,
#                             x="年",
#                             y="電子書內容收益",
#                             title="【歷年】電子書內容收益"
#                         )
#                         fig1.update_xaxes(type="category")
#                         st.plotly_chart(fig1, use_container_width=True)

#                         # 2. 銷售市場地區 pie 圖
#                         market_data = (
#                             result.groupby("銷售地區")["電子書內容收益"]
#                             .sum()
#                             .reset_index()
#                         )

#                         if not market_data.empty:
#                             fig2 = px.pie(
#                                 market_data,
#                                 values="電子書內容收益",
#                                 names="銷售地區",
#                                 title="【銷售市場】-海內/外收益佔比",
#                                 hover_data=["電子書內容收益"]
#                             )
#                             st.plotly_chart(fig2, use_container_width=True)

#                         # 3. 銷售單位前五
#                         sales_unit_top5 = (
#                             result.groupby("銷售單位")["電子書內容收益"]
#                             .sum()
#                             .reset_index()
#                             .sort_values("電子書內容收益", ascending=False)
#                             .head(5)
#                         )

#                         total_sales = result["電子書內容收益"].sum()

#                         if total_sales != 0 and not sales_unit_top5.empty:
#                             sales_unit_top5["百分比"] = (
#                                 (sales_unit_top5["電子書內容收益"] / total_sales) * 100
#                             ).round(2).astype(str) + "%\n(佔總收益)"

#                             fig3 = px.bar(
#                                 sales_unit_top5,
#                                 x="銷售單位",
#                                 y="電子書內容收益",
#                                 text="百分比",
#                                 title="【銷售單位】排名前五"
#                             )
#                             st.plotly_chart(fig3, use_container_width=True)

#                         # 4. 出版年收益前五
#                         result["出版年"] = result["出版年"].astype(str).str.replace(r"\s+", "", regex=True)

#                         pubyear_top5 = (
#                             result.groupby("出版年")["電子書內容收益"]
#                             .sum()
#                             .reset_index()
#                             .sort_values("電子書內容收益", ascending=False)
#                             .head(5)
#                         )

#                         if total_sales != 0 and not pubyear_top5.empty:
#                             pubyear_top5["出版年收益百分比"] = (
#                                 (pubyear_top5["電子書內容收益"] / total_sales) * 100
#                             ).round(2).astype(str) + "%\n(佔總收益)"

#                             fig4 = px.bar(
#                                 pubyear_top5,
#                                 x="出版年",
#                                 y="電子書內容收益",
#                                 text="出版年收益百分比",
#                                 title="【出版品出版年】銷售收益前五"
#                             )
#                             fig4.update_xaxes(type="category")
#                             st.plotly_chart(fig4, use_container_width=True)
#             else:
#                 st.warning("請輸入正確合約簡編 / ISBN / 單位名稱查詢")
#         else:
#             st.warning("請先上傳 Excel 文件，或點擊『使用內嵌測試檔案』。")
#     else:
#         st.warning("密碼錯誤。")
# else:
#     st.warning("尚未輸入密碼。")


import io
import streamlit as st
import pandas as pd
import plotly.express as px


# =========================
# 基本設定
# =========================
st.set_page_config(
    page_title="權利金銷售情況",
    layout="wide"
)

PASSWORDS_AND_NAMES = {
    "1234": "Hello! '測試者'，您好～",
    "6197": "Ersha湘婷",
}

SHEET_NAME = "2014Q1-今【銷售明細_書籍】ALL項目"
USE_COLS = [
    "單位名稱", "合約簡編", "ISBN", "合約詳編", "出版年",
    "電子書內容收益", "拆帳比例", "權利金", "銷售單位", "季", "銷售地區"
]
BUILTIN_FILE_PATH = "pages/test_file.xlsx"


# =========================
# Session State 初始化
# =========================
def init_session_state():
    defaults = {
        "authenticated": False,
        "user_name": "",
        "raw_data": None,
        "data_source": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =========================
# 資料讀取
# =========================
@st.cache_data(ttl=3600 * 4)
def load_excel(file_obj):
    df = pd.read_excel(
        file_obj,
        sheet_name=SHEET_NAME,
        usecols=USE_COLS,
        engine="openpyxl"
    )
    return df


@st.cache_data(ttl=3600 * 4)
def load_builtin_excel(file_path):
    df = pd.read_excel(
        file_path,
        sheet_name=SHEET_NAME,
        usecols=USE_COLS,
        engine="openpyxl"
    )
    return df


# =========================
# 資料前處理
# =========================
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    # 季欄位拆成年、季
    data["季"] = data["季"].astype(str).str.strip()
    split_result = data["季"].str.split("Q", expand=True)

    if split_result.shape[1] >= 2:
        data["年"] = split_result[0].astype(str).str.strip()
        data["季別"] = split_result[1].astype(str).str.strip()
    else:
        data["年"] = ""
        data["季別"] = ""

    # 常用欄位字串化，避免 contains / upper 報錯
    for col in ["單位名稱", "合約簡編", "ISBN", "合約詳編", "出版年", "銷售單位", "銷售地區"]:
        data[col] = data[col].astype(str).str.strip()

    # 數值欄位轉型
    for col in ["電子書內容收益", "拆帳比例", "權利金"]:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    # 出版年清乾淨
    data["出版年"] = data["出版年"].astype(str).str.replace(r"\s+", "", regex=True)

    return data


# =========================
# 驗證密碼
# =========================
def render_login():
    st.title("權利金銷售情況")

    password_input = st.text_input("請輸入密碼（測試用：1234）:", type="password")

    if not password_input:
        st.warning("尚未輸入密碼。")
        return

    if password_input in PASSWORDS_AND_NAMES:
        st.session_state.authenticated = True
        st.session_state.user_name = PASSWORDS_AND_NAMES[password_input]
        st.success(f"Hi~{st.session_state.user_name}！密碼正確，已解鎖應用程序！")
    else:
        st.session_state.authenticated = False
        st.warning("密碼錯誤。")


# =========================
# 檔案載入區
# =========================
def render_file_loader():
    st.markdown(
        '<span style="color:red; font-weight:bold; font-size:22px;">'
        '｜STEP.1 _匯入檔案 ↓'
        '</span>',
        unsafe_allow_html=True
    )

    with st.expander("請上傳 Excel 文件：【權利金】歷年總表紀錄", expanded=True):
        uploaded_file = st.file_uploader(
            "第一次載入大量數據可能需要數秒；匯入後資料快取 4 小時",
            type=["xlsx"]
        )

        if uploaded_file is not None:
            try:
                st.session_state.raw_data = load_excel(uploaded_file)
                st.session_state.data_source = "uploaded"
                st.success("已成功加載上傳檔案。")
            except Exception as e:
                st.error(f"上傳檔案讀取失敗：{e}")

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("使用內嵌測試檔案"):
            try:
                st.session_state.raw_data = load_builtin_excel(BUILTIN_FILE_PATH)
                st.session_state.data_source = "builtin"
                st.success("測試檔案已成功加載。")
            except FileNotFoundError:
                st.error("找不到內嵌測試檔案，請確認路徑是否正確。")
            except Exception as e:
                st.error(f"加載測試檔案時發生錯誤：{e}")

    with col2:
        if st.session_state.data_source == "builtin" and st.session_state.raw_data is not None:
            try:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    st.session_state.raw_data.to_excel(
                        writer,
                        index=False,
                        sheet_name=SHEET_NAME
                    )
                buffer.seek(0)

                st.download_button(
                    label="下載測試檔案",
                    data=buffer,
                    file_name="test_file.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"建立測試檔案下載時發生錯誤：{e}")


# =========================
# STEP.2 總覽
# =========================
def render_overview(data: pd.DataFrame):
    st.markdown(
        '<span style="color:red; font-weight:bold; font-size:22px;">'
        '｜STEP.2 _電子書收益總覽 ↓'
        '</span>',
        unsafe_allow_html=True
    )

    with st.expander("總覽條件", expanded=False):
        view_option = st.selectbox(
            "相同合約簡編旗下的品牌合併計算",
            ["歷年加總", "近3年"]
        )

        if view_option == "歷年加總":
            total_rank = (
                data.groupby("合約簡編")[["電子書內容收益", "權利金"]]
                .sum()
                .round(0)
                .reset_index()
                .sort_values("電子書內容收益", ascending=False)
            )
            total_rank.index = range(1, len(total_rank) + 1)
            st.dataframe(total_rank, use_container_width=True)

        elif view_option == "近3年":
            valid_years = sorted([y for y in data["年"].unique() if str(y).strip() != ""])
            recent_3_years = valid_years[-3:] if len(valid_years) >= 3 else valid_years

            recent_data = data[data["年"].isin(recent_3_years)]
            recent_rank = (
                recent_data.groupby("合約簡編")[["電子書內容收益", "權利金"]]
                .sum()
                .round(0)
                .reset_index()
                .sort_values("電子書內容收益", ascending=False)
            )
            recent_rank.index = range(1, len(recent_rank) + 1)
            st.dataframe(recent_rank, use_container_width=True)


# =========================
# 多條件查詢
# =========================
def filter_data(
    data: pd.DataFrame,
    keyword: str,
    keyword_mode: str,
    selected_years: list,
    selected_regions: list,
    selected_sales_units: list,
):
    filtered = data.copy()

    # 年份篩選
    if selected_years:
        filtered = filtered[filtered["年"].isin(selected_years)]

    # 地區篩選
    if selected_regions:
        filtered = filtered[filtered["銷售地區"].isin(selected_regions)]

    # 銷售單位篩選
    if selected_sales_units:
        filtered = filtered[filtered["銷售單位"].isin(selected_sales_units)]

    # 關鍵字篩選
    keyword = keyword.strip().upper()
    if keyword:
        publisher_col = filtered["單位名稱"].astype(str).str.upper()
        contract_col = filtered["合約簡編"].astype(str).str.upper()
        isbn_col = filtered["ISBN"].astype(str).str.upper()
        detail_col = filtered["合約詳編"].astype(str).str.upper()

        if keyword_mode == "精確比對":
            mask = (
                (contract_col == keyword) |
                (isbn_col == keyword) |
                (publisher_col == keyword) |
                (detail_col == keyword)
            )
        else:  # 模糊搜尋
            mask = (
                contract_col.str.contains(keyword, na=False) |
                isbn_col.str.contains(keyword, na=False) |
                publisher_col.str.contains(keyword, na=False) |
                detail_col.str.contains(keyword, na=False)
            )

        filtered = filtered[mask]

    return filtered


# =========================
# STEP.3 查詢區
# =========================
def render_query_section(data: pd.DataFrame):
    st.markdown(
        '<span style="color:red; font-weight:bold; font-size:22px;">'
        '｜STEP.3 _匯入檔案後，輸入條件查詢 ↓'
        '</span>',
        unsafe_allow_html=True
    )

    years = sorted([y for y in data["年"].dropna().unique() if str(y).strip() != ""])
    regions = sorted([x for x in data["銷售地區"].dropna().unique() if str(x).strip() != ""])
    sales_units = sorted([x for x in data["銷售單位"].dropna().unique() if str(x).strip() != ""])

    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("輸入：合約簡編 / ISBN / 單位名稱 / 合約詳編")
    with col2:
        keyword_mode = st.selectbox("查詢模式", ["模糊搜尋", "精確比對"])

    col3, col4, col5 = st.columns(3)
    with col3:
        selected_years = st.multiselect("年份篩選", years)
    with col4:
        selected_regions = st.multiselect("銷售地區篩選", regions)
    with col5:
        selected_sales_units = st.multiselect("銷售單位篩選", sales_units)

    result = filter_data(
        data=data,
        keyword=keyword,
        keyword_mode=keyword_mode,
        selected_years=selected_years,
        selected_regions=selected_regions,
        selected_sales_units=selected_sales_units,
    )

    return keyword, result


# =========================
# 統計卡片
# =========================
def render_summary_cards(result: pd.DataFrame, keyword: str):
    display_keyword = keyword.strip() if keyword.strip() else "目前篩選條件"

    total_orders = len(result)
    total_clients = result["銷售單位"].nunique() if not result.empty else 0
    total_income = result["電子書內容收益"].sum() if not result.empty else 0
    total_royalty = result["權利金"].sum() if not result.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("訂單件數", f"{total_orders}")
    col2.metric("銷售單位數", f"{total_clients}")
    col3.metric("電子書內容收益", f"{total_income:,.0f}")
    col4.metric("權利金總額", f"{total_royalty:,.0f}")

    st.caption(f"目前統計對象：{display_keyword}")


# =========================
# 結果表格
# =========================
def render_result_table(result: pd.DataFrame, keyword: str):
    st.markdown(
        '<span style="color:blue; font-size:20px;">'
        '【一、以下是篩選後的權利金情形】'
        '</span>',
        unsafe_allow_html=True
    )

    display_df = result.copy()
    display_df.index = range(1, len(display_df) + 1)
    st.dataframe(display_df, use_container_width=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8-sig")
    file_name = f"{keyword.strip() if keyword.strip() else 'query_result'}_查詢結果.csv"

    st.download_button(
        label="下載查詢結果 CSV",
        data=csv_data,
        file_name=file_name,
        mime="text/csv"
    )


# =========================
# 圖表區
# =========================
def render_charts(result: pd.DataFrame):
    st.markdown(
        '<span style="color:blue; font-size:20px;">'
        '【二、視覺化分析】'
        '</span>',
        unsafe_allow_html=True
    )

    # 歷年收益
    income_per_year = (
        result.groupby("年")["電子書內容收益"]
        .sum()
        .reset_index()
        .sort_values("年")
    )

    # 銷售地區
    market_data = (
        result.groupby("銷售地區")["電子書內容收益"]
        .sum()
        .reset_index()
    )

    # 銷售單位前五
    sales_unit_top5 = (
        result.groupby("銷售單位")["電子書內容收益"]
        .sum()
        .reset_index()
        .sort_values("電子書內容收益", ascending=False)
        .head(5)
    )

    # 出版年前五
    pubyear_top5 = (
        result.groupby("出版年")["電子書內容收益"]
        .sum()
        .reset_index()
        .sort_values("電子書內容收益", ascending=False)
        .head(5)
    )

    total_sales = result["電子書內容收益"].sum()

    c1, c2 = st.columns(2)

    with c1:
        fig1 = px.bar(
            income_per_year,
            x="年",
            y="電子書內容收益",
            title="【歷年】電子書內容收益"
        )
        fig1.update_xaxes(type="category")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        if not market_data.empty:
            fig2 = px.pie(
                market_data,
                values="電子書內容收益",
                names="銷售地區",
                title="【銷售市場】海內 / 外收益佔比"
            )
            st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        if total_sales != 0 and not sales_unit_top5.empty:
            sales_unit_top5 = sales_unit_top5.copy()
            sales_unit_top5["百分比"] = (
                (sales_unit_top5["電子書內容收益"] / total_sales) * 100
            ).round(2).astype(str) + "%"

            fig3 = px.bar(
                sales_unit_top5,
                x="銷售單位",
                y="電子書內容收益",
                text="百分比",
                title="【銷售單位】收益前五"
            )
            st.plotly_chart(fig3, use_container_width=True)

    with c4:
        if total_sales != 0 and not pubyear_top5.empty:
            pubyear_top5 = pubyear_top5.copy()
            pubyear_top5["百分比"] = (
                (pubyear_top5["電子書內容收益"] / total_sales) * 100
            ).round(2).astype(str) + "%"

            fig4 = px.bar(
                pubyear_top5,
                x="出版年",
                y="電子書內容收益",
                text="百分比",
                title="【出版年】收益前五"
            )
            fig4.update_xaxes(type="category")
            st.plotly_chart(fig4, use_container_width=True)


# =========================
# 主程式
# =========================
def main():
    init_session_state()
    render_login()

    if not st.session_state.authenticated:
        return

    render_file_loader()

    if st.session_state.raw_data is None:
        st.warning("請先上傳 Excel，或使用內嵌測試檔案。")
        return

    data = preprocess_data(st.session_state.raw_data)

    render_overview(data)

    keyword, result = render_query_section(data)

    st.markdown(
        '<span style="color:red; font-weight:bold; font-size:22px;">'
        '｜STEP.4 _自動分析 ~ BOOM!! ↓'
        '</span>',
        unsafe_allow_html=True
    )

    with st.expander("依據 STEP.3 條件自動分析", expanded=True):
        if result.empty:
            st.warning("查無符合條件的資料。")
            return

        render_summary_cards(result, keyword)
        render_result_table(result, keyword)
        render_charts(result)


if __name__ == "__main__":
    main()
