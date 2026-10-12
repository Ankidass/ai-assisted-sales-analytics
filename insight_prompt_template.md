# AI-assisted insight prompt template

Use this after you have generated and checked the summary tables. Do not paste personal or confidential data into an AI tool.

> You are assisting with a beginner sales analytics practice project. Using only the summary table below, identify up to three patterns worth investigating. For each pattern, cite the exact numbers from the table, distinguish observation from hypothesis, and suggest one follow-up question. Do not invent causes, do not claim causation from correlation, and state when the data is insufficient.
>
> Summary table:
> [Paste `outputs/category_summary.csv` or `outputs/monthly_summary.csv` here]
>
> Output format:
> 1. Observed pattern (include metric and values)
> 2. Possible explanation (clearly label as a hypothesis)
> 3. Follow-up analysis to validate it

## Human validation checklist
- Verify the totals against the source CSV / SQL query.
- Check whether categories or months have very different order counts.
- Do not call a product "underperforming" based on revenue alone; also consider margin, units, discount, and sample size.
- Edit or reject AI-generated claims that cannot be supported by the data.
