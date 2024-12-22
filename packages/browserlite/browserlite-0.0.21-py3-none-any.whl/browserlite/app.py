from typing import Literal

from .core.automation import AutomationManager,SearchServiceType

BrowserType = Literal[
    'google-chrome',
    'microsoft-edge-stable',
    'firefox'
]


def browse(
    query,
    service_name: SearchServiceType = "google",
    browser: BrowserType = 'microsoft-edge-stable',
    base_url="http://www.google.com/"
):
    manager = AutomationManager()
    result = manager.execute_search(
        query=query,
        service_name=service_name,
        browser=browser,
        base_url=base_url
    )
    return result


def chatgpt(query):
    return browse(
        query,
        service_name="chatgpt",
        base_url="http://www.chatgpt.com/"
    )
def huggingchat(query):
    return browse(
        query,
        service_name="huggingchat",
        base_url="https://huggingface.co/chat/"
    )