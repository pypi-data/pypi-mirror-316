import time
import shutil
import logging
import selenium.common.exceptions

from webdriver_hj3415 import drivers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils_hj3415 import noti

# 환경변수를 이용해서 브라우저 결정
import os
from decouple import Config, RepositoryEnv

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
config = Config(RepositoryEnv(env_path))

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = os.path.join(WORKING_DIR, '_down_krx')

headless = config('HEADLESS', cast=bool)
driver_version = config('DRIVER_VERSION', default=None)

from utils_hj3415 import helpers

scraper_logger = helpers.setup_logger('scraper_logger', logging.WARNING)

def download_krx300():
    """
    tigeretf 사이트에서 krx300 구성종목 파일을 다운로드한다.
    파일다운은 save_to 에 설정된 파일경로를 사용한다.
    :return:
    """
    # 임시폴더 정리
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

    print(f'Download krx300 file and save to {TEMP_DIR}.')
    # tiger etf krx300 주소
    url = "https://www.tigeretf.com/ko/product/search/detail/index.do?ksdFund=KR7292160009"

    webdriver = drivers.get_chrome(driver_version=driver_version, headless=headless, temp_dir=TEMP_DIR)

    webdriver.get(url)
    webdriver.implicitly_wait(10)

    # 구성 종목 다운 버튼
    btn_xpath = '// *[ @ id = "formPdfList"] / div[3] / div[1] / div / div / a'

    trying = 0
    while trying < 3:
        try:
            WebDriverWait(webdriver, 10).until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
            button = webdriver.find_element(By.XPATH, btn_xpath)
            button.click()
            time.sleep(2)  # 파일 다운로드 대기
            break
        except selenium.common.exceptions.TimeoutException:
            trying += 1
            scraper_logger.error("다운로드 버튼이 준비되지 않아서 다시 시도합니다.")
            webdriver.refresh()
            time.sleep(2)
            if trying >= 3:
                noti.telegram_to('manager', "krx300 다운로드에 문제가 있습니다. ")
                raise Exception(f"{url} 페이지 로딩에 문제가 있습니다.")
    webdriver.close()

if __name__ == '__main__':
    download_krx300()