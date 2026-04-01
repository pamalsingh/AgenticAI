"""
Amazon Home Page Object.
Contains all locators and methods specific to Amazon's home page.
"""

from pages.base_page import BasePage


class AmazonHomePage(BasePage):
    """
    Page Object for Amazon.in home page.
    Manages all interactions with the home page elements.
    """
    
    # Locators
    SEARCH_INPUT = "input#twotabsearchtextbox"
    SEARCH_BUTTON = "button[type='submit']"
    PAGE_TITLE_EXPECTED = "Online Shopping site in India"
    
    def __init__(self, page):
        """
        Initialize Amazon home page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        self.base_url = "http://www.amazon.in"
    
    def open(self):
        """
        Open Amazon.in home page.
        """
        self.goto(self.base_url)
        # Wait for initial content to render
        self.wait_for_timeout(3000)
    
    def is_page_loaded(self) -> bool:
        """
        Verify that the home page is loaded.
        
        Returns:
            True if page is loaded, False otherwise
        """
        try:
            self.page.locator(self.SEARCH_INPUT).wait_for(timeout=10000)
            return True
        except:
            return False
    
    def search_for_product(self, search_term: str):
        """
        Search for a product on Amazon.
        
        Args:
            search_term: Product to search for
        """
        # Enter search term
        self.fill_input(self.SEARCH_INPUT, search_term)
        
        # Press Enter to search
        self.press_key(self.SEARCH_INPUT, "Enter")
        
        # Wait for results to load
        self.wait_for_timeout(5000)
    
    def get_page_title(self) -> str:
        """
        Get the home page title.
        
        Returns:
            Page title
        """
        return self.page.title()
    
    def get_current_url(self) -> str:
        """
        Get the current URL.
        
        Returns:
            Current URL
        """
        return self.page.url

