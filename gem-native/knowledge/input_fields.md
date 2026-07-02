# 输入字段字典（input_fields.md）

> 本文件严格对应 `schemas/financial_input.schema.json`。
> 用于说明向 Gem 提供数据时的字段规范，确保输入结构正确、必填字段完整。

---

## 顶层结构

| 字段键 | 中文名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|---|
| `company` | 公司名称 | 字符串 | **必填** | 被分析企业的名称（用于报告标题） |
| `years` | 年度列表 | 整数数组 | **必填** | 包含的年度，如 `[2021, 2022, 2023]`，最少 1 个年度 |
| `data` | 年度财务数据 | 对象 | **必填** | 键为年度字符串（如 `"2021"`），值为该年度各字段 |
| `industry_benchmark` | 行业基准数据 | 对象 | 可选 | 行业中位数，用于对标分析（见下方说明） |

---

## 每个年度数据（`data["{年度}"]`）的字段

| 字段键 | 中文名 | 说明 |
|---|---|---|
| `period` | 报告期 | 可选：`annual`/`q1`/`h1`/`q2`/`q3`，缺省按 `annual`。用于季度数据下对指定比率分母做年化。 |

### 必填字段（每个年度均必须提供）

| 字段键 | 中文名 | 说明 |
|---|---|---|
| `revenue` | 营业收入 | 利润表口径，不含其他收益 |
| `cogs` | 营业成本 | 对应利润表"营业成本"行 |
| `cfo` | 经营活动现金流量净额 | 现金流量表"经营活动"净额 |
| `net_profit` | 净利润 | 利润表"净利润"（归母+少数） |

### 利润表字段（选填，缺失在加减法中按 0 处理）

| 字段键 | 中文名 | 说明 | 影响指标/规则 |
|---|---|---|---|
| `taxes_surcharges` | 税金及附加 | 利润表"税金及附加"行 | core_profit |
| `selling_exp` | 销售费用 | 利润表"销售费用"行 | core_profit, selling_exp_ratio |
| `admin_exp` | 管理费用 | 利润表"管理费用"行 | core_profit, admin_exp_ratio |
| `rd_exp` | 研发费用 | 利润表"研发费用"行 | core_profit, rd_exp_ratio |
| `operating_interest_exp` | 经营性利息费用 | 从财务费用中分拆的经营性部分（若不单独披露可留空） | core_profit |
| `other_income` | 其他收益 | 利润表"其他收益"行（政府补助等） | core_profit |
| `operating_profit` | 营业利润 | 利润表"营业利润"行（用于交叉验证） | 参考字段 |
| `non_recurring_pnl` | 非经常性损益 | 非经常性损益净额（净利润口径） | non_recurring_ratio, **R3** |
| `financial_exp` | 财务费用 | 利润表"财务费用"行 | fin_exp_ratio, **R1** |

### 资产负债表——资产端字段（选填）

| 字段键 | 中文名 | 说明 | 影响指标/规则 |
|---|---|---|---|
| `cash` | 货币资金 | 资产负债表"货币资金"行 | cash_ratio, **R1** |
| `ar` | 应收账款 | 应收账款净额（已扣坏账准备） | ar_to_rev, **R4** |
| `inventory` | 存货 | 存货净额（已扣跌价准备） | inv_to_cogs, **R4** |
| `goodwill` | 商誉 | 商誉净额（已扣减值） | goodwill_to_equity, goodwill_to_core_profit, **R5** |
| `operating_assets` | 经营性资产合计 | 与主营业务直接相关的资产合计 | op_vs_inv_assets |
| `investing_assets` | 投资性资产合计 | 金融投资类资产合计 | op_vs_inv_assets |
| `cip` | 在建工程 | 在建工程原值 | cip_ratio, **R1** |
| `total_assets` | 资产总计 | 资产负债表"资产总计" | cash_ratio, debt_ratio, cip_ratio, **R1**，三表勾稽CC1 |

### 资产负债表——负债权益端字段（选填）

| 字段键 | 中文名 | 说明 | 影响指标/规则 |
|---|---|---|---|
| `ap` | 应付账款+应付票据 | 两者合计 | ap_vs_inventory |
| `contract_liabilities` | 合同负债/预收款项 | 合同负债或旧准则预收款 | 参考字段 |
| `prepayments` | 预付款项 | 资产负债表"预付款项" | 参考字段 |
| `short_debt` | 短期借款 | 一年内到期的有息债务 | debt_ratio, **R1** |
| `long_debt` | 长期借款+应付债券 | 一年以上有息债务合计 | debt_ratio, **R1** |
| `retained_earnings` | 未分配利润 | 资产负债表"未分配利润" | 参考字段 |
| `total_equity` | 股东权益合计 | 归母+少数股东权益 | goodwill_to_equity, **R5** |

### 现金流量表字段（选填）

| 字段键 | 中文名 | 说明 | 影响指标/规则 |
|---|---|---|---|
| `cfi` | 投资活动现金流量净额 | 现金流量表"投资活动"净额 | 参考字段 |
| `cff` | 筹资活动现金流量净额 | 现金流量表"筹资活动"净额 | 参考字段 |
| `capex` | 资本支出 | "购建固定/无形/长期资产支付的现金" | capex_intensity |
| `dividend_paid` | 分配股利支付的现金 | 现金流量表筹资活动子项 | dividend_payout, **R6** |
| `new_equity_raised` | 吸收投资收到的现金 | 现金流量表筹资活动子项 | **R6** 分析辅助 |
| `credit_impairment` | 信用减值损失 | 绝对值，利润表"信用减值损失" | 参考字段 |
| `asset_impairment` | 资产减值损失 | 绝对值，利润表"资产减值损失" | 参考字段 |

### 附注字段（选填，缺失将影响特定规则精度）

| 字段键 | 中文名 | 说明 | 影响指标/规则 |
|---|---|---|---|
| `ar_aging_over_2y` | 账龄 2 年以上应收金额 | 来自年报附注应收账款账龄分析 | ar_provision_coverage, **R7**（缺失则 R7 无法判断） |
| `ar_provision` | 应收坏账准备 | 来自年报附注，已计提的坏账准备余额 | ar_provision_coverage, **R7**（缺失则 R7 无法判断） |
| `inventory_provision` | 存货跌价准备 | 来自年报附注，存货跌价准备余额 | 参考字段 |

---

## 行业基准字段（`industry_benchmark`，可选）

| 字段键 | 中文名 | 说明 |
|---|---|---|
| `gross_margin_median` | 行业毛利率中位数 | 用于对标企业毛利率水平 |
| `asset_turnover_median` | 行业资产周转率中位数 | 用于对标资产运营效率 |
| `debt_ratio_median` | 行业有息负债率中位数 | 用于对标负债结构 |

---

## 数据提供说明

1. **单位一致**：同一份数据中所有金额字段须使用相同单位（万元、百万元或亿元均可，但须统一）。
2. **年度键为字符串**：`data` 对象的键必须是年度的字符串形式，如 `"2023"`，而非整数。
3. **建议年度数**：建议提供 **3–5 年**数据，年度越多，趋势类规则（R2、R3、R4）的判断越准确。
4. **附注字段**：`ar_aging_over_2y` 和 `ar_provision` 来自年报附注，若缺失则 R7（减值计提不足）无法判断，建议尽量补充。
