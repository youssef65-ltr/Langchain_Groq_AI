from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate , PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
import json
from dotenv import load_dotenv

load_dotenv()

        
# 1 ) LLM setup :
LLM = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    max_tokens=2000,
    temperature=0.7
)

quiz_prompt = PromptTemplate(
    input_variables=["context" , "num_quizs"],
    template="""
you are an smart AI assistant the user generate Quizs from the text below as a JSON form :
Text : 
{context}
Return ONLY a valid JSON array.
Generate {num_quizs} Quizs as a list of dictionaries like this form below :
[{{
    "id": "unique id",
    "question": "...",
    "choices":four answers ["choise1", "choise2", "choise3", "choise4"],
    "correct_answer": index of the correct choices,
    "explanation": "short explanation",
    "difficulty": "easy | medium | hard",
    "topic": "topic of the quiz"
}},...]

Rules:
- Always generate 4 choices
- correct_answer must be the index (0-3)
- Do not add text outside JSON
- JSON must be valid

"""
)


# 2 ) Create a chain using LCEL syntax that means
#                1      =>  2   =>      3
quiz_chain = quiz_prompt | LLM | StrOutputParser()


# 3 ) tools
@tool
def generate_quizzes( context : str , num_quizs : int ) :
    """
    Generate quizzes from a given text.
    """
    response = quiz_chain.invoke({
        "context": context,
        "num_quizs": num_quizs
    })
    # exception if the the json is not valid
    try:
        return json.loads(response)
    except:
        return {
            "error": "AI returned invalid JSON",
            "raw_output": response
        }


#  ==========================================================================================================================
# # Define a prompt template
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant. Be concise."),
#     ("human", "{input}")
# ])

# # Create a chain using LCEL syntax
# chain = prompt | LLM | StrOutputParser()

# # Invoke the chain with an input
# response = chain.invoke({"input": "Explain the benefit of combining LangChain and Groq."})
# print(response)
#  ==========================================================================================================================





text = """
HTTP methods, also known as HTTP verbs, define the desired action to be performed on a specific resource identified by a URL. The most commonly used methods in web development, especially for RESTful APIs (Representational State Transfer APIs), are GET, POST, PUT, PATCH, and DELETE, which correspond to the basic CRUD operations (Create, Read, Update, Delete).
"""
    # the result :
quizzes = generate_quizzes.invoke({
        "context": text,
        "num_quizs": 1
    })
print(quizzes)

