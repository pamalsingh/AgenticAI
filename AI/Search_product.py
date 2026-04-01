"""
Playwright test for Amazon.in T-shirts search.

Test Scenario:
1. Open http://www.amazon.in
2. Search for "T-shirts"
3. Verify that "Van Heusen" is displayed in the search results.

Implementation: pytest-style with Playwright
"""

import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.fixture
def browser_context():
    """Create a browser context for the test."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


def test_search_tshirts_amazon(browser_context):
    """
    Test to verify T-shirts search on Amazon.in and check for Van Heusen brand.
    
    Steps:
    1. Open http://www.amazon.in
    2. Search for "T-shirts"
    3. Verify that "Van Heusen" is displayed in the search results.
    """
    page = browser_context.new_page()
    
    # Step 1: Open http://www.amazon.in
    print("\n" + "="*60)
    print("STEP 1: Opening http://www.amazon.in")
    print("="*60)
    
    try:
        page.goto("http://www.amazon.in", wait_until="domcontentloaded", timeout=30000)
        
        # Amazon has persistent background requests, so we wait for load instead of networkidle
        page.wait_for_timeout(3000)  # Wait for initial content to render
        
        print(f"✓ Page loaded successfully")
        print(f"  URL: {page.url}")
        print(f"  Title: {page.title()}")
    except Exception as e:
        print(f"✗ Failed to load page: {e}")
        page.close()
        raise
    
    # Step 2: Search for "T-shirts"
    print("\n" + "="*60)
    print("STEP 2: Searching for 'T-shirts'")
    print("="*60)
    
    try:
        # Find the search input - Amazon uses id='twotabsearchtextbox'
        search_input = page.locator("input#twotabsearchtextbox")
        
        # Wait for the search box to be visible
        search_input.wait_for(timeout=10000)
        print("✓ Search input found")
        
        # Type "T-shirts"
        search_input.fill("T-shirts")
        print("✓ Entered 'T-shirts' in search box")
        
        # Press Enter to search
        search_input.press("Enter")
        
        # Wait for search results to load - use load state instead of networkidle
        page.wait_for_timeout(5000)  # Wait for results to render
        print("✓ Search results loaded")
        print(f"  Results URL: {page.url}")
        
    except Exception as e:
        print(f"✗ Search failed: {e}")
        # Take a screenshot for debugging
        page.screenshot(path="search_failure.png")
        page.close()
        raise
    
    # Step 3: Verify "Van Heusen" is displayed in search results
    print("\n" + "="*60)
    print("STEP 3: Verifying 'Van Heusen' in search results")
    print("="*60)
    
    try:
        # Wait a moment for the page to fully render
        page.wait_for_timeout(2000)
        
        # Get the page content to search for Van Heusen
        content = page.content().lower()
        
        if "van heusen" in content:
            print("✓ 'Van Heusen' found in page content!")
            
            # Try to find the product link/element
            van_heusen_elements = page.locator("text=/van heusen/i").all()
            
            if van_heusen_elements:
                print(f"✓ Found {len(van_heusen_elements)} Van Heusen product(s)")
                
                # Get text from first match
                first_element_text = van_heusen_elements[0].inner_text()
                print(f"  First result: {first_element_text[:100]}")
                
                # Take a screenshot showing the results
                page.screenshot(path="search_results_success.png")
                print("\n✓ Screenshot saved: search_results_success.png")
                
                assert "van heusen" in first_element_text.lower(), "Van Heusen not in first result"
                print("\n✓✓✓ TEST PASSED: Van Heusen found in search results! ✓✓✓\n")
            else:
                # Alternative: search in the results area
                results_area = page.locator("[data-component-type='s-search-result']")
                print(f"✓ Found {results_area.count()} search result items")
                
                # Check each result for Van Heusen
                for i in range(min(5, results_area.count())):
                    result_text = results_area.nth(i).inner_text()
                    if "van heusen" in result_text.lower():
                        print(f"✓ Van Heusen found in result #{i+1}")
                        print(f"  {result_text[:150]}")
                        page.screenshot(path="search_results_success.png")
                        assert True
                        print("\n✓✓✓ TEST PASSED: Van Heusen found in search results! ✓✓✓\n")
                        return
                
                # If we still don't find it in structured results, check the full page
                print("⚠ Checking full page content for Van Heusen...")
                assert "van heusen" in content, "Van Heusen not found in search results"
                page.screenshot(path="search_results_success.png")
                print("\n✓✓✓ TEST PASSED: Van Heusen found in search results! ✓✓✓\n")
        else:
            print("✗ 'Van Heusen' NOT found in page content")
            print("\nDebug info:")
            print(f"  Page URL: {page.url}")
            print(f"  Page title: {page.title()}")
            
            # Take a screenshot for debugging
            page.screenshot(path="search_results_failure.png")
            print("  Screenshot saved: search_results_failure.png")
            
            # List available brands in results
            results_area = page.locator("[data-component-type='s-search-result']")
            if results_area.count() > 0:
                print(f"\n  Found {results_area.count()} results. Brands visible:")
                for i in range(min(5, results_area.count())):
                    result_text = results_area.nth(i).inner_text()
                    print(f"    Result {i+1}: {result_text[:120]}")
            
            raise AssertionError("Van Heusen not found in search results")
            
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        page.close()
        raise
    
    page.close()
    print("\n" + "="*60)
    print("TEST COMPLETED SUCCESSFULLY")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Run with: python -m pytest AI/Search_product.py -v -s
    pytest.main([__file__, "-v", "-s"])

