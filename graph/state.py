from typing import List, TypedDict
from pydantic import BaseModel, Field

class GraphState(BaseModel):
    """
    Represents the state of our graph.
    """
    question: str = Field(description="question")
    generation: str = Field(description="LLM generation")
    web_search: bool = Field(description="whether to add search")
    documents: List[str] = Field(description="list of documents")
