"""
Refactored Playwright test using Page Object Model (POM) design pattern.

Test Scenario:
1. Open http://www.amazon.in
2. Search for "T-shirts"
3. Verify that "Van Heusen" is displayed in the search results.

Design Pattern: Page Object Model (POM)
Benefits:
  - Better code organization and maintainability
  - Element locators centralized in page objects
  - Easy to update locators without changing tests
  - Reusable page objects across multiple tests
  - Clear separation of concerns
"""

import pytest
from playwright.sync_api import sync_playwright
from pages.amazon_home_page import AmazonHomePage
from pages.amazon_search_results_page import AmazonSearchResultsPage


@pytest.fixture
def browser_context():
    """Create a browser context for the test."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


def test_search_tshirts_amazon_with_pom(browser_context):
    """
    Test to verify T-shirts search on Amazon.in using Page Object Model.
    
    Steps:
    1. Open http://www.amazon.in
    2. Search for "T-shirts"
    3. Verify that "Van Heusen" is displayed in the search results.
    
    Uses Page Objects:
    - AmazonHomePage: Handles home page interactions
    - AmazonSearchResultsPage: Handles search results page interactions
    """
    page = browser_context.new_page()
    
    # Initialize page objects
    home_page = AmazonHomePage(page)
    search_results_page = AmazonSearchResultsPage(page)
    
    # ======== STEP 1: Open Amazon.in ========
    print("\n" + "="*60)
    print("STEP 1: Opening http://www.amazon.in")
    print("="*60)
    
    try:
        home_page.open()
        
        # Verify page is loaded
        assert home_page.is_page_loaded(), "Home page did not load properly"
        
        print(f"✓ Page loaded successfully")
        print(f"  URL: {home_page.get_current_url()}")
        print(f"  Title: {home_page.get_page_title()}")
        
    except Exception as e:
        print(f"✗ Failed to load page: {e}")
        home_page.take_screenshot("home_page_failure.png")
        page.close()
        raise
    
    # ======== STEP 2: Search for "T-shirts" ========
    print("\n" + "="*60)
    print("STEP 2: Searching for 'T-shirts'")
    print("="*60)
    
    try:
        search_term = "T-shirts"
        
        # Use home page to search
        home_page.search_for_product(search_term)
        print(f"✓ Entered '{search_term}' and submitted search")
        
        # Verify we're on search results page
        assert search_results_page.is_results_page_loaded(), "Search results page did not load"
        print("✓ Search results page loaded")
        print(f"  Results URL: {search_results_page.get_page_url()}")
        
        # Get results count
        results_count = search_results_page.get_results_count()
        print(f"  Found {results_count} search result items")
        
    except Exception as e:
        print(f"✗ Search failed: {e}")
        home_page.take_screenshot("search_failure.png")
        page.close()
        raise
    
    # ======== STEP 3: Verify "Van Heusen" in results ========
    print("\n" + "="*60)
    print("STEP 3: Verifying 'Van Heusen' in search results")
    print("="*60)
    
    try:
        brand_name = "Van Heusen"
        
        # Check if brand is in results
        is_brand_found = search_results_page.is_brand_in_results(brand_name)
        
        if is_brand_found:
            print(f"✓ '{brand_name}' found in search results!")
            
            # Get count of brand products
            brand_count = search_results_page.get_brand_products_count(brand_name)
            print(f"✓ Found {brand_count} {brand_name} product(s)")
            
            # Get first brand product text
            first_product = search_results_page.get_first_brand_product_text(brand_name)
            print(f"  First result: {first_product[:100]}")
            
            # Get all results for detailed view
            all_results = search_results_page.get_all_results_text(limit=3)
            print(f"\n  Top {len(all_results)} results:")
            for i, result in enumerate(all_results, 1):
                preview = result[:80].replace('\n', ' ')
                print(f"    {i}. {preview}...")
            
            # Take screenshot
            search_results_page.take_screenshot("search_results_success.png")
            print("\n✓ Screenshot saved: search_results_success.png")
            
            # Assert the brand is found
            assert brand_count > 0, f"{brand_name} not found in search results"
            print(f"\n✓✓✓ TEST PASSED: {brand_name} found in search results! ✓✓✓\n")
        else:
            print(f"✗ '{brand_name}' NOT found in search results")
            search_results_page.take_screenshot("search_results_failure.png")
            raise AssertionError(f"{brand_name} not found in search results")
            
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        page.close()
        raise
    
    page.close()
    print("="*60)
    print("TEST COMPLETED SUCCESSFULLY")
    print("="*60 + "\n")


def test_search_multiple_products_with_pom(browser_context):
    """
    Additional test demonstrating POM flexibility.
    Search for multiple products and verify results.
    """
    page = browser_context.new_page()
    
    # Initialize page objects
    home_page = AmazonHomePage(page)
    search_results_page = AmazonSearchResultsPage(page)
    
    print("\n" + "="*60)
    print("TEST: Multi-Product Search with POM")
    print("="*60)
    
    try:
        # Open home page
        home_page.open()
        assert home_page.is_page_loaded()
        print("✓ Home page loaded")
        
        # Test multiple searches
        search_terms = [
            ("T-shirts", "Van Heusen"),
            ("Watches", "Titan"),
            ("Books", "Penguin"),
        ]
        
        for search_term, brand in search_terms:
            print(f"\n📍 Searching for '{search_term}' and verifying '{brand}'")
            
            # Perform search
            home_page.search_for_product(search_term)
            
            # Check results
            if search_results_page.is_results_page_loaded():
                count = search_results_page.get_results_count()
                print(f"  ✓ Found {count} results")
                
                # Check for brand
                if search_results_page.is_brand_in_results(brand):
                    brand_count = search_results_page.get_brand_products_count(brand)
                    print(f"  ✓ {brand} found in {brand_count} product(s)")
                else:
                    print(f"  ⚠ {brand} not found in results")
            else:
                print(f"  ✗ Results page did not load")
        
        print(f"\n✓ Multi-product search test completed successfully\n")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        page.close()
        raise
    
    page.close()


if __name__ == "__main__":
    # Run with: python -m pytest AI/Search_product_pom.py -v -s
    pytest.main([__file__, "-v", "-s"])

