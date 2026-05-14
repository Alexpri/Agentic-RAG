from typing import List

from langchain_core.documents import Document
from pydantic import BaseModel, Field

class GraphState(BaseModel):
    """
    Represents the state of our graph.
    """
    question: str = Field(description="question")
    generation: str = Field(default="", description="LLM generation")
    web_search: bool = Field(default=False, description="whether to add search")
    documents: List[Document] = Field(
        default_factory=list, description="list of documents"
    )