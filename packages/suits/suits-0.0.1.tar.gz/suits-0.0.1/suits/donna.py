import google.generativeai as genai

class Donna:
    def __init__(self, context):
        self.context = context
        self.model = None  # Will be initialized after API key is set
        
    def credentials(self, api_key: str):
        """Set up Gemini API with your key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        return self  # This allows for method chaining
        
    def i_need_you_to(self, prompt: str):
        """Execute the given prompt on the context"""
        if not self.model:
            raise Exception("Please set up your API key first using credentials()")
            
        full_prompt = f"""
        Context: {self.context}\nTask: {prompt}

        Execute the given task on the given context object. Your final response must be only the main result, no other text or explanation is needed.
        """
        response = self.model.generate_content(full_prompt)
        return response.text