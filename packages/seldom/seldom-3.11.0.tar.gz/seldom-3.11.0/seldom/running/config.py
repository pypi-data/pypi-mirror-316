"""
Seldom configuration file
"""
import threading


class Seldom:
    """
    Seldom browser driver
    """
    _thread_local = threading.local()

    @property
    def driver(self):
        """
        Browser or App driver
        """
        return getattr(self._thread_local, 'driver', None)

    @driver.setter
    def driver(self, value):
        self._thread_local.driver = value

    @property
    def base_url(self):
        """
        API base url
        """
        return getattr(self._thread_local, 'base_url', None)

    @base_url.setter
    def base_url(self, value):
        self._thread_local.base_url = value

    timeout = 10
    debug = False
    compare_url = None
    app_server = None
    app_info = None
    app_package = None
    extensions = None
    env = None
    api_data_url = None


Seldom = Seldom()


class BrowserConfig:
    """
    Define run browser config
    """
    NAME = None
    REPORT_PATH = None
    REPORT_TITLE = "Seldom Test Report"
    LOG_PATH = None

    # driver config
    options = None
    command_executor = ""
    executable_path = None


def base_url():
    """return base url"""
    return Seldom.base_url


def driver():
    """return driver"""
    return Seldom.driver


class FileRunningConfig:
    """
    file runner config
    """
    api_excel_file_name = None
