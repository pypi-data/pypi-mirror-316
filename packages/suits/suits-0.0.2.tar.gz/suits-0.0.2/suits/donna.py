import google.generativeai as genai
from ast import literal_eval
import shutup
shutup.please()

class Donna:
    def __init__(self, context):
        self.context = context
        self.model = None
        
    def briefing(self, api_key: str, temperature: float=0.2):
        """Set up Gemini API with your key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash", 
                                         generation_config=genai.GenerationConfig(
                                             temperature=temperature))
        return self
        
    def i_need_you_to(self, prompt: str, output_config: type=None, reasoning: bool=False):
        """Execute the given prompt on the context"""
        if not self.model:
            raise Exception("Please set up your API key first using briefing()")
            
        if output_config and reasoning:
            raise ValueError("Cannot use Reasoning Mode with Structured Mode.")

        full_prompt = f"""
        Context: {self.context}\nTask: {prompt}

        Execute the given task on the given context object. Your final response must be only the main result, no other text or explanation is needed.
        If given any specific format or configuration for your final response, do follow the same.
        """

        reasoning_prompt = f"""
        YOUR PERSONA: You are an AI system capable of complex reasoning and self reflection. Reason through the query inside <thinking> tags, and then provide your
        final response inside <output> tags. If you detect that you made mistake in your reasoning at any point, correct yourself inside <reflection>
        tags.

        YOUR JOB: Execute the given task on the given context object. If given any specific format or configuration for your final response, do follow the same.

        GIVEN CONTEXT OBJECT: {self.context}

        GIVEN TASK: {prompt}
        """

        try:
            if output_config:
                conf = genai.GenerationConfig(response_mime_type="application/json", 
                                            response_schema=output_config)
                res = self.model.generate_content(full_prompt, generation_config=conf).text
                return literal_eval(res)
            
            elif reasoning:
                return self.model.generate_content(reasoning_prompt).text
            
            else:
                return self.model.generate_content(full_prompt).text
                
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")