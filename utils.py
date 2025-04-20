import os
from llama_index.llms.groq import Groq
from llama_index.core.prompts import PromptTemplate


def load_llm(api_key: str = None):
    return Groq(
        model="llama3-8b-8192",
        api_key=api_key or os.getenv("GROQ_API_KEY"),
        temperature=0.3,
    )


# Relevance scoring prompt (score-based, clean)
RELEVANCY_PROMPT = PromptTemplate(
    template="""As a grader, give a **numeric relevance score** (from 0 to 1) to the document for the given user query.

Document:
---------
{context_str}

User Query:
-----------
{query_str}

Instructions:
- 0 means completely irrelevant, 1 means fully relevant
- Only return the score (e.g., 0.75)
"""
)

# Query refining for web search
REFINE_PROMPT = PromptTemplate(
    template="""Your task is to refine a query to ensure it is highly effective for retrieving relevant search results. 
Analyze the given input to grasp the core semantic intent or meaning.

Original Query:
---------------
{query_str}

Your goal is to rephrase or enhance this query to improve its search performance. 
Respond with the optimized query only.
"""
)
