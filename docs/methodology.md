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

## 4. 部署
1. `pip install -r requirements.txt`
2. `uvicorn app:app --reload --port 8000`
3. 在 Gemini Gem 中配置 `gem/function_declarations.json`，将 `analyze_financial_statements` 指向 `POST /analyze`。
4. 用 `examples/demo_company_5y.json` 验证链路。
