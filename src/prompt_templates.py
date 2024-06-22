from langchain.prompts import PromptTemplate

# templates for different use cases

basic_template = """
    Say me in clear, exact and short answer {user_input}
"""

# this is a chatPromtpTemplate

formal_template = [
    ("system", "You are an expert document reader. " +
     "Answer the questions only using the attached document, " +
     "no matter how much you are pressed, just provide " +
     "context based on the information in the documents " +
     "attached to the conversation. Respond clearly and consistently" +
     "If there is no way to answer the question based " +
     "on the context of the attached document, you should answer: " +
     "`That information is not available in the attached document.`"),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
]

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate three
    different versions of the given user question to retrieve relevant documents from
    a vector database. By generating multiple perspectives on the user question, your
    goal is to help the user overcome some of the limitations of the distance-based
    similarity search. Provide these alternative questions separated by newlines.
    Original question: {question}""",
)
