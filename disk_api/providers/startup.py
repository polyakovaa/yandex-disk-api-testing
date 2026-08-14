from typing import Callable, Optional
from dependency_injector.providers import Singleton
from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.browsers.browser_startup import BrowserServiceProvider, BrowserStartup
from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper
from browsers.extended_browser_profile import ExtendedBrowserProfile
from browsers.extended_browser_factory import ExtendedLocalBrowserFactory


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
        service_provider = super().configure_services(
            application_provider, settings, service_provider
        )
        service_provider.browser_profile.override(
            Singleton(ExtendedBrowserProfile, service_provider.settings_file)
        )
        return service_provider

    @classmethod
    def init_browser(cls):
        BrowserServices.Instance.set_startup(cls())
        service_provider = BrowserServices.Instance.service_provider
        BrowserServices.Instance.browser_factory = ExtendedLocalBrowserFactory(
            service_provider.action_retrier(),
            service_provider.browser_profile(),
            service_provider.timeout_configuration(),
            BrowserServices.Instance.localized_logger,
        )
