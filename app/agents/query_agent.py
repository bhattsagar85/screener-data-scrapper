from typing import List

from app.schemas.intent import (
    IntentSchema,
    TechnicalPattern,
)
from app.schemas.screener_query import (
    ScreenerQuerySchema,
    QueryCondition,
)


class QueryAgent:
    """
    Converts IntentSchema into a Screener.in DSL query.
    This agent is deterministic and contains NO LLM logic.
    """

    def build_query(self, intent: IntentSchema) -> ScreenerQuerySchema:
        conditions: List[QueryCondition] = []

        # -----------------------------
        # Technical Patterns
        # -----------------------------

        if intent.technical:
            for pattern in intent.technical.patterns:

                if pattern == TechnicalPattern.GOLDEN_CROSS:
                    conditions.extend([
                        QueryCondition(
                            field="Current price",
                            operator=">",
                            value="DMA 50"
                        ),
                        QueryCondition(
                            field="DMA 50",
                            operator=">",
                            value="DMA 200"
                        )
                    ])

                elif pattern == TechnicalPattern.DEATH_CROSS:
                    conditions.extend([
                        QueryCondition(
                            field="Close Price",
                            operator="<",
                            value="DMA 50"
                        ),
                        QueryCondition(
                            field="DMA 50",
                            operator="<",
                            value="DMA 200"
                        )
                    ])

                elif pattern == TechnicalPattern.VOLUME_SPIKE:
                    conditions.append(
                        QueryCondition(
                            field="Volume",
                            operator=">",
                            value="1.5 * Average Volume 10days"
                        )
                    )

                elif pattern == TechnicalPattern.PRICE_BREAKOUT:
                    conditions.append(
                        QueryCondition(
                            field="Close Price",
                            operator=">",
                            value="Previous Close"
                        )
                    )

        # -----------------------------
        # Fundamental Filters
        # -----------------------------

        if intent.fundamentals:

            f = intent.fundamentals

            if f.min_roce is not None:
                conditions.append(
                    QueryCondition(
                        field="ROCE",
                        operator=">",
                        value=str(f.min_roce)
                    )
                )

            if f.max_pe is not None:
                conditions.append(
                    QueryCondition(
                        field="PE",
                        operator="<",
                        value=str(f.max_pe)
                    )
                )

            if f.max_debt_to_equity is not None:
                conditions.append(
                    QueryCondition(
                        field="Debt to equity",
                        operator="<",
                        value=str(f.max_debt_to_equity)
                    )
                )

            if f.market_cap_min is not None:
                conditions.append(
                    QueryCondition(
                        field="Market Capitalization",
                        operator=">",
                        value=str(f.market_cap_min)
                    )
                )

            if f.market_cap_max is not None:
                conditions.append(
                    QueryCondition(
                        field="Market Capitalization",
                        operator="<",
                        value=str(f.market_cap_max)
                    )
                )

        # -----------------------------
        # Build Screener DSL string
        # -----------------------------

        query_string = " AND ".join(
            f"{c.field} {c.operator} {c.value}"
            for c in conditions
        )

        explanation = self._build_explanation(intent)

        return ScreenerQuerySchema(
            query_string=query_string,
            conditions=conditions,
            explanation=explanation,
        )

    # -----------------------------
    # Explanation Builder
    # -----------------------------

    def _build_explanation(self, intent: IntentSchema) -> str:
        parts: List[str] = []

        if intent.technical and intent.technical.patterns:
            patterns = ", ".join(p.value.replace("_", " ") for p in intent.technical.patterns)
            parts.append(f"Technical pattern(s): {patterns}")

        if intent.fundamentals:
            f = intent.fundamentals

            if f.min_roce is not None:
                parts.append(f"ROCE greater than {f.min_roce}%")

            if f.max_debt_to_equity is not None:
                parts.append(f"Debt to Equity less than {f.max_debt_to_equity}")

            if f.max_pe is not None:
                parts.append(f"P/E less than {f.max_pe}")

            if f.market_cap_min or f.market_cap_max:
                parts.append("Filtered by market capitalization range")

        if not parts:
            return "Basic stock screening query"

        return " | ".join(parts)
