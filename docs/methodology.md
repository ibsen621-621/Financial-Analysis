# 方法论与口径说明

## 1. 框架
底子（资产负债表）→ 面子（利润表）→ 日子（现金流量表）→ 三表勾稽。

## 2. 核心口径
- 核心利润 = 营业收入 − 营业成本 − 税金及附加 − 销售费用 − 管理费用 − 研发费用 − 经营性利息费用 + 其他收益
- 核心利润率 = 核心利润 / 营业收入
- 核心利润获现率 = 经营活动现金流量净额 / 核心利润

## 3. 边界与免责
- 本模型为结构化辅助分析，不构成投资建议。
- 附注字段缺失会降低减值类规则(R7)与商誉规则(R5)的可靠性。
- 阈值为经验默认值，应结合行业分位动态校准。

## 4. 季度数据年化
- 为避免季度口径下"存量 ÷ 单期流量"错配，按报告期对流量分母年化：
  - `annual` = 1
  - `q1` = 4
  - `h1`/`q2` = 2
  - `q3` = 4/3
- 仅以下指标使用年化分母：`ar_to_rev`、`inv_to_cogs`、`capex_intensity`、`goodwill_to_core_profit`。
- 存量÷存量（如 `cash_ratio`、`debt_ratio`）和流量÷流量（如 `core_profit_margin`、`cash_conversion`）不年化，保持原口径。
- 默认 `period=annual`，因此历史年报数据结果与裁决保持不变；R1–R7 阈值不变。
- 本协议按 A 股常见 YTD 累计口径处理。若输入为"单季"而非累计口径，请先转换为累计数据或自行调整年化系数。

## 5. 部署
1. `pip install -r requirements.txt`
2. `uvicorn app:app --reload --port 8000`
3. 在 Gemini Gem 中配置 `gem/function_declarations.json`，将 `analyze_financial_statements` 指向 `POST /analyze`。
4. 用 `examples/demo_company_5y.json` 验证链路。
