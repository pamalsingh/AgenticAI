"""
Pages package - Contains all Page Object Models for the test suite.
"""

from pages.base_page import BasePage
from pages.amazon_home_page import AmazonHomePage
from pages.amazon_search_results_page import AmazonSearchResultsPage

__all__ = [
    'BasePage',
    'AmazonHomePage',
    'AmazonSearchResultsPage',
]

