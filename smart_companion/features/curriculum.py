from typing import List, Dict

class CurriculumManager:
    """
    Manages exam curriculum and tutor prompts.
    """
    def __init__(self):
        self.subjects = {
            "Physics": ["Mechanics", "Electromagnetism", "Thermodynamics"],
            "Chemistry": ["Organic", "Inorganic", "Physical"],
            "Math": ["Calculus", "Algebra", "Geometry"],
            "CS": ["Algorithms", "Data Structures", "OS"]
        }

        self.tutor_prompts = {
            "Socratic": "You are a Socratic tutor. Guide the student to the answer with questions. Do not give the answer directly.",
            "ELI5": "Explain the concept as if I am 5 years old. Use analogies.",
            "Exam": "Test me on this topic with a hard question, then evaluate my answer."
        }

    def get_topics(self, subject: str) -> List[str]:
        return self.subjects.get(subject, [])

    def get_tutor_prompt(self, mode: str) -> str:
        return self.tutor_prompts.get(mode, "You are a helpful tutor.")

    def add_topic(self, subject: str, topic: str):
        if subject in self.subjects:
            self.subjects[subject].append(topic)
        else:
            self.subjects[subject] = [topic]
