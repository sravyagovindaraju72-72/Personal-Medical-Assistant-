import urllib.parse

def generate_amazon_link(product_name: str) -> str:
    """
    Generates an Amazon search URL for a given product name.
    
    Args:
        product_name: Name of the product (e.g., "Ginger Tea")
        
    Returns:
        Amazon search URL string
    """
    
    if not product_name or not product_name.strip():
        return "https://www.amazon.com"
    
    # Clean the product name
    cleaned_name = product_name.strip()
    
    # URL encode the product name (handles spaces, special characters)
    encoded_name = urllib.parse.quote_plus(cleaned_name)
    
    # Construct Amazon search URL
    amazon_url = f"https://www.amazon.com/s?k={encoded_name}"
    
    return amazon_url


def add_amazon_links_to_recommendations(recommendations: dict) -> dict:
    """
    Adds Amazon search links to each recommendation item.
    
    Args:
        recommendations: Dict with teas, medications, exercises, products
        
    Returns:
        Same dict with 'amazon_link' added to each item
    """
    
    # Add links to teas
    if 'teas' in recommendations and isinstance(recommendations['teas'], list):
        for tea in recommendations['teas']:
            if 'name' in tea:
                tea['amazon_link'] = generate_amazon_link(tea['name'])
    
    # Add links to medications
    if 'medications' in recommendations and isinstance(recommendations['medications'], list):
        for med in recommendations['medications']:
            if 'name' in med:
                med['amazon_link'] = generate_amazon_link(med['name'])
    
    # Add links to exercises (generally don't need Amazon links, but include for consistency)
    if 'exercises' in recommendations and isinstance(recommendations['exercises'], list):
        for exercise in recommendations['exercises']:
            if 'name' in exercise:
                # For exercises, we might not want Amazon links, but include empty or skip
                exercise['amazon_link'] = ''  # or could generate based on equipment needed
    
    # Add links to products
    if 'products' in recommendations and isinstance(recommendations['products'], list):
        for product in recommendations['products']:
            if 'name' in product:
                product['amazon_link'] = generate_amazon_link(product['name'])
    
    return recommendations