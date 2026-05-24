import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 設定接管已開啟的 Chrome ---
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=chrome_options)

# 設定：驗證並跳出優惠券的等待時間
wait_coupon = WebDriverWait(driver, 1.5) 
wait = WebDriverWait(driver, 1.0)

print(f"🚀 成功接管瀏覽器！目前網頁：{driver.title}")
print("🔥 搶票模式（精準卡片 ID + 黃金時差版）已啟動...")

# 【絕對路徑定義】
input_xpath = '//*[@id="__layout"]/div/main/div/div/div/div[2]/article[1]/section[3]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/form/div[1]/div/div/div/div/input'
button_xpath = '//*[@id="__layout"]/div/main/div/div/div/div[2]/article[1]/section[3]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/form/div[1]/div/div/div/div/div'
pay_button_xpath = '//*[@id="__layout"]/div/main/div/div/div/div[2]/article[1]/div[3]/div[2]/div[2]/div/button'

promo_code = "HOTEL96202605"  # 👈 搶票前請務必確認這行代碼正確
coupon_card_xpath = f'//*[@id="mkt-coupon-card-{promo_code}"]/div[2]/div[2]'

retry_count = 0

# === 無限循環衝鋒 ===
while True:
    try:
        retry_count += 1
        print(f"\n🔄 正在進行第 {retry_count} 次嘗試輸入代碼...")

        # 1. 定位輸入框並注入優惠碼
        promo_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
        
        promo_input.click()
        promo_input.clear()
        
        promo_input.send_keys(promo_code)
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, promo_input, promo_code)
        
        # 2. 點擊「使用」按鈕
        use_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"{button_xpath} | {button_xpath}//button | {button_xpath}//*[contains(text(), '使用')]"))
        )
        try:
            use_button.click()
        except:
            driver.execute_script("arguments[0].click();", use_button)
        
        print(f"👉 已點擊『使用』，正在盯著網頁，等待專屬卡片 ID 出現...")

        # 🚨 【阻擋判定】
        try:
            error_msg = driver.find_element(By.XPATH, "//*[contains(text(), '已用罄')] | //*[contains(text(), '無法使用')]")
            if error_msg.is_displayed():
                print(f"🛑 殘念！偵測到真正阻擋訊息：『{error_msg.text}』")
                print("⚠️ 優惠碼已被搶光！腳本終止，請手動換碼或原價結帳！")
                break 
        except:
            pass 

        # 3. 【嚴格等待優惠券出現：使用全新精準 ID】
        # 程式會精準鎖定包含代碼名字的卡片區塊
        coupon_card = wait_coupon.until(
            EC.presence_of_element_located((By.XPATH, coupon_card_xpath))
        )
        
        print(f"🎯 成功直達抓到目標優惠券！正在進行強制點擊勾選...")
        driver.execute_script("arguments[0].click();", coupon_card)
        
        # 💡 【黃金時差優化】：對付網頁「黑一下」的重新計算與渲染
        time.sleep(0.2) 

        # 4. 發動總攻擊點擊「前往付款」
        print("⚡ 正在發動總攻擊：直達點擊核心『前往付款』按鈕...")
        pay_button = wait.until(EC.element_to_be_clickable((By.XPATH, pay_button_xpath)))
        try:
            pay_button.click()
        except:
            driver.execute_script("arguments[0].click();", pay_button)
            
        print("🔥 【大成功】已成功選用最新優惠券並觸發前往付款！")
        break  

    except Exception as e:
        print(f"❌ 網頁未出現卡片元件（活動可能尚未開始）。0.1秒後重新嘗試...")
        time.sleep(0.1)