from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, \
    ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def get_verifier_chain():
    system_template = (
        "You are an assistant that checks whether a user's answer matches the correct answer. "
        "Return only a JSON object with only one field: 'is_correct' (boolean)."
    )

    human_template = (
        "Question: {question}\n"
        "Correct Answer: {correct_answer}\n"
        "User's Answer: {user_answer}\n"
        "Determine if the user's answer matches the correct answer, allowing for minor typos or variations."
    )
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ])
    return prompt | llm


verifier_chain = get_verifier_chain()
