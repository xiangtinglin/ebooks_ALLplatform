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
        
            #篩選條件
            Filter_contract_number = data["合約詳編"] == NUMBERorISBN
            Filter_isbn = data["ISBN"] == NUMBERorISBN
            result = data[Filter_contract_number | Filter_isbn]
            '''*以下是篩選後的權利金情形(可供下載)'''
            result.index = range(1,len(result)+1)
            st.dataframe(result)
            # ------------------------------------------- 重要資訊統計 ▼-------------------------------------------------------
            '''*以下是書單上架情況統計'''
            total = "總共採購案數(非title數):" + str(len(result))
            total 
            total_money = "歷年單位權利金總額:" + result["權利金"].sum()
            total_money        
            # #匯出檔案
            # result.to_excel(r"C:\Users\User'''\.streamlit\輸出檔案\金尉.xlsx")  
        
            # ------------------------------------------- 開始繪圖 ▼-------------------------------------------------------
        
            '''**開始繪圖(請耐心等候....但其實很快^^ XD)'''
            #繪圖_顯示特殊字形
            from pylab import mpl
            mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']  
            # 指定默認字形：解決plot不能顯示中文問題
            mpl.rcParams['axes.unicode_minus'] = False
        
            import matplotlib.pyplot as plt
            result['權利金'] = float(result['權利金'])
            
            # explode = (0.05, 0.05)
            # colors = ['pink', 'steelblue']
            result.groupby(['銷售單位']).apply(lambda x:x[x.columns]).plot(kind='pie')

            plt.title('【B2C經銷平台】銷售情況',color='r',size=18)
            plt.xlabel("(統計至2023/10/17止)",color='gray',size=10)
            plt.ylabel("佔比(%)",color='blue')
            plt.legend(loc='lower right')
            st.pyplot()
        else:
            st.warning("請上傳 Excel 文件。")
    else:
        st.warning("密碼錯誤。")
else:
    st.warning("尚未輸入密碼。")
