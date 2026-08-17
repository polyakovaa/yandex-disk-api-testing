from enum import Enum


class BrowserName(str, Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"


class BrowserPreference(str, Enum):
    FIREFOX_DOWNLOAD_DIR = "browser.download.dir"
