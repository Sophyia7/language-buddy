import google.generativeai as genai 


# Gemini Configuration
generation_config = {
  "temperature": 0.7,
  "top_p": 0.8,
  "top_k": 40,
  "max_output_tokens": 1024,
}

# Safety settings - set to low to allow language learning content
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# Initialize model configuration
model_config = {
    'model_name': 'gemini-pro',
    'generation_config': generation_config,
    'safety_settings': safety_settings,
}


# Export configurations
__all__ = ['generation_config', 'safety_settings', 'model_config']