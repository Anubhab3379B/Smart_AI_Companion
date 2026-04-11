from typing import List, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.memory import ConversationBufferMemory
from smart_companion.core.inference import ModelManager
from smart_companion.core.memory import MemorySystem
from smart_companion.tools.math_tools import math_tool
from smart_companion.tools.code_executor import code_tool
from smart_companion.tools.web_search import web_search_tool
from smart_companion.tools.manim_tool import manim_tool

class CompanionAgent:
    """
    The main orchestrator that connects the LLM, Memory, and Tools.
    """
    def __init__(self, model_manager: ModelManager, memory_system: Optional[MemorySystem] = None):
        self.model_manager = model_manager
        self.memory_system = memory_system
        self.tools = [math_tool, code_tool, web_search_tool, manim_tool]
        self.agent_executor = self._build_agent()

    def _build_agent(self):
        # We need to wrap our ModelManager's LLM or just use LlamaCpp from LangChain directly
        # utilizing the same model path.
        # For simplicity, we re-instantiate LlamaCpp here or adapt ModelManager.
        # Check if ModelManager has a path
        
        llm = LlamaCpp(
            model_path=self.model_manager.model_path,
            n_ctx=self.model_manager.n_ctx,
            n_gpu_layers=self.model_manager.n_gpu_layers,
            temperature=0.7,
            verbose=False
        )

        template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)

        agent = create_react_agent(llm, self.tools, prompt)
        
        return AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            verbose=True, 
            handle_parsing_errors=True,
            memory=ConversationBufferMemory(memory_key="chat_history")
        )

    def run(self, query: str) -> str:
        """
        Runs the agent loop.
        """
        # First, check memory (RAG)
        context = ""
        if self.memory_system:
            docs = self.memory_system.query(query)
            if docs:
                context = "\n".join([d.page_content for d in docs])
                # We could inject this context into the prompt or just prepend it
                query = f"Context from memory:\n{context}\n\nQuestion: {query}"
        
        try:
            return self.agent_executor.invoke({"input": query})['output']
        except Exception as e:
            return f"Agent Logic Error: {e}"

if __name__ == "__main__":
    # Example
    # mgr = ModelManager("path/to/model")
    # agent = CompanionAgent(mgr)
    # print(agent.run("What is 25 * 52?"))
    pass
