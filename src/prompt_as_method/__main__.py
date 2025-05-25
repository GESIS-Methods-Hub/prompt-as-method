from .prompt_template import PromptTemplate
from .prompt import ResponseFormat
from .llm import Ollama

llm = Ollama("http://localhost:11434/api/chat")
prompt_template = PromptTemplate(template_string="What is 1 + {{word}}? Return a JSON object with the solution")
prompt = prompt_template.render({"word": "two"})
prompt.model = "llama3.1"
prompt.max_completion_tokens = 20
prompt.response_format = ResponseFormat(
    type="json_schema",
    json_schema={
        "type": "object",
        "properties": {
            "solution": {
                "type": "integer"
            }
        },
        "required": ["solution"]
    }
)
print(llm.generate(prompt))
