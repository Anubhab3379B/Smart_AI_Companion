from typing import List
from smart_companion.tools.web_search import web_search_tool

class DeepResearcher:
    """
    Orchestrates a deep research session by breaking down queries.
    """
    def __init__(self, agent):
        self.agent = agent

    def research(self, topic: str) -> str:
        """
        Performs multi-step research on a topic.
        """
        # Step 1: Breakdown
        plan = self.agent.run(f"Break down this research topic into 3 specific sub-questions: {topic}. Return them as a numbered list.")
        
        # Step 2: Search loop
        report_sections = []
        sub_questions = [line for line in plan.split('\n') if line.strip()]
        
        for q in sub_questions[:3]: # Limit to top 3 for speed
             # Search using the tool directly or via agent
             # We use the raw tool for precision here
             search_results = web_search_tool.run(q)
             summary = self.agent.run(f"Summarize these search results for the question '{q}':\n{search_results}")
             report_sections.append(f"### {q}\n{summary}")
        
        # Step 3: Synthesis
        full_report_text = "\n\n".join(report_sections)
        final_synthesis = self.agent.run(f"Synthesize this research data into a comprehensive report on '{topic}':\n\n{full_report_text}")
        
        return final_synthesis
