import pipes
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
st.title("【總經銷】書單上架&分析")

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
        with st.expander( "請上傳Excel文件:(NEW)總經銷書單"):
            uploaded_file = st.file_uploader("p.s.第一次載入大量數據需要數秒，之後查詢會很快^^，匯入後檔案預設存效4小時", type=["xlsx"])
            # ------------------ 暫存函式 ▼------------------------
            import pandas as pd
            sheet_name = "總經銷書單" #@指定分頁
        
            @st.cache_data(ttl=3600*4)  # 設定生存時間 (TTL) 為 3600*4 秒 (4 小時)
            def fist_loading(file_path):
                data = pd.read_excel(file_path,
                                     sheet_name=sheet_name,         #@指定分頁
                                     usecols=[0,2,3,8,17,19,23,25,29,31,36,38,42,44,48,50,54,56,60,62,66,68,72,74,78,80,84,86,90,92,96,98],  #@指定欄位
                                     # nrows=10,                      #@指定列數
                                     # header = 3,                      #header = ?  >> 指定第?列為header(index)
                                     engine='openpyxl')
                return data
            
        if uploaded_file:
            data = fist_loading(uploaded_file)
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
            
            '''> STEP.2 匯入檔案後，輸入條件查詢'''
            NBorISBNorBN = st.selectbox("用合約詳編/ISBN/書名查詢",data["書名"])
            NBorISBNorBN = NBorISBNorBN.upper()
            if NBorISBNorBN:

                '''> STEP.3 自動分析~BOOM!!'''
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
                Filter_contract_number = data["合約編號"] == NBorISBNorBN
                Filter_isbn = data["ISBN"] == NBorISBNorBN
                Filter_BN = data["書名"].str.contains(NBorISBNorBN)
                result = data[Filter_contract_number | Filter_isbn | Filter_BN]
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
            
                # plt.title('&#8203;``【oaicite:0】``&#8203;',color='r',size=18)
                # plt.xlabel("(分類依據：)",color='gray',size=10)
                # plt.ylabel("佔比(%)",color='blue')
                # plt.legend(loc='lower right')
                # plt.show()
                ## 導入套件
                import time
                import numpy as np
                import pandas as pd
                chart_data = pd.DataFrame(
                    np.random.randn(20, 3),
                    columns=['a', 'b', 'c'])
                st.line_chart(chart_data)
            else:
                st.warning("請輸入正確的合約詳編/ISBN/單位名稱查詢")
        else:
            st.warning("請上傳 Excel 文件。")
    else:
        st.warning("密碼錯誤。")
else:
    st.warning("尚未輸入密碼。")
