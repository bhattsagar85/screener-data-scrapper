from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from app.schemas.intent import IntentSchema


class IntentAgent:
    """
    Converts natural language stock screening queries
    into a validated IntentSchema.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0
    ):
        # LLM (deterministic)
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature
        )

        # Structured output parser
        self.parser = PydanticOutputParser(
            pydantic_object=IntentSchema
        )

        # Prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert Indian Stock Market Analyst.

Your job is to extract structured intent from user stock screening queries.

RULES:
- Output ONLY valid JSON matching the given schema
- Do NOT invent indicators or fields
- If something is not mentioned, leave it null
- Use defaults ONLY when explicitly defined below

SUPPORTED TECHNICAL PATTERNS:
- golden_cross
- death_cross
- price_breakout
- volume_spike

SUPPORTED FUNDAMENTALS:
- ROCE
- P/E
- Debt to Equity
- Market Capitalization

DEFAULT INTERPRETATIONS (IMPORTANT):
- "low debt" means Debt to Equity < 0.5
- "high ROCE" means ROCE > 20
- "midcap" means Market Capitalization between 5,000 and 20,000 crores

If the user uses these vague terms, apply the defaults.
Otherwise, do NOT guess numeric thresholds.

{format_instructions}
"""
                ),
                ("human", "{user_query}")
            ]
        )

        # Chain
        self.chain = self.prompt | self.llm | self.parser

    def run(self, user_query: str) -> IntentSchema:
        """
        Execute intent extraction and return IntentSchema.
        """
        return self.chain.invoke(
            {
                "user_query": user_query,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
