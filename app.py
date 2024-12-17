from flask import Flask, render_template, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import GEMINI_API_KEY

app = Flask(__name__)


prompt = open('pdf-text.txt', 'r', encoding='utf-8').read()
# print(prompt)


study_assistant_template= prompt + """
You are a study assistant. Your name is Sam.
Your expertise is exclusively in providing information and advice about anything related to content of the prompt. 
This includes any questions and related content in the provided text.
You do not provide information outside of this scope. 
If a question is not about the content of the text, respond with, "I can't assist you with that, sorry!" 
Question: {question} 
Answer: 
"""

# Initialize the PromptTemplate
study_assistant_prompt_template = PromptTemplate.from_template(study_assistant_template)

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, api_key=GEMINI_API_KEY)

# Chain the template with the LLM
# llm_chain = LLMChain(prompt=study_assistant_prompt_template, llm=llm)
llm_chain = study_assistant_prompt_template | llm 


def query_llm(question): 
    llm_response = llm_chain.invoke({'question': question})
    if hasattr(llm_response, 'content'):
        response = llm_response.content
    else:
        response = str(llm_response) 
    return response

@app.route("/") 
def index(): 
    return render_template("home.html") 



@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        question = request.json.get('question', '')
                
        if not question.strip():
            return jsonify({'error': 'Question is required'}), 400
        response = query_llm(question) 
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': 'An internal error occurred'}), 500


if __name__ == "__main__": 
    app.run(debug=True)