from selenium.webdriver.common.by import By

MOVIES_ALL = (By.CSS_SELECTOR, "div[class*='ipc-metadata-list-summary-item__tc']")
MAIS_INFOS = (By.CSS_SELECTOR, "div[class='sc-59b6048d-1 ctocsE cli-post-element'] button")
BUTTON_1 = (By.CSS_SELECTOR, "button[class='ipc-icon-button cli-info-icon ipc-icon-button--base ipc-icon-button--onAccent2']")
DIR = (By.CSS_SELECTOR, "div[class='sc-9bca7e5d-2 fTTvyd']")
DIR_ART = (By.CSS_SELECTOR, "div[class='sc-9bca7e5d-2 fTTvyd'] ul li")
DESC = (By.CSS_SELECTOR, "div[class='sc-7316798c-2 czDiFW']")
PRIME = (By.CSS_SELECTOR, "div[class='sc-b06b1d17-1 jzVWUl'] a")
CLOSE = (By.CSS_SELECTOR, "button[class='ipc-icon-button ipc-icon-button--baseAlt ipc-icon-button--onBase']")
PRINCI_BILHE = (By.CSS_SELECTOR, "a[href='/chart/boxoffice/?ref_=chttp_ql_1']")
DETAIL_FDS = (By.CSS_SELECTOR, "li[class='sc-ee64acb1-1 lkUVhM']")