import httpx

class APIShare:
    def __init__(self, token):
        self.token = token
    
    def test(self):
        return self.token
