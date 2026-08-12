from typing import Callable, Optional
from py_selenium_auto.browsers.browser_startup import BrowserServiceProvider, BrowserStartup
from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper


class Startup(BrowserStartup):

    @classmethod
    def configure_services(
        cls,
        application_provider: Callable,
        settings: Optional[JsonSettingsFile] = None,
        service_provider: BrowserServiceProvider = None,
    ) -> BrowserServiceProvider:
        settings = settings or cls.get_settings(
            RootPathHelper.calling_root_path(),
            RootPathHelper.current_root_path(__file__),
        )
        return super().configure_services(application_provider, settings, service_provider)
