import requests
from lxml import html
import ollama
from autogen import Agent

def fetch_wikipedia_content(url):
    headers = {
        'User-Agent': 'MyPythonApp/1.0 (https://example.com/my-python-app)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        paragraphs = tree.xpath('//p')
        content = ''
        for p in paragraphs:
            content += p.text_content()
        return content
    else:
        return f"Error: Unable to fetch content. Status code: {response.status_code}"
url = "https://en.wikipedia.org/wiki/Bangladesh"
content = fetch_wikipedia_content(url)
print(content)

def generate_answer(question, context):
    input_text = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    try:
        response = ollama.generate(model="codellama:7b", prompt=input_text)
        if isinstance(response, dict) and 'response' in response:
            answer = response['response']
            print("Extracted response:", answer)
            return answer.split("Answer:")[1].strip()
        else:
            print(f"Unexpected response format: {response}")
            return "No answer generated in the expected format."
    except Exception as e:
        return f"Error during generation: {str(e)}"



class QAAgent(Agent):
    def __init__(self, context):
        super().__init__()
        self.context = context

    def handle_query(self, query):
        answer = generate_answer(query, self.context)
        return answer


qa_agent = QAAgent(content)


def answer_query(agent, query):
    return agent.handle_query(query)



query = "What is the population of Bangladesh?"
response = answer_query(qa_agent, query)

print("------------------------------")
query = "What is the capital of Bangladesh?"
response = answer_query(qa_agent, query)

print("------------------------------")

query = "What is the area of Bangladesh?"
response = answer_query(qa_agent, query)