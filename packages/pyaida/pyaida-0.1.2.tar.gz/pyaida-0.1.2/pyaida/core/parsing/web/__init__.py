
from . providers import PROVIDERS, ResourceParseBase
from urllib.parse import urlparse

def get_provider(url:str):
    """determine if we have a custom provider for the url"""
    
    return PROVIDERS.get(urlparse(url).netloc, ResourceParseBase())


def get_resource_data(url:str, custom_provider:ResourceParseBase=None):
    """look for a url specific provider or use the default"""
    provider = custom_provider or get_provider(url)
    return provider(url)