# 财务数据录入模板（input_template.md）

> 复制本模板，填入目标公司的财务数据，然后将填好的内容粘贴给 Gem，即可获得三表穿透分析报告。
>
> **填写说明**：
> - **必填字段**：`revenue`、`cogs`、`cfo`、`net_profit` 每年度必须填写，否则分析无法进行。
> - **建议年度数**：覆盖 3–5 个会计年度，趋势类风险规则（R2、R3、R4）需要多年数据才能判断。
> - **附注字段**：`ar_aging_over_2y`（账龄 2 年以上应收）和 `ar_provision`（应收坏账准备）来自年报附注，缺失会导致 R7（减值计提不足）无法判断，建议尽量补充。
> - **单位**：同一份数据中所有金额须使用相同单位（万元 / 百万元 / 亿元，选一即可）。
> - 不知道的字段可留空（删除该行或填 `null`），Gem 会在缺失数据清单中列出影响。

---

## 方式一：JSON 格式（推荐，与示例样例格式一致）

将以下 JSON 结构填入公司数据后，整体粘贴给 Gem：

```json
{
  "company": "【公司名称】",
  "years": [20XX, 20XX, 20XX],
  "data": {
    "20XX": {
      "revenue": null,
      "cogs": null,
      "taxes_surcharges": null,
      "selling_exp": null,
      "admin_exp": null,
      "rd_exp": null,
      "operating_interest_exp": null,
      "other_income": null,
      "operating_profit": null,
      "net_profit": null,
      "non_recurring_pnl": null,
      "cash": null,
      "ar": null,
      "inventory": null,
      "goodwill": null,
      "operating_assets": null,
      "investing_assets": null,
      "cip": null,
      "total_assets": null,
      "ap": null,
      "contract_liabilities": null,
      "prepayments": null,
      "short_debt": null,
      "long_debt": null,
      "financial_exp": null,
      "retained_earnings": null,
      "total_equity": null,
      "cfo": null,
      "cfi": null,
      "cff": null,
      "capex": null,
      "dividend_paid": null,
      "new_equity_raised": null,
      "credit_impairment": null,
      "asset_impairment": null,
      "ar_aging_over_2y": null,
      "ar_provision": null,
      "inventory_provision": null
    }
  }
}
```

**操作步骤**：
1. 将 `"20XX"` 替换为实际年度，如 `"2021"`，并在 `years` 数组中同步更新（注意 years 中是整数，data 的键是字符串）。
2. 若有多年数据，复制 `"20XX": { ... }` 块，粘贴并修改年度。
3. 将各字段的 `null` 替换为实际数值（相同单位），不知道的字段保留 `null` 或删除该行。
4. 将填好的完整 JSON 粘贴给 Gem。

---

## 方式二：表格格式（适合手工填写，视觉更直观）

在下方表格中填写数据（每列为一个年度），然后粘贴给 Gem：

### 利润表数据

| 字段（中文名） | 字段键 | 必填 | 20XX 年 | 20XX 年 | 20XX 年 |
|---|---|:---:|---|---|---|
| 营业收入 | `revenue` | ✅ | | | |
| 营业成本 | `cogs` | ✅ | | | |
| 税金及附加 | `taxes_surcharges` | | | | |
| 销售费用 | `selling_exp` | | | | |
| 管理费用 | `admin_exp` | | | | |
| 研发费用 | `rd_exp` | | | | |
| 经营性利息费用 | `operating_interest_exp` | | | | |
| 其他收益 | `other_income` | | | | |
| 营业利润 | `operating_profit` | | | | |
| 净利润 | `net_profit` | ✅ | | | |
| 非经常性损益 | `non_recurring_pnl` | | | | |
| 财务费用 | `financial_exp` | | | | |

### 资产负债表数据（资产端）

| 字段（中文名） | 字段键 | 必填 | 20XX 年 | 20XX 年 | 20XX 年 |
|---|---|:---:|---|---|---|
| 货币资金 | `cash` | | | | |
| 应收账款 | `ar` | | | | |
| 存货 | `inventory` | | | | |
| 商誉 | `goodwill` | | | | |
| 经营性资产合计 | `operating_assets` | | | | |
| 投资性资产合计 | `investing_assets` | | | | |
| 在建工程 | `cip` | | | | |
| 资产总计 | `total_assets` | | | | |
| 预付款项 | `prepayments` | | | | |

### 资产负债表数据（负债权益端）

| 字段（中文名） | 字段键 | 必填 | 20XX 年 | 20XX 年 | 20XX 年 |
|---|---|:---:|---|---|---|
| 应付账款+应付票据 | `ap` | | | | |
| 合同负债/预收款项 | `contract_liabilities` | | | | |
| 短期借款 | `short_debt` | | | | |
| 长期借款+应付债券 | `long_debt` | | | | |
| 未分配利润 | `retained_earnings` | | | | |
| 股东权益合计 | `total_equity` | | | | |

### 现金流量表数据

| 字段（中文名） | 字段键 | 必填 | 20XX 年 | 20XX 年 | 20XX 年 |
|---|---|:---:|---|---|---|
| 经营活动现金流量净额 | `cfo` | ✅ | | | |
| 投资活动现金流量净额 | `cfi` | | | | |
| 筹资活动现金流量净额 | `cff` | | | | |
| 资本支出 | `capex` | | | | |
| 分配股利支付的现金 | `dividend_paid` | | | | |
| 吸收投资收到的现金 | `new_equity_raised` | | | | |
| 信用减值损失 | `credit_impairment` | | | | |
| 资产减值损失 | `asset_impairment` | | | | |

### 附注数据（影响 R7 规则，建议补充）

| 字段（中文名） | 字段键 | 必填 | 20XX 年 | 20XX 年 | 20XX 年 |
|---|---|:---:|---|---|---|
| 账龄 2 年以上应收金额 | `ar_aging_over_2y` | | | | |
| 应收坏账准备 | `ar_provision` | | | | |
| 存货跌价准备 | `inventory_provision` | | | | |

---

## 最小示例参考

以下是引用 `examples/demo_company_5y.json`（仓库根目录）的最小示例说明：

> 该示例包含"示例科技股份" 2021–2023 年三年数据（文件名含"5y"为命名惯例），字段覆盖率较高（包含附注数据）。
> 可直接将 `demo_company_5y.json` 的完整 JSON 内容粘贴给 Gem，验证分析流程是否正确运行。
>
> **预期触发规则**：
> - R2（失血式增长）：2022–2023 年获现率分别约为 0.68 和 0.50，均 < 0.8
> - R5（商誉减值压力）：2023 年商誉/净资产 = 300/1000 = 0.30，商誉/核心利润偏高
> - R7（减值计提不足）：2023 年 ar_provision_coverage = 30/140 ≈ 0.21 < 0.30
> - **预期最终判断：回避**（高风险规则 ≥ 2 条）
