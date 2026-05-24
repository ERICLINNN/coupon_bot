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
wait = WebDriverWait(driver, 5)

print(f"🚀 成功接管瀏覽器！目前網頁：{driver.title}")

try:
    # 【神級精準絕對路徑】
    # 1. 優惠碼輸入框
    input_xpath = '//*[@id="__layout"]/div/main/div/div/div/div[2]/article[1]/section[3]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/form/div[1]/div/div/div/div/input'
    # 2. 橘色「使用」按鈕外框
    button_xpath = '//*[@id="__layout"]/div/main/div/div/div/div[2]/article[1]/section[3]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/form/div[1]/div/div/div/div/div'
    # 3. 真正負責跳轉的「前往付款」按鈕本人
    pay_button_xpath = '//*[@id="__layout"]/div/main/div/div/div/div[2]/article[1]/div[3]/div[2]/div[2]/div/button'

    # --- 1. 輸入優惠碼 ---
    print("正在直達定位輸入框...")
    promo_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
    promo_code = "OSAKA0524"  # 👈 搶票前請務必確認這行代碼正確
    
    # 透過 JS 強制注入優惠碼並引發網頁更新事件
    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, promo_input, promo_code)
    print("✅ 1. 透過絕對路徑注入優惠碼成功")
    
    time.sleep(0.1) # 縮短延遲，搶票爭分奪秒

    # --- 2. 點擊「使用」按鈕 ---
    print("正在直達點擊『使用』按鈕...")
    use_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"{button_xpath} | {button_xpath}//button | {button_xpath}//*[contains(text(), '使用')]"))
    )
    try:
        use_button.click()
    except:
        driver.execute_script("arguments[0].click();", use_button)
    print("✅ 2. 成功點擊『使用』按鈕")
    
    time.sleep(0.5) # 給折價券清單跳出來的緩衝時間

    # --- 3. 點擊/勾選優惠券 ---
    try:
        # 根據自動選用最優折扣機制，這裡做為防萬一的自動化保險
        promo_coupon = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '50%')] | //*[contains(text(), '折扣')] | //*[contains(@class, 'coupon')]"))
        )
        driver.execute_script("arguments[0].click();", promo_coupon)
        print("✅ 3. 成功點擊/勾選優惠券")
    except Exception:
        print("ℹ️ 3. 系統已自動選用最優折扣，直接跳過")

    # --- 4. 點擊「前往付款」 ---
    print("正在直達點擊核心『前往付款』按鈕...")
    pay_button = wait.until(EC.element_to_be_clickable((By.XPATH, pay_button_xpath)))
    
    # 雙重保障點擊：先用標準點擊，失敗立刻用 JS 強制點擊
    try:
        pay_button.click()
    except:
        driver.execute_script("arguments[0].click();", pay_button)
        
    print("🔥 4. 成功觸發核心點擊！網頁應該開始跳轉付款頁面了！")

except Exception as e:
    print(f"❌ 執行中途卡住，錯誤訊息: {e}")