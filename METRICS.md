# Metrics

## Core Metrics

| Metric         | Value  |
| -------------- | ------ |
| Code Coverage  | 0%     |
| Build Time     | 0s     |
| Bundle Size    | 0KB    |
| Test Files     | 0      |
| Test Cases     | 0      |

## Health

| Metric         | Value    |
| -------------- | -------- |
| Open Issues    | 0        |
| PR Turnaround  | 0 days   |
| Skipped Tests  | 0        |
| Health Score   | 0/100    |

<!--
AGENT INSTRUCTIONS:
This file tracks project health metrics using a structured table format.

CRITICAL FORMAT REQUIREMENTS:
1. Use EXACTLY these section names: "## Core Metrics", "## Health"
2. Metrics MUST be in markdown table format with "| Metric | Value |" headers
3. Keep metric names and values on single lines
4. Common metric names for parsing: "Code Coverage", "Build Time", "Bundle Size"
5. Health metrics: "Open Issues", "PR Turnaround", "Skipped Tests", "Health Score"

PARSEABLE METRIC NAMES (case-insensitive):
- "Code Coverage" or "Coverage" → Extracted for health score calculation
- "Test Files", "Test Cases" → Testing metrics
- "Build Time" → Performance metric
- "Bundle Size" → Performance metric
- "Open Issues" → Health indicator
- "Health Score" → Overall health

GOOD EXAMPLES:
## Core Metrics

| Metric         | Value  |
| -------------- | ------ |
| Code Coverage  | 87.5%  |
| Build Time     | 6.2s   |
| Test Files     | 4      |

## Health

| Metric         | Value    |
| -------------- | -------- |
| Open Issues    | 3        |
| Health Score   | 95/100   |

BAD EXAMPLES (may not parse correctly):
### Core Metrics (wrong heading level)
Metric: Code Coverage
Value: 87% (not in table format)

When updating:
1. Update values based on latest code analysis or CI/CD outputs
2. "Code Coverage": Percentage of code covered by tests (e.g., "87.5%")
3. "Build Time": Time taken for build process (e.g., "6.2s")
4. "Bundle Size": Size of production assets (e.g., "245KB")
5. Ensure values are accurate and reflect current codebase state
6. Add custom metrics as new table rows in appropriate sections
-->
