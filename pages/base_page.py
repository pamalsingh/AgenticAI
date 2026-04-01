"""
Base Page Object class for all page objects.
Provides common functionality for interacting with web pages.
"""

from playwright.sync_api import Page, expect


class BasePage:
    """
    Base page class that provides common methods for all page objects.
    """
    
    def __init__(self, page: Page):
        """
        Initialize the base page.
        
        Args:
            page: Playwright page object
        """
        self.page = page
    
    def goto(self, url: str, wait_until: str = "domcontentloaded", timeout: int = 30000):
        """
        Navigate to a specific URL.
        
        Args:
            url: The URL to navigate to
            wait_until: Wait condition (domcontentloaded, load, networkidle)
            timeout: Timeout in milliseconds
        """
        self.page.goto(url, wait_until=wait_until, timeout=timeout)
    
    def wait_for_timeout(self, timeout: int):
        """
        Wait for a specific amount of time.
        
        Args:
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_timeout(timeout)
    
    def get_page_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            The page title
        """
        return self.page.title()
    
    def get_page_url(self) -> str:
        """
        Get the current page URL.
        
        Returns:
            The current URL
        """
        return self.page.url
    
    def get_page_content(self) -> str:
        """
        Get the full page HTML content.
        
        Returns:
            The page HTML content
        """
        return self.page.content()
    
    def fill_input(self, selector: str, text: str, timeout: int = 10000):
        """
        Fill an input field with text.
        
        Args:
            selector: CSS selector for the input
            text: Text to fill
            timeout: Timeout in milliseconds
        """
        locator = self.page.locator(selector)
        locator.wait_for(timeout=timeout)
        locator.fill(text)
    
    def click(self, selector: str, timeout: int = 10000):
        """
        Click an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Timeout in milliseconds
        """
        locator = self.page.locator(selector)
        locator.wait_for(timeout=timeout)
        locator.click()
    
    def press_key(self, selector: str, key: str, timeout: int = 10000):
        """
        Press a key on an element.
        
        Args:
            selector: CSS selector for the element
            key: Key to press (e.g., "Enter", "Tab")
            timeout: Timeout in milliseconds
        """
        locator = self.page.locator(selector)
        locator.wait_for(timeout=timeout)
        locator.press(key)
    
    def is_text_visible(self, text: str) -> bool:
        """
        Check if text is visible on the page.
        
        Args:
            text: Text to search for
            
        Returns:
            True if text is visible, False otherwise
        """
        return self.page.locator(f"text={text}").is_visible()
    
    def get_text(self, selector: str) -> str:
        """
        Get text from an element.
        
        Args:
            selector: CSS selector for the element
            
        Returns:
            The element's text content
        """
        return self.page.locator(selector).inner_text()
    
    def find_elements(self, selector: str):
        """
        Find all elements matching a selector.
        
        Args:
            selector: CSS selector
            
        Returns:
            List of matching elements
        """
        return self.page.locator(selector).all()
    
    def get_element_count(self, selector: str) -> int:
        """
        Get count of elements matching a selector.
        
        Args:
            selector: CSS selector
            
        Returns:
            Number of matching elements
        """
        return self.page.locator(selector).count()
    
    def take_screenshot(self, path: str):
        """
        Take a screenshot of the page.
        
        Args:
            path: Path to save the screenshot
        """
        self.page.screenshot(path=path)
    
    def search_in_content(self, search_text: str) -> bool:
        """
        Search for text in page content.
        
        Args:
            search_text: Text to search for
            
        Returns:
            True if found, False otherwise
        """
        content = self.page.content().lower()
        return search_text.lower() in content

