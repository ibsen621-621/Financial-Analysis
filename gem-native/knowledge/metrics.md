# 指标计算口径（metrics.md）

> 本文件是 Gem 原生版的计算协议参考，严格对应 `engine/metrics.py` 中的 `compute_year` 函数。
> Gem 在分析时必须逐年、逐指标按本文件定义计算，不得自行修改公式或阈值。

---

## 辅助函数语义

### `safe_div(a, b)`
所有指标的除法运算均使用 `safe_div`：
- 若分母 `b` 为 `0`、`0.0` 或 `None`（缺失），则结果为 **N/A**（不得臆造数值）。
- 只有分母为有效非零数值时，才执行 `a ÷ b`。

### `_g(d, key)`
从输入数据中取字段值：
- 若字段存在且有值，返回该值（转为浮点数）。
- 若字段**缺失或为 null**，在**加减法**中按 `0` 处理（不影响结果符号）。
- 但若该字段作为**分母**，则按"缺失"处理，`safe_div` 返回 N/A。

---

## 第一步：核心利润（core_profit）

核心利润是后续多个比率的基础，必须优先计算。

```
core_profit = revenue
            − cogs
            − taxes_surcharges      （缺失按 0）
            − selling_exp           （缺失按 0）
            − admin_exp             （缺失按 0）
            − rd_exp                （缺失按 0）
            − operating_interest_exp（缺失按 0）
            + other_income          （缺失按 0）
```

---

## 第二步：全部指标定义

| 指标键 | 中文名 | 公式 | 说明 |
|---|---|---|---|
| `core_profit` | 核心利润 | 见上方公式 | 反映主业真实盈利能力（剔除金融损益，加回政策补贴） |
| `core_profit_margin` | 核心利润率 | `core_profit ÷ revenue` | 主业盈利占收入比，衡量定价能力与成本管控 |
| `gross_margin` | 毛利率 | `(revenue − cogs) ÷ revenue` | 产品/服务的基础盈利空间 |
| `cash_conversion` | 核心利润获现率 | `cfo ÷ core_profit` | 核心利润转化为实际现金的能力；< 0.8 连续两年触发 R2 |
| `cfo_to_net_profit` | CFO/净利润 | `cfo ÷ net_profit` | 净利润的现金含金量；< 1 说明利润中有较多非现金成分 |
| `selling_exp_ratio` | 销售费用率 | `selling_exp ÷ revenue` | 销售投入强度 |
| `admin_exp_ratio` | 管理费用率 | `admin_exp ÷ revenue` | 管理效率 |
| `rd_exp_ratio` | 研发费用率 | `rd_exp ÷ revenue` | 创新投入强度 |
| `ar_to_rev` | 应收/收入 | `ar ÷ revenue` | 应收账款占收入比；上升趋势结合存货双升触发 R4 |
| `inv_to_cogs` | 存货/成本 | `inventory ÷ cogs` | 存货相对成本的积压程度 |
| `cash_ratio` | 货币资金/资产 | `cash ÷ total_assets` | 资产中现金占比；≥ 0.20 为 R1 条件之一 |
| `debt_ratio` | 有息负债率 | `(short_debt + long_debt) ÷ total_assets` | 资产中有息债务占比；≥ 0.25 为 R1 条件之一 |
| `fin_exp_ratio` | 财务费用/收入 | `financial_exp ÷ revenue` | 融资成本负担；≥ 0.02 为 R1 条件之一 |
| `cip_ratio` | 在建工程/资产 | `cip ÷ total_assets` | 资产中在建工程占比；≥ 0.10 为 R1 条件之一 |
| `goodwill_to_equity` | 商誉/净资产 | `goodwill ÷ total_equity` | 商誉对净资产的侵蚀风险；≥ 0.30 为 R5 条件之一 |
| `goodwill_to_core_profit` | 商誉/核心利润 | `goodwill ÷ core_profit` | 商誉消化能力；≥ 3.0 为 R5 条件之一 |
| `op_vs_inv_assets` | 经营性/投资性资产 | `operating_assets ÷ investing_assets` | 资产结构中经营资产主导程度；比值越高越健康 |
| `ap_vs_inventory` | 应付/存货 | `ap ÷ inventory` | 供应链话语权；比值高说明对供应商占款能力强 |
| `capex_intensity` | 资本开支强度 | `capex ÷ revenue` | 维持/扩张业务所需的资本投入密度 |
| `dividend_payout` | 分红率 | `dividend_paid ÷ net_profit` | 利润中用于分红的比例；≥ 0.50 触发 R6 |
| `non_recurring_ratio` | 非经常性损益占比 | `non_recurring_pnl ÷ net_profit` | 利润中非经常性成分占比；≥ 0.30 结合利润率下行触发 R3 |
| `ar_provision_coverage` | 2年以上应收坏账覆盖率 | `ar_provision ÷ ar_aging_over_2y` | 高账龄应收的坏账准备充足度；< 0.30 触发 R7 |

---

## 计算注意事项

1. **计算顺序**：先算 `core_profit`，再用它计算 `core_profit_margin`、`cash_conversion`、`goodwill_to_core_profit`。
2. **缺失字段**：`taxes_surcharges`、`selling_exp`、`admin_exp`、`rd_exp`、`operating_interest_exp`、`other_income` 缺失时在加减法中按 0 处理，但不等于这些费用不存在，应在缺失清单中标注。
3. **N/A 的传播**：若 `core_profit = 0`，则 `cash_conversion`、`goodwill_to_core_profit` 均为 N/A。
4. **精度**：中间计算保持全精度，最终报告展示核心利润保留整数或1位小数，比率类指标转为百分比保留1位小数。
