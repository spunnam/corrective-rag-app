import os
from typing import Optional, Any, List
from dotenv import load_dotenv
from llama_index.core import SummaryIndex, Document
from llama_index.core.workflow import (
    Workflow,
    step,
    Context,
    StartEvent,
    StopEvent,
    Event,
)
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.schema import NodeWithScore
from llama_index.tools.linkup_research.base import LinkupToolSpec
from core.utils import RELEVANCY_PROMPT, REFINE_PROMPT

load_dotenv()


class RetrieveEvent(Event):
    retrieved_nodes: List[NodeWithScore]


class WebSearchEvent(Event):
    relevant_text: str


class QueryEvent(Event):
    relevant_text: str
    search_text: str


class CorrectiveRAGWorkflow(Workflow):
    def __init__(
        self, index, llm, verbose: bool = True, timeout: int = 60, **kwargs: Any
    ) -> None:
        super().__init__(verbose=verbose, timeout=timeout, **kwargs)
        self.index = index
        self.llm = llm
        self.linkup_tool = LinkupToolSpec(
            api_key=os.environ["LINKUP_API_KEY"],
            depth="deep",
            output_type="searchResults",
        )

    @step
    async def retrieve(self, ctx: Context, ev: StartEvent) -> Optional[RetrieveEvent]:
        query_str = ev.get("query_str")
        retriever_kwargs = ev.get("retriever_kwargs", {})

        if query_str is None:
            return None

        retriever: BaseRetriever = self.index.as_retriever(**retriever_kwargs)
        result = retriever.retrieve(query_str)
        await ctx.set("retrieved_nodes", result)
        await ctx.set("query_str", query_str)
        return RetrieveEvent(retrieved_nodes=result)

    @step
    async def eval_relevance(
        self, ctx: Context, ev: RetrieveEvent
    ) -> WebSearchEvent | QueryEvent:
        retrieved_nodes = ev.retrieved_nodes
        query_str = await ctx.get("query_str")

        relevant_texts = []
        for node in retrieved_nodes:
            prompt = RELEVANCY_PROMPT.format(context_str=node.text, query_str=query_str)
            response = self.llm.complete(prompt)
            score_str = response.text.strip()

            print("[DEBUG] Relevance LLM raw result:", score_str)

            try:
                score = float(score_str)
                if score >= 0.5:
                    relevant_texts.append(node.text)
            except ValueError:
                print("[WARNING] Could not parse score:", score_str)

        if not relevant_texts:
            print("[DEBUG] No relevant text found — triggering web fallback.")
            return WebSearchEvent(relevant_text="")
        else:
            return QueryEvent(relevant_text="\n".join(relevant_texts), search_text="")

    @step
    async def web_search(self, ctx: Context, ev: WebSearchEvent) -> QueryEvent:
        query_str = await ctx.get("query_str")

        prompt = REFINE_PROMPT.format(query_str=query_str)
        result = self.llm.complete(prompt)
        transformed_query_str = result.text.strip()

        search_results = self.linkup_tool.search(transformed_query_str).results
        print(
            "[DEBUG] Linkup returned results:",
            [r.content[:200] for r in search_results],
        )

        search_text = "\n".join([r.content for r in search_results])
        return QueryEvent(relevant_text=ev.relevant_text, search_text=search_text)

    @step
    async def query_result(self, ctx: Context, ev: QueryEvent) -> StopEvent:
        relevant_text = ev.relevant_text
        search_text = ev.search_text
        query_str = await ctx.get("query_str")

        if not relevant_text.strip() and not search_text.strip():
            return StopEvent(
                result="Sorry, I couldn’t find anything relevant to your question."
            )

        documents = [Document(text=relevant_text + "\n" + search_text)]
        index = SummaryIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        result = query_engine.query(query_str)

        return StopEvent(result=str(result))
