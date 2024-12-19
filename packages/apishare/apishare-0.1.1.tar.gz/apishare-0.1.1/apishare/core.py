import httpx

class APIShare:
    """Main class for API sharing functionality"""
    
    def __init__(self):
        """Initialize APIShare instance"""
        self.client = httpx.Client()
    
    def get(self, url: str, **kwargs) -> httpx.Response:
        """Send GET request to specified URL
        
        Args:
            url (str): The URL to send request to
            **kwargs: Additional arguments to pass to httpx.get
            
        Returns:
            httpx.Response: The response from the server
        """
        return self.client.get(url, **kwargs)
    
    def post(self, url: str, **kwargs) -> httpx.Response:
        """Send POST request to specified URL
        
        Args:
            url (str): The URL to send request to
            **kwargs: Additional arguments to pass to httpx.post
            
        Returns:
            httpx.Response: The response from the server
        """
        return self.client.post(url, **kwargs)
    
    def __del__(self):
        """Clean up resources"""
        self.client.close()
