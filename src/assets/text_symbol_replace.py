import re

def clean_text_to_underscore(text):
    """
    Remove text symbols and spaces, replace with underscores.
    Convert all letters to lowercase and add underscore before numbers after words.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text with underscores replacing symbols and spaces
        
    Example:
        Input: "400 million years ago, it was the ocean, and 400 million years later, it is the desert1"
        Output: "400_million_years_ago_it_was_the_ocean_and_400_million_years_later_it_is_the_desert_1"
    """
    # Convert to lowercase first
    cleaned = text.lower()
    
    # Add underscore before numbers that come after letters/words
    cleaned = re.sub(r'([a-zA-Z])(\d)', r'\1_\2', cleaned)
    
    # Remove all non-alphanumeric characters except spaces
    # Replace spaces and multiple consecutive non-alphanumeric chars with single underscore
    cleaned = re.sub(r'[^a-zA-Z0-9\s]+', '_', cleaned)
    
    # Replace spaces with underscores
    cleaned = re.sub(r'\s+', '_', cleaned)
    
    # Remove multiple consecutive underscores and replace with single underscore
    cleaned = re.sub(r'_+', '_', cleaned)
    
    # Remove leading and trailing underscores
    cleaned = cleaned.strip('_')
    
    return cleaned

def clean_text_to_underscore_advanced(text):
    """
    Advanced version that handles more edge cases.
    Convert all letters to lowercase and add underscore before numbers after words.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text with underscores replacing symbols and spaces
    """
    # Convert to lowercase first
    cleaned = text.lower()
    
    # Add underscore before numbers that come after letters/words
    cleaned = re.sub(r'([a-zA-Z])(\d)', r'\1_\2', cleaned)
    
    # Replace all non-alphanumeric characters with underscores
    cleaned = re.sub(r'[^a-zA-Z0-9]', '_', cleaned)
    
    # Remove multiple consecutive underscores
    cleaned = re.sub(r'_+', '_', cleaned)
    
    # Remove leading and trailing underscores
    cleaned = cleaned.strip('_')
    
    return cleaned

# Example usage
if __name__ == "__main__":
    # Test the function
    test_text = "400 million years ago, it was the ocean, and 400 million years later, it is the desert1"
    
    print("Original text:")
    print(test_text)
    print("\nCleaned text:")
    print(clean_text_to_underscore(test_text))
    
    print("\nAdvanced cleaned text:")
    print(clean_text_to_underscore_advanced(test_text))
    
    # Additional test cases
    test_cases = [
        "Hello, World! How are you?",
        "File@Name#123$%^&*()",
        "Multiple    spaces   here",
        "Special@#$%Characters!!!",
        "Numbers123 and Text456",
        "My Vacation Photo (2023).jpg",
        "Document@#$%Final.pdf",
        "A Bite of the Moon1.jpg",
        "SOLO EXHIBITION- Hotel Smoke and Ash2.JPG",
        "The Cambrian Period5.JPG"
    ]
    
    print("\nAdditional test cases:")
    for test in test_cases:
        print(f"'{test}' -> '{clean_text_to_underscore(test)}'")
