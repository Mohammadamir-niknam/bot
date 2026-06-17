from pydantic import SecretStr
from config import Settings

def test_proxy_urls_are_ordered_and_trimmed():
    settings = Settings(bot_token=SecretStr("123456789:abcdefghijklmnopqrstuvwxyz"), proxy_url_1="https://one/", proxy_url_2="", proxy_url_3="https://three/")
    assert settings.proxy_urls == ("https://one", "https://three")
