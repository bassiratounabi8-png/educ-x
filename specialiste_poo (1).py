"""
specialiste_poo.py
Defines the Question base class and its two concrete subclasses:
MultipleChoiceQuestion and TrueFalseQuestion.
Demonstrates abstraction, inheritance, and polymorphism.
"""

from abc import ABC, abstractmethod


class Question(ABC):
    """
    Abstract base class representing a generic quiz question.
    Subclasses must implement verify_answer() and display().
    Encapsulates common attributes: id, statement, subject, difficulty,
    author, explanation, and answer history.
    """

    def __init__(
        self,
        id: int,
        statement: str,
        subject: str,
        difficulty: int = 1,
        author: str = None,
        explanation: str = None,
    ) -> None:
        """
        Initialises a Question with its core attributes.

        Args:
            id (int): Unique identifier for the question.
            statement (str): The question text shown to the user.
            subject (str): The topic this question belongs to.
            difficulty (int): Difficulty level, default is 1.
            author (str): Optional name of whoever wrote the question.
            explanation (str): Optional explanation shown after answering.
        """
        self.id = id
        self.statement = statement
        self.subject = subject
        self.difficulty = difficulty
        self.author = author
        self.explanation = explanation
        self.history: list = []  # stores True/False for each attempt

    @abstractmethod
    def verify_answer(self, answer: str) -> bool:
        """Checks whether the given answer is correct. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def display(self, highlight=None) -> str:
        """Returns a formatted string to display the question. Must be implemented by subclasses."""
        pass

    def add_result(self, correct: bool) -> None:
        """Records whether the last attempt was correct or not."""
        self.history.append(correct)

    @staticmethod
    def text_style(text: str, red: bool = False, underline: bool = False) -> str:
        """
        Applies ANSI terminal styling to a string.

        Args:
            text (str): The text to style.
            red (bool): If True, applies red colour.
            underline (bool): If True, underlines the text.

        Returns:
            str: The styled string.
        """
        codes = []
        if red:
            codes.append("31")
        if underline:
            codes.append("4")
        if not codes:
            return text
        return f"\033[{';'.join(codes)}m{text}\033[0m"

    def display_header(self) -> str:
        """Returns a header string showing subject, difficulty, and optional author."""
        header = f"{self.subject} — Difficulty {self.difficulty}"
        if self.author:
            header += f" — Author: {self.author}"
        return header

    def display_explanation(self) -> str:
        """Returns the explanation text if one exists, otherwise returns an empty string."""
        return f"\nExplanation: {self.explanation}" if self.explanation else ""

    def score(self) -> str:
        """
        Returns the success rate across all attempts as a formatted string.
        Example: '3/5 (60%)'
        """
        if not self.history:
            return "No results"
        correct = sum(self.history)
        total = len(self.history)
        return f"{correct}/{total} ({correct * 100 / total:.0f}%)"

    def __str__(self) -> str:
        """Returns a short readable summary of the question."""
        return f"[{self.id}] {self.statement} ({self.subject})"


class MultipleChoiceQuestion(Question):
    """
    A question that presents several answer choices.
    The user selects the correct one by index or by typing the answer.
    Inherits from Question and implements verify_answer() and display().
    """

    def __init__(
        self,
        id: int,
        statement: str,
        subject: str,
        choices: list,
        correct_answer: int,
        difficulty: int = 1,
        author: str = None,
        explanation: str = None,
    ) -> None:
        """
        Initialises a MultipleChoiceQuestion.

        Args:
            choices (list): List of answer options, e.g. ["Paris", "Lyon", "Marseille"].
            correct_answer (int): Index of the correct choice in the list.
        """
        super().__init__(id, statement, subject, difficulty, author=author, explanation=explanation)
        self.choices = choices
        self.correct_answer = correct_answer  # index of the correct option

    def display(self, highlight: int = None) -> str:
        """
        Returns the question and its choices as a formatted string.
        Optionally highlights one choice in red and underlined.
        """
        text = f"\n{self.display_header()}\n{self.statement}\n"
        for i, choice in enumerate(self.choices):
            index = f"{i}."
            if highlight is not None and highlight == i:
                index = self.text_style(index, red=True, underline=True)
            text += f"  {index} {choice}\n"
        return text

    def verify_answer(self, answer: str) -> bool:
        """
        Checks whether the user's answer matches the correct choice.
        Accepts either the index as a number or the answer text directly.

        Args:
            answer (str): The user's input.

        Returns:
            bool: True if correct, False otherwise.
        """
        try:
            # Try treating the input as an index number
            value = int(answer)
            is_correct = value == self.correct_answer
        except (ValueError, TypeError):
            # Fall back to comparing text directly
            is_correct = (
                str(answer).strip().lower()
                == str(self.choices[self.correct_answer]).strip().lower()
            )
        self.add_result(is_correct)
        return is_correct


class TrueFalseQuestion(Question):
    """
    A question with only two possible answers: True or False.
    Inherits from Question and implements verify_answer() and display().
    Demonstrates polymorphism: same method name, different behaviour.
    """

    def __init__(
        self,
        id: int,
        statement: str,
        subject: str,
        answer: bool,
        difficulty: int = 1,
        author: str = None,
        explanation: str = None,
    ) -> None:
        """
        Initialises a TrueFalseQuestion.

        Args:
            answer (bool): The correct answer, True or False.
        """
        super().__init__(id, statement, subject, difficulty, author=author, explanation=explanation)
        self.answer = bool(answer)

    def display(self, highlight: str = None) -> str:
        """Returns the question text with a True or False prompt."""
        text = f"\n{self.display_header()}\n{self.statement}\nTrue or False?"
        if highlight == "true":
            text = self.text_style(text, red=True, underline=True)
        return text

    def verify_answer(self, answer: str) -> bool:
        """
        Checks whether the user's answer matches the correct boolean value.
        Accepts several common ways to say true or false.

        Args:
            answer (str): The user's input.

        Returns:
            bool: True if correct, False otherwise.
        """
        response = str(answer).strip().lower()

        # Accept multiple ways of expressing true or false
        if response in ["true", "t", "1", "yes", "y"]:
            choice = True
        elif response in ["false", "f", "0", "no", "n"]:
            choice = False
        else:
            choice = None  # unrecognised input counts as wrong

        is_correct = choice is not None and choice == self.answer
        self.add_result(is_correct)
        return is_correct
