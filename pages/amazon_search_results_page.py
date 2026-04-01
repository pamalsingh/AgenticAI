"""
Amazon Search Results Page Object.
Contains all locators and methods specific to Amazon's search results page.
"""

from pages.base_page import BasePage


class AmazonSearchResultsPage(BasePage):
    """
    Page Object for Amazon.in search results page.
    Manages all interactions with search results elements.
    """
    
    # Locators
    SEARCH_RESULTS = "[data-component-type='s-search-result']"
    PRODUCT_TITLE = "h2 a span"
    RESULTS_CONTAINER = "div[data-search-results-container]"
    
    def __init__(self, page):
        """
        Initialize Amazon search results page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
    
    def is_results_page_loaded(self) -> bool:
        """
        Verify that the search results page is loaded.
        
        Returns:
            True if results page is loaded, False otherwise
        """
        # Check if we have search results
        return self.get_element_count(self.SEARCH_RESULTS) > 0
    
    def get_results_count(self) -> int:
        """
        Get the number of search results displayed.
        
        Returns:
            Count of search result items
        """
        return self.get_element_count(self.SEARCH_RESULTS)
    
    def get_result_text_by_index(self, index: int) -> str:
        """
        Get text content of a specific search result.
        
        Args:
            index: Index of the result (0-based)
            
        Returns:
            Text content of the result
        """
        results = self.find_elements(self.SEARCH_RESULTS)
        if index < len(results):
            return results[index].inner_text()
        return ""
    
    def get_all_results_text(self, limit: int = 5) -> list:
        """
        Get text content of multiple search results.
        
        Args:
            limit: Maximum number of results to retrieve
            
        Returns:
            List of result texts
        """
        results = []
        elements = self.find_elements(self.SEARCH_RESULTS)
        
        for i in range(min(limit, len(elements))):
            results.append(elements[i].inner_text())
        
        return results
    
    def is_brand_in_results(self, brand_name: str) -> bool:
        """
        Check if a specific brand is present in search results.
        
        Args:
            brand_name: Brand name to search for
            
        Returns:
            True if brand is found, False otherwise
        """
        # First check in page content
        if self.search_in_content(brand_name):
            return True
        return False
    
    def get_brand_products_count(self, brand_name: str) -> int:
        """
        Count how many products of a specific brand are in results.
        
        Args:
            brand_name: Brand name to count
            
        Returns:
            Count of products from this brand
        """
        results = self.find_elements(self.SEARCH_RESULTS)
        count = 0
        
        for result in results:
            if brand_name.lower() in result.inner_text().lower():
                count += 1
        
        return count
    
    def get_first_brand_product_text(self, brand_name: str) -> str:
        """
        Get the text of the first product of a specific brand.
        
        Args:
            brand_name: Brand name to search for
            
        Returns:
            Text content of first matching product
        """
        results = self.find_elements(self.SEARCH_RESULTS)
        
        for result in results:
            result_text = result.inner_text()
            if brand_name.lower() in result_text.lower():
                return result_text
        
        return ""
    
    def get_page_url(self) -> str:
        """
        Get the current search results page URL.
        
        Returns:
            Current URL
        """
        return self.page.url
    
    def get_search_query_from_url(self) -> str:
        """
        Extract search query from the URL.
        
        Returns:
            Search query parameter value
        """
        url = self.page.url
        if "k=" in url:
            return url.split("k=")[1].split("&")[0].replace("+", " ")
        return ""

