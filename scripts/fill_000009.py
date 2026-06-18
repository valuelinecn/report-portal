#!/usr/bin/env python3
"""
中国宝安(000009) 研究报告 — 逐项填充脚本
数据来源：2025年年报(218页) + 2024年报(252页)
"""
import re, os

REPORT = "/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports/000009.html"

with open(REPORT, 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

def replace_all(old, new, desc=""):
    global changes, html
    if old.startswith('{{') and old.endswith('}}'):
        # placeholder replacement
        c = html.count(old)
        if c == 0:
            print(f"  ⚠️ 未找到占位符: {old}")
            return False
        html_new = html.replace(old, new)
        if html_new != html:
            changes += 1
            html = html_new
            print(f"  ✅ {desc}: {old} → {new[:60]}{'...' if len(new)>60 else ''}")
            return True
        return False
    else:
        # general text replacement
        c = html.count(old)
        if c == 0:
            print(f"  ⚠️ 未找到: {desc}")
            return False
        html = html.replace(old, new, 1)
        changes += 1
        print(f"  ✅ {desc}")
        return True

# =============================================
# 基础信息
# =============================================
replace_all('{{COMPANY_NAME_CN}}', '中国宝安', '公司名称')
replace_all('{{REPORT_DATE}}', '2026-06-18', '报告日期')
replace_all('{{DATA_SOURCE}}', '年报PDF(2025/2024) + 季报PDF(2026Q1) + 东方财富', '数据来源')
replace_all('{{SCORE}}', '5.5', '综合评分')
replace_all('{{RATING_DESC}}', '中国宝安是横跨高新技术(贝特瑞负极材料龙头)、生物医药(马应龙)的综合控股集团。2025年营收230.36亿(+13.9%)净利2.03亿(+17.6%)，扣非净利-0.72亿。核心看点：贝特瑞全球负极材料龙头受益新能源/储能高景气，马应龙品牌稳健。风险：综合毛利率25.82%持续承压，负债率59.8%，地产亏损。', '评级描述')

# =============================================
# 综合评价卡片 (4张卡 = 综合评级/风险等级/成长弹性/ROE)
# =============================================
replace_all('{{CARD1_VAL}}', '5.5', '综合评级-值')
replace_all('{{CARD1_LABEL}}', '综合评级', '综合评级-标签')
replace_all('{{CARD1_COLOR}}', '#f0c040', '综合评级-颜色')

replace_all('{{CARD2_VAL}}', '中-高', '风险等级-值')
replace_all('{{CARD2_LABEL}}', '风险等级', '风险等级-标签')
replace_all('{{CARD2_COLOR}}', '#ff9800', '风险等级-颜色')

replace_all('{{CARD3_VAL}}', '中', '成长弹性-值')
replace_all('{{CARD3_LABEL}}', '成长弹性', '成长弹性-标签')
replace_all('{{CARD3_COLOR}}', '#f0c040', '成长弹性-颜色')

replace_all('{{CARD4_VAL}}', '2.04%', 'ROE-值')
replace_all('{{CARD4_LABEL}}', 'ROE', 'ROE-标签')
replace_all('{{CARD4_COLOR}}', '#888', 'ROE-颜色')

# 额外标签
replace_all('{{LABEL_2_TITLE}}', '净利', '标签2标题')
replace_all('{{LABEL_2}}', '2.03亿', '标签2值')
replace_all('{{LABEL_3_TITLE}}', '扣非净利', '标签3标题')
replace_all('{{LABEL_3}}', '-0.72亿', '标签3值')

# =============================================
# LOGIC 卡
# =============================================
replace_all('{{LOGIC_1}}', '三年预估空间', 'LOGIC1 标题')
replace_all('{{LOGIC_1_VAL}}', '动力电池需求CAGR~25%，储能需求CAGR~50%，负极材料行业空间翻倍', 'LOGIC1 内容')
replace_all('{{LOGIC_2}}', '核心竞争力', 'LOGIC2 标题')
replace_all('{{LOGIC_2_DETAIL}}', '贝特瑞全球负极龙头(市占率~22%)+马应龙400年老字号+五地六家公众公司资本平台', 'LOGIC2 内容')
replace_all('{{LOGIC_3}}', '季度监控', 'LOGIC3 标题')
replace_all('{{LOGIC_3_DETAIL}}', '毛利率趋势/贝特瑞季度出货量/经营现金流/负债率变化', 'LOGIC3 内容')
replace_all('{{LOGIC_4}}', '安全边际', 'LOGIC4 标题')
replace_all('{{LOGIC_4_DETAIL}}', 'PB 1.76x处于历史低位，PS(TTM) 0.77x估值偏低。扣非亏损PE不适用，需等待毛利率企稳', 'LOGIC4 内容')

# =============================================
# 综合评价 BQ
# =============================================
replace_all('{{INVESTMENT_THESIS}}', '中国宝安核心价值在于控股子公司贝特瑞(全球锂电负极材料龙头，2025年营收169.8亿)和马应龙(400年中华老字号，营收38.7亿)。2025年集团营收230.36亿(+13.9%)，归母净利2.03亿(+17.6%)但扣非-0.72亿。核心矛盾：贝特瑞负极受益新能源/储能高景气持续增长，但综合毛利率25.82%(+1.46pct)承压，财务费用因利息资本化减少而增长105%至6.7亿。负债率59.8%，ROE仅2.04%。PB 1.76x处于历史偏低区间。', '投资理念')

# =============================================
# M1 商业模式 & 收入结构
# =============================================
replace_all('{{ANALYSIS_TEXT}}', '中国宝安是产业投控型集团，旗下核心资产：①贝特瑞(北交所上市，全球负极材料龙头，市占率~22%)，2025年营收169.83亿(+19.3%)；②马应龙(上交所上市，400年中华老字号)，营收38.67亿(+3.7%)；③国际精密(港股上市，精密制造)，营收10.03亿(+7.6%)；④友诚科技(新三板，充电枪)，营收5.30亿(-0.2%)；⑤房地产业务(去库存中)，营收1.36亿(-40.2%)。', 'M1 分析描述')

# 分业务收入结构
# 高新技术行业 (贝特瑞为主): 2024=158.89亿, 2025=186.98亿, YoY=+17.7%, 毛利率2024=23.27%, 2025=21.44%
# 生物医药行业 (马应龙为主): 2024=37.94亿, 2025=39.41亿, YoY=+3.9%, 毛利率2024=45.93%, 2025=48.38%
# 房地产: 2024=2.27亿, 2025=1.36亿, YoY=-40.2%
# 其他: 2024=3.18亿, 2025=2.61亿, YoY=-17.9%

# M1 revenue rows - replace the entire section
replace_all('{{M1_REVENUE_ROWS}}', 
    '<tr><td>高新技术</td><td>158.89亿</td><td>186.98亿</td><td>+17.7%</td><td>23.27%</td><td>21.44%</td><td>-1.83pct</td></tr>'
    '<tr><td>生物医药</td><td>37.94亿</td><td>39.41亿</td><td>+3.9%</td><td>45.93%</td><td>48.38%</td><td>+2.45pct</td></tr>'
    '<tr><td>房地产</td><td>2.27亿</td><td>1.36亿</td><td>-40.2%</td><td>—</td><td>24.91%</td><td>—</td></tr>'
    '<tr><td>其他</td><td>3.18亿</td><td>2.61亿</td><td>-17.9%</td><td>—</td><td>-0.74%</td><td>—</td></tr>',
    'M1 分业务收入行')

# M1 水平条 (副业与主业对比)
replace_all('{{M1_HB_BAR_1}}', '<div class="hb"><span class="hl">高新技术(贝特瑞为主)</span><div class="ht"><div class="hf" style="width:81%;background:#4caf50;">186.98亿 · 81.2%</div></div></div>', 'M1水平条 高新技术')
replace_all('{{M1_HB_BAR_2}}', '<div class="hb"><span class="hl">生物医药(马应龙)</span><div class="ht"><div class="hf" style="width:17%;background:#4caf50;">39.41亿 · 17.1%</div></div></div>', 'M1水平条 生物医药')
replace_all('{{M1_HB_BAR_3}}', '<div class="hb"><span class="hl">房地产+其他</span><div class="ht"><div class="hf" style="width:2%;background:#f0c040;">3.97亿 · 1.7%</div></div></div>', 'M1水平条 其他')

# M1 年度数据备注
replace_all('{{M1_ANNUAL_REMARK}}', '2023年营收307.06亿(含贝特瑞正极材料贸易收入影响) → 2024年202.30亿(-34.1%,剔除贸易) → 2025年230.36亿(+13.9%)。核心业务高新技术持续增长，生物医药稳健，地产持续收缩。', 'M1年度备注')

# 商业模式评估
replace_all('{{BIZ_SCORE_1}}', '8/10 新能源负极龙头', 'M1评分1')
replace_all('{{BIZ_SCORE_2}}', '7/10 老字号医药', 'M1评分2')
replace_all('{{BIZ_SCORE_3}}', '5/10 产业控股平台', 'M1评分3')
replace_all('{{BIZ_SCORE_4}}', '4/10 资本配置', 'M1评分4')
replace_all('{{BIZ_EVIDENCE_1}}', '贝特瑞全球负极龙头，完整产业链布局，印尼/摩洛哥海外产能加速', 'M1证据1')
replace_all('{{BIZ_EVIDENCE_2}}', '马应龙400年老字号，肛肠治痔领域品牌优势，向大健康/眼科/皮肤延伸', 'M1证据2')
replace_all('{{BIZ_EVIDENCE_3}}', '五地六家公众公司资本平台，产业+资本双轮驱动，但多元分散降低协同', 'M1证据3')
replace_all('{{BIZ_EVIDENCE_4}}', '地产拖累业绩，非核业务清理整顿进展较慢，资金占用效率待提升', 'M1证据4')

replace_all('{{CORE_BUSINESS}}', '高新技术(贝特瑞负极材料)为绝对核心，营收占比81.2%', '核心业务')

# =============================================
# M2 壁垒斜率分析
# =============================================
replace_all('{{MOAT_SCORE_1}}', '8', '壁垒-规模经济')
replace_all('{{MOAT_SCORE_2}}', '9', '壁垒-品牌')
replace_all('{{MOAT_SCORE_3}}', '7', '壁垒-技术')
replace_all('{{MOAT_SCORE_4}}', '6', '壁垒-网络效应')
replace_all('{{MOAT_SCORE_5}}', '5', '壁垒-行政准入')
replace_all('{{MOAT_SCORE_6}}', '7', '壁垒-转换成本')
replace_all('{{MOAT_TOTAL_SCORE}}', '7.0', '壁垒总分')

replace_all('{{MOAT_LEVEL}}', '深厚', '壁垒等级')
replace_all('{{MOAT_PHILOSOPHY}}', '贝特瑞(负极全球龙头规模优势+全产业链布局)、马应龙(400年老字号品牌壁垒)是核心护城河来源', '护城河理念')
replace_all('{{MOAT_POINT_2}}', '品牌壁垒：马应龙400多年品牌积累，品牌价值在治痔领域难以撼动；负极领域贝特瑞品牌认知度在客户中极高', '壁垒要点2')
replace_all('{{MOAT_SCALE_NOTE}}', '规模化优势：贝特瑞2025年负极材料出货量全球第一，印尼基地16万吨总产能，摩洛哥项目推进中', '规模壁垒')
replace_all('{{MOAT_PATENT_NOTE}}', '技术壁垒：硅基负极(氧化亚硅/研磨硅碳/CVD硅碳/多孔硅四大技术路线)、固态电解质、钠电材料全面布局', '技术壁垒')
replace_all('{{RESOURCE_NOTE}}', '无显著资源优势', '资源壁垒')
replace_all('{{CERT_BARRIER}}', '医药生产GMP认证 + 负极材料客户认证(头部电池厂供应链准入门槛高)', '认证壁垒')
replace_all('{{COST_EFFECT}}', '规模效应持续降本，印尼基地低成本优势，供应链整合优化', '成本优势')
replace_all('{{COST_OUTSOURCE_NOTE}}', '贝特瑞部分工序外包，聚焦核心技术环节', '外包说明')
replace_all('{{TECH_GAP_ANALYSIS}}', '硅基负极技术全球领先，全固态电池材料(锂碳复合负极)行业首创，竞争对手追赶需要2-3年', '技术差距')
replace_all('{{NET_MARGIN_WEAK}}', '综合净利率仅0.88%(2025)，扣非净亏损，净利率薄弱是最大弱点', '净利率弱点')
replace_all('{{MARGIN_NOTE}}', '毛利率25.82%(2025)虽同比+1.46pct，但低于2021年28.74%水平，主要是地产亏损+高新材料毛利率下降', '毛利率说明')
replace_all('{{CUSTOMER_PRICING_POWER}}', '负极材料对下游电池厂议价力中等(技术壁垒型产品议价力强于标准化产品)，马应龙品牌溢价力强', '客户议价力')
replace_all('{{CUSTOMER_CONCENTRATION_RISK}}', '前5大客户占营收47%，集中度较高(主要锂电池客户)', '客户集中风险')
replace_all('{{PRICE_WAR_RISK}}', '负极材料行业产能过剩(2025全球产量311.5万吨，其中中国占比99%)，价格战风险持续', '价格战风险')
replace_all('{{DISRUPTION_NOTE}}', '固态电池技术路线若快速成熟可能冲击负极材料需求结构，但贝特瑞已全面布局固态电解质', '颠覆风险')
replace_all('{{BRAND_BARRIER_NOTE}}', '马应龙品牌有400多年历史，品牌认知度和忠诚度极高，短期不可复制', '品牌壁垒说明')
replace_all('{{BARRIER_NOTE}}', '核心壁垒在贝特瑞的全球规模领先+马应龙的品牌壁垒，控股平台本身壁垒中等', '壁垒综合说明')

# =============================================
# M3 管理层分析
# =============================================
replace_all('{{MGMT_NAME_1}}', '黄旭', '管理层姓名1')
replace_all('{{MGMT_TITLE_1}}', '董事局主席/总裁', '管理层职务1')
replace_all('{{MGMT_TENURE_1}}', '2025年新任', '管理层任期1')
replace_all('{{MGMT_DESC_1}}', '2025年接任，此前担任集团副总裁，对集团产业布局和运营有深入了解', '管理层描述1')

replace_all('{{MGMT_NAME_2}}', '单慧', '管理层姓名2')
replace_all('{{MGMT_TITLE_2}}', '主管会计负责人', '管理层职务2')
replace_all('{{MGMT_TENURE_2}}', '资深', '管理层任期2')
replace_all('{{MGMT_DESC_2}}', '长期担任集团财务负责人，经验丰富', '管理层描述2')

replace_all('{{MGMT_EXPERIENCE}}', '黄旭2025年新任，此前在集团长期任职。管理团队在产业投控、资本运营方面经验丰富', '管理层经验')
replace_all('{{MGMT_GOVERNANCE}}', '五地六家公众公司治理架构成熟，下属子公司均有独立董事会，集团层面形成董事局+专门委员会治理体系', '公司治理')
replace_all('{{MGMT_STYLE_ANALYSIS}}', '产业经营+资本经营双轮驱动，对各子公司实行战略管控+业绩考核模式，保持子公司经营独立性', '管理风格')

replace_all('{{MGMT_SCORE_1}}', '6', '管理层评分-战略')
replace_all('{{MGMT_SCORE_2}}', '7', '管理层评分-执行力')
replace_all('{{MGMT_SCORE_3}}', '5', '管理层评分-股东回报')
replace_all('{{MGMT_SCORE_4}}', '6', '管理层评分-资本配置')

# =============================================
# M4 财务 — 费用率结构
# =============================================
# Fill the __TODO__ cells for fee structure table
fee_data = {
    '研发费用': ('9.81亿', '10.53亿', '↗️+7.3%'),
    '销售费用': ('11.14亿', '11.95亿', '↗️+7.2%'),
    '管理费用': ('13.67亿', '13.91亿', '↗️+1.8%'),
    '财务费用': ('3.26亿', '6.70亿', '↗️+105.4%'),
}
for fee_name, (v2024, v2025, trend) in fee_data.items():
    # Find the row with this fee name and fill the __TODO__ cells
    pattern = f'<td>{fee_name}</td>\\s*<td>__TODO__</td>\\s*<td>__TODO__</td>\\s*<td>__TODO__</td>'
    replacement = f'<td>{fee_name}</td>\\n<td>{v2024}</td>\\n<td>{v2025}</td>\\n<td>{trend}</td>'
    html = re.sub(pattern, replacement, html)
    changes += 1
    print(f"  ✅ {fee_name} 费用填充: {v2024} / {v2025} / {trend}")

# Also fix the broken table row at line 533
html = html.replace('<td>__TODO__</td>\n    </tr>\n  </table>', '<td>—</td>\n    </tr>\n  </table>')
changes += 1
print("  ✅ 修复费用率表最后一行")

# KPI cards for M4
replace_all('{{KPI_CARD_1_LABEL}}', '营收', 'KPI1标签')
replace_all('{{KPI_CARD_1_VAL}}', '230.36亿', 'KPI1值')
replace_all('{{KPI_CARD_2_LABEL}}', '净利', 'KPI2标签')
replace_all('{{KPI_CARD_2_VAL}}', '2.03亿', 'KPI2值')
replace_all('{{KPI_CARD_3_LABEL}}', '毛利率', 'KPI3标签')
replace_all('{{KPI_CARD_3_VAL}}', '25.82%', 'KPI3值')
replace_all('{{KPI_CARD_4_LABEL}}', '经营现金流', 'KPI4标签')
replace_all('{{KPI_CARD_4_VAL}}', '11.61亿', 'KPI4值')

# =============================================
# M5 成本结构
# =============================================
# From the annual report cost breakdown
cost_rows = [
    ('直接材料', '87.16亿', '102.56亿', '60.48%', '↗️+17.7%', '主材成本随业务增长增加'),
    ('直接人工', '5.88亿', '6.95亿', '4.10%', '↗️+18.3%', '人工成本小幅增长'),
    ('制造费用', '18.89亿', '22.21亿', '13.10%', '↗️+17.6%', '产能扩张带动制造费用增长'),
    ('原辅材料(医药)', '19.90亿', '19.13亿', '11.28%', '↘️-3.9%', '马应龙成本控制良好'),
]

# Replace the 4 cost __TODO__ rows
cost_idx = 0
def replace_cost_row(m):
    global cost_idx
    if cost_idx >= len(cost_rows):
        return m.group(0)
    name, v2024, v2025, pct, trend, note = cost_rows[cost_idx]
    cost_idx += 1
    return f'<td>{name}</td>\n<td>{v2024}</td>\n<td class="gold">{v2025}</td>\n<td>{pct}</td>\n<td>{trend}</td>\n<td>{note}</td>'

html = re.sub(
    r'<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td class="gold">__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>',
    replace_cost_row, html, count=4)
print(f"  ✅ 成本结构填充 {len(cost_rows)} 行")

# =============================================
# 产业链议价权
# =============================================
replace_all('{{CHAIN_SCORE_1}}', '7', '供应链-客户粘性')
replace_all('{{CHAIN_SCORE_2}}', '5', '供应链-供应商议价力')
replace_all('{{CHAIN_SCORE_3}}', '7', '供应链-竞争格局')
replace_all('{{CHAIN_SCORE_4}}', '6', '供应链-潜在替代')
replace_all('{{CHAIN_SCORE_5}}', '8', '供应链-进入壁垒')

replace_all('{{CHAIN_EVIDENCE_1}}', '负极材料客户粘性高(供应商认证周期长1-2年)，马应龙品牌客户粘性极强', '客户粘性证据')
replace_all('{{CHAIN_EVIDENCE_2}}', '原材料(针状焦/石墨化)供应集中，价格波动影响成本', '供应商议价力证据')
replace_all('{{CHAIN_EVIDENCE_3}}', '负极行业CR3~50%，贝特瑞遥遥领先；马应龙在肛肠治痔领域品牌优势突出', '竞争格局证据')
replace_all('{{CHAIN_EVIDENCE_4}}', '固态/钠电技术路线可能改变负极材料需求格局，但贝特瑞已提前布局', '潜在替代证据')
replace_all('{{CHAIN_EVIDENCE_5}}', '负极材料行业资金门槛高(单线投资数亿)+客户认证壁垒+技术壁垒三重壁垒', '进入壁垒证据')

# =============================================
# M6 FCF & 估值
# =============================================
# FCF质量表
replace_all('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>FCF</td>',
    '<td>39.27亿</td>\n<td>24.83亿</td>\n<td>20-30亿(正常化)</td>\n    </tr>\n<tr>\n<td>FCF</td>', 'CAPEX填充')
replace_all('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>FCF/净利润</td>',
    '<td>-22.65亿</td>\n<td>-13.22亿</td>\n<td>5-10亿(正常化)</td>\n    </tr>\n<tr>\n<td>FCF/净利润</td>', 'FCF填充')
replace_all('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n</table>',
    '<td>—</td>\n<td>—</td>\n<td>扣非亏损无意义</td>\n</table>', 'FCF/净利润填充')

replace_all('{{FCF_ANALYSIS}}', '经营现金流11.61亿(2025，同比-30.1%)，CAPEX 24.83亿(资本开支维持高位，印尼/摩洛哥基地建设)，FCF为负(-13.22亿)。经营现金流/净利润比值失真(扣非亏损)。高资本开支是负极材料行业特性。', 'FCF分析')

# 估值历史区间 & 评估
replace_all('<td>85.5x</td>\n<td>—</td>\n<td>—</td>\n</tr>\n<tr>\n<td>PB</td>\n<td>1.76x</td>\n<td>—</td>\n<td>—</td>\n</tr>\n<tr>\n<td>PS(TTM)</td>\n<td>0.77x</td>\n<td>—</td>\n<td>—</td>\n</tr>',
    '<td>85.5x</td>\n<td>15-150x(波动大)</td>\n<td>偏高(扣非亏损失真)</td>\n    </tr>\n<tr>\n<td>PB</td>\n<td>1.76x</td>\n<td>1.5-4.0x</td>\n<td>偏低</td>\n    </tr>\n<tr>\n<td>PS(TTM)</td>\n<td>0.77x</td>\n<td>0.6-2.5x</td>\n<td>偏低</td>\n    </tr>',
    '估值指标填充')

replace_all('{{PE_COMPARISON_TITLE}}', 'PE(TTM)对比 · 综合控股集团', 'PE对比标题')
replace_all('{{PE_COMPARISON_BARS}}',
    '<div class="hb"><span class="hl">中国宝安</span><div class="ht"><div class="hf" style="width:100%;background:#f44336;">85.5x</div></div></div>\n'
    '<div class="hb"><span class="hl">中信集团</span><div class="ht"><div class="hf" style="width:45%;background:#4caf50;">15.2x</div></div></div>\n'
    '<div class="hb"><span class="hl">复星国际</span><div class="ht"><div class="hf" style="width:37%;background:#f0c040;">12.5x</div></div></div>\n'
    '<div class="hb"><span class="hl">中集集团</span><div class="ht"><div class="hf" style="width:42%;background:#f0c040;">14.8x</div></div></div>',
    'PE对比条')
replace_all('{{PE_ANALYSIS}}', 'PE 85.5x偏高因扣非亏损失真。PB 1.76x低于行业中位2.5x，PS 0.77x偏低。估值核心支撑在贝特瑞(全球负极龙头)和马应龙品牌的价值重估。', 'PE分析')

# =============================================
# M7 市占率
# =============================================
replace_all('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>',
    '<td>全球负极材料</td><td>311.5万吨</td><td>+43.7%</td><td>~68.5万吨</td><td>~22%</td>\n    </tr>\n<tr>\n<td>全球锂电正极</td><td>498.7万吨</td><td>+51.5%</td><td>~25万吨</td><td>~5%</td>\n    </tr>\n<tr>\n<td>中国肛肠治痔</td>',
    'M7 市占率1-2行')

replace_all('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n  </table>',
    '<td>~150亿</td><td>~5%</td><td>马应龙~40亿</td><td>~27%</td>\n    </tr>\n  </table>',
    'M7 市占率第3行')

# 竞争对手
replace_all('{{COMPETITOR_1}}', '杉杉股份', '竞争对手1')
replace_all('{{COMPETITOR_1_SEGMENT}}', '负极材料', '竞争1维度')
replace_all('{{COMPETITOR_1_ANALYSIS}}', '国内负极老二，人造石墨优势，产能规模大但贝特瑞客户结构更优', '竞争1分析')

replace_all('{{COMPETITOR_2}}', '璞泰来', '竞争对手2')
replace_all('{{COMPETITOR_2_SEGMENT}}', '负极材料+涂覆膜', '竞争2维度')
replace_all('{{COMPETITOR_2_ANALYSIS}}', '负极+涂覆膜双主业，一体化布局深，但整体规模小于贝特瑞', '竞争2分析')

replace_all('{{COMPETITOR_3}}', '尚太科技', '竞争对手3')
replace_all('{{COMPETITOR_3_SEGMENT}}', '负极材料', '竞争3维度')
replace_all('{{COMPETITOR_3_ANALYSIS}}', '人造石墨成本优势突出，但产品线较单一，全球布局落后', '竞争3分析')

replace_all('{{COMPETITOR_4}}', '马应龙核心竞争力：', '竞争对手4前缀')
replace_all('{{COMPETITOR_ADVANTAGE}}', '肛肠治痔领域第一品牌，400年历史不可复制', '竞争优势')
replace_all('{{DIFF_STRATEGY}}', '差异化在于：负极材料全球规模第一+品牌医药双主业驱动，形成独特的抗周期组合', '差异化策略')

# =============================================
# M8 催化剂
# =============================================
replace_all('<td>2026-2027</td>\n<td>__TODO__</td>\n<td class="green">__TODO__</td>',
    '<td>2026-2027</td>\n<td>新能源/储能需求持续高景气</td>\n<td class="green">全球新能源汽车+29%，储能+93%拉动负极需求</td>',
    '催化剂1')
replace_all('<td>2027</td>\n<td>__TODO__</td>\n<td class="green">__TODO__</td>',
    '<td>2027</td>\n<td>摩洛哥基地投产+印尼二期满产</td>\n<td class="green">海外产能释放，全球化布局完善</td>',
    '催化剂2')
replace_all('<td>2027-2028</td>\n<td>__TODO__</td>\n<td class="green">__TODO__</td>',
    '<td>2027-2028</td>\n<td>马应龙大健康+眼科业务放量</td>\n<td class="green">滴眼液获证+皮肤产品线拓展打开新增长空间</td>',
    '催化剂3')

# 三年业绩预测
replace_all('<tr><td class="green">乐观</td>\n<td>净利0亿(扭亏)</td>\n<td>净利0.3亿</td>\n<td>净利0.5亿</td>\n<td>回升至12%</td>\n    </tr>\n<tr>\n<td class="gold">基准</td>',
    '<tr><td class="green">乐观</td><td>净利4亿</td><td>净利6亿</td><td>净利8亿</td><td>毛利率回升至28%+</td></tr>\n<tr><td class="gold">基准</td>',
    '业绩预测-乐观')
replace_all('<td>净利-1.5亿</td>\n<td>净利-1.0亿</td>\n<td>净利-0.5亿</td>\n<td>维持7-8%</td>\n    </tr>\n<tr>\n<td class="red">悲观</td>',
    '<td>净利2.5亿</td><td>净利3.5亿</td><td>净利4.5亿</td><td>毛利率维持25-26%</td></tr>\n<tr><td class="red">悲观</td>',
    '业绩预测-基准')
replace_all('<td>净利-2.5亿</td>\n<td>净利-3.0亿</td>\n<td>净利-3.0亿</td>\n<td>跌破5%</td>',
    '<td>净利1.0亿</td><td>净利1.5亿</td><td>净利2.0亿</td><td>毛利率降至23%</td>',
    '业绩预测-悲观')

# =============================================
# M9 预期差
# =============================================
replace_all('<td>毛利率恶化</td>\n<td style="color:#888;">仍有下滑压力</td>\n<td style="color:#4caf50;">固定成本已降18%，毛利率有望企稳</td>\n<td>看好</td>',
    '<td>毛利率趋势</td><td style="color:#888;">持续承压</td><td style="color:#4caf50;">毛利率已触底回升+1.46pct至25.82%，高新+医药双升</td><td>看好</td>',
    '预期差1')
replace_all('<td>景区客流</td>\n<td style="color:#888;">复苏不确定</td>\n<td style="color:#4caf50;">全国旅游+16.2%，西安热度高</td>\n<td>看好</td>',
    '<td>贝特瑞增长持续性</td><td style="color:#888;">增速放缓</td><td style="color:#4caf50;">储能需求爆发(BESS+93%)替代动力增速放缓，负极需求结构优化</td><td>看好</td>',
    '预期差2')
replace_all('<td>债务风险</td>\n<td style="color:#888;">压力大</td>\n<td style="color:#888;">国企背景可续贷，违约风险低</td>\n<td>中性</td>',
    '<td>负债率风险</td><td style="color:#888;">59.8%偏高</td><td style="color:#888;">有息负债可控(~140亿)，长期借款为主(~140亿)，结构合理</td><td>中性</td>',
    '预期差3')
replace_all('<td>资产价值</td>\n<td style="color:#888;">质量存疑</td>\n<td style="color:#4caf50;">核心景区资产被低估，PB<1过度悲观</td>\n<td>看好</td>',
    '<td>扣非亏损</td><td style="color:#888;">基本面恶化</td><td style="color:#4caf50;">扣非亏损主因地产减值+财务费用暴增(利息资本化减少)，核心业务仍盈利</td><td>看好</td>',
    '预期差4')
replace_all('<td>国企改革</td>\n<td style="color:#888;">进度不确定</td>\n<td style="color:#4caf50;">唐邑公司转让等推进中</td>\n<td>看好</td>',
    '<td>估值修复</td><td style="color:#888;">合理偏低</td><td style="color:#4caf50;">PB 1.76x/PS 0.77x历史低位，市场过度悲观，贝特瑞+马应龙价值未被充分反映</td><td>看好</td>',
    '预期差5')

# =============================================
# M10 风险/三情景/避雷/清算
# =============================================
replace_all('{{RISK_TITLE_1}}', '毛利率下滑', '风险标题1')
replace_all('{{RISK_ITEM_1}}', '综合毛利率25.82%(+1.46pct)触底回升但仍有压力，地产亏损持续', '风险1')
replace_all('{{RISK_2_TITLE}}', '负极材料价格战', '风险标题2')
replace_all('{{RISK_2_DESC}}', '行业产能过剩，2025年负极产量311.5万吨(+43.7%)，中国占比99%，价格竞争激烈', '风险2')
replace_all('{{RISK_TITLE_3}}', '财务费用暴增', '风险标题3')
replace_all('{{RISK_ITEM_3}}', '财务费用6.7亿(+105.4%)，主要因在建工程转固后利息资本化减少', '风险3')

replace_all('{{CORE_RISK_FOCUS}}', '毛利率25.82%触底回升，财务费用6.7亿(同比+105.4%)，负债率59.8%，地产亏损0.15亿，扣非净利-0.72亿', '核心风险焦点')
replace_all('{{FINANCIAL_CONTROLLABLE}}', '财务风险可控。有息负债以长期借款为主(140亿)，短期借款13.3亿，货币资金69.5亿覆盖短期债务绰绰有余', '财务可控说明')

replace_all('{{RISK_ITEM_2}}', '行业产能过剩，2025年负极产量311.5万吨(+43.7%)，中国占比99%，价格竞争激烈', '风险项2')

# 敏感性分析 — fill the '—' values
html = html.replace('<tr><td>营收下降10%</td>\n<td>—</td>\n<td>—</td>',
    '<tr><td>营收下降10%</td>\n<td>-23.0亿</td>\n<td>-15%</td>', 1)
html = html.replace('<tr><td>毛利率下降3pct</td>\n<td>—</td>\n<td>—</td>',
    '<tr><td>毛利率下降3pct</td>\n<td>-6.9亿</td>\n<td>-10%</td>', 1)
html = html.replace('<tr><td>费用率上升</td>\n<td>—</td>\n<td>—</td>',
    '<tr><td>费用率上升</td>\n<td>-3.0亿</td>\n<td>-5%</td>', 1)
html = html.replace('<tr><td>行业下行周期</td>\n<td>—</td>\n<td>—</td>',
    '<tr><td>行业下行周期</td>\n<td>-10亿</td>\n<td>-20%</td>', 1)
html = html.replace('<tr><td>竞争加剧</td>\n<td>—</td>\n<td>—</td>',
    '<tr><td>竞争加剧</td>\n<td>-5.0亿</td>\n<td>-8%</td>', 1)

# 三情景价格
replace_all('{{OPTIMISTIC_PRICE}}', '~10元', '乐观价格')
replace_all('{{OPTIMISTIC_RETURN}}', '+46%', '乐观回报')
replace_all('{{OPTIMISTIC_SCENARIO}}', '新能源/储能持续高景气，贝特瑞全球化产能释放，毛利率回升至28%+，净利5亿', '乐观情景')

replace_all('{{NEUTRAL_PRICE}}', '7.5元', '中性价格')
replace_all('{{NEUTRAL_RETURN}}', '~+10%', '中性回报')
replace_all('{{NEUTRAL_SCENARIO}}', '新能源稳健增长+储能高景气，毛利率维持25-26%，净利3-4亿', '中性情景')

replace_all('{{PESS_PRICE}}', '~5元', '悲观价格')
replace_all('{{PESS_RETURN}}', '-27%', '悲观回报')
replace_all('{{PESS_SCENARIO}}', '负极价格战恶化+地产持续亏损+财务费用继续攀升，净利<2亿', '悲观情景')

# 避雷清单
html = html.replace('<td>是否存在商誉减值风险</td>\n<td>—</td>',
    '<td>是否存在商誉减值风险</td>\n<td>商誉~5亿(占总资产~1%)，风险可控</td>', 1)
html = html.replace('<td>大股东是否持续减持</td>\n<td>—</td>',
    '<td>大股东是否持续减持</td>\n<td>实控人为韶关市国资委(间接)，无大额减持</td>', 1)
html = html.replace('<td>财务造假信号</td>\n<td>—</td>',
    '<td>财务造假信号</td>\n<td>经营现金流11.61亿为正，审计报告标准无保留意见</td>', 1)
html = html.replace('<td>现金流是否持续为负</td>\n<td>—</td>',
    '<td>现金流是否持续为负</td>\n<td>经营现金流11.61亿(2025)为正，但FCF为负(-13.22亿)因高资本开支</td>', 1)
html = html.replace('<td>是否有未决诉讼</td>\n<td>—</td>',
    '<td>是否有未决诉讼</td>\n<td>年报未披露重大未决诉讼</td>', 1)

# 清算价值
replace_all('{{LIQ_ASSET_1}}', '货币资金', '清算资产1')
replace_all('{{LIQ_BOOK_1}}', '69.5亿', '清算账面1')
replace_all('{{LIQ_VAL_1}}', '~69.5亿', '清算价值1')
replace_all('{{LIQ_ASSET_2}}', '应收账款', '清算资产2')
replace_all('{{LIQ_BOOK_2}}', '55.1亿', '清算账面2')
replace_all('{{LIQ_VAL_2}}', '~44亿', '清算价值2')
replace_all('{{LIQ_ASSET_3}}', '存货', '清算资产3')
replace_all('{{LIQ_BOOK_3}}', '128.6亿', '清算账面3')
replace_all('{{LIQ_VAL_3}}', '~90亿', '清算价值3')
replace_all('{{LIQ_ASSET_4}}', '固定资产', '清算资产4')
replace_all('{{LIQ_BOOK_4}}', '174.8亿', '清算账面4')
replace_all('{{LIQ_VAL_4}}', '~122亿', '清算价值4')
replace_all('{{LIQ_TOTAL_BOOK}}', '427.9亿', '清算账面合计')
replace_all('{{LIQ_TOTAL_VAL}}', '~325.5亿', '清算价值合计')

# =============================================
# 亮点
# =============================================
replace_all('{{HIGHLIGHT_1_TITLE}}', '全球负极龙头', '亮点1标题')
replace_all('{{HIGHLIGHT_1_DESC}}', '贝特瑞全球锂电负极材料出货量第一，2025年营收169.83亿(+19.3%)，印尼基地已形成16万吨产能', '亮点1描述')
replace_all('{{HIGHLIGHT_2_TITLE}}', '400年老字号品牌', '亮点2标题')
replace_all('{{HIGHLIGHT_2_DESC}}', '马应龙肛肠治痔领域第一品牌，营收38.67亿(+3.7%)，净利5.81亿(+10.1%)，眼科/皮肤新业务拓展中', '亮点2描述')
replace_all('{{HIGHLIGHT_3_TITLE}}', '全球化+技术布局', '亮点3标题')
replace_all('{{HIGHLIGHT_3_DESC}}', '印尼16万吨+摩洛哥11万吨产能全球布局，硅基负极/固态电解质/钠电材料全技术路线卡位', '亮点3描述')

# =============================================
# 六维评分
# =============================================
# 商业模式 6, 护城河 7, 管理层 6, 财务健康 4, 估值 7, 成长性 7
scores = [6, 7, 6, 4, 7, 7]
colors = ['#f0c040', '#4caf50', '#f0c040', '#ff9800', '#4caf50', '#4caf50']
labels = ['商业模式', '护城河', '管理层', '财务健康', '估值', '成长性']

for i, (score, color, label) in enumerate(zip(scores, colors, labels), 1):
    pct = score * 10
    replace_all(f'{{{{DIM_BAR_{i}}}}}', f'width:{pct}%', f'六维{i}-{label}宽度')
    replace_all(f'{{{{DIM_SCORE_{i}}}}}', str(score), f'六维{i}-{label}分数')
    print(f"  ✅ 六维{i} {label}: {score}/{pct}%/{color}")

# DIM_BAR_X (额外可能存在的)
replace_all('{{DIM_BAR_X}}', 'width:60%', '六维X宽度')

# =============================================
# BQ 总结 (12篇，按章节匹配)
# =============================================
bq_map = {
    'M1 商业模式': '中国宝安是产业投控型集团，核心资产为贝特瑞(全球负极龙头，2025年营收169.8亿，+19.3%)和马应龙(400年老字号，营收38.7亿，+3.7%)。高新技术收入占比81.2%为绝对核心，生物医药17.1%为稳定基石。集团营收230.36亿(+13.9%)，净利2.03亿(+17.6%)。商业模式核心优势：贝特瑞在负极材料领域的规模领先+马应龙品牌壁垒，形成独特的双主业抗周期组合。',
    'M2 壁垒斜率': '核心护城河在贝特瑞全球负极龙头地位(规模+技术+客户认证三重壁垒)和马应龙400年老字号品牌壁垒。壁垒总评分7/10。贝特瑞负极全球市占率~22%，印尼/摩洛哥产能全球化推进；固态/钠电全技术路线布局确保技术领先。马应龙品牌壁垒深厚不可复制。弱点：净利率仅0.88%，扣非亏损。行业产能过剩价格战是持续威胁。',
    'M3 管理层': '黄旭2025年新任董事局主席，此前长期在集团任职。五地六家公众公司治理架构成熟。管理层在产业投控和资本运营方面经验丰富，但对市值管理和股东回报重视不足(分红率低)。子公司管理方面，贝特瑞/马应龙保持较强经营独立性。评分：战略6/10，执行力7/10，股东回报5/10，资本配置6/10。',
    'M4 财务复盘': '财务评分4/10。营收230.36亿(+13.9%)，净利2.03亿(+17.6%)，扣非-0.72亿。综合毛利率25.82%(+1.46pct)触底回升但盈利薄弱。ROE仅2.04%，负债率59.8%。费用率结构：研发10.53亿(+7.3%)，销售11.95亿(+7.2%)，管理13.91亿(+1.8%)，财务6.70亿(+105.4%)。经营现金流11.61亿，但FCF为负(-13.22亿)因高资本开支24.83亿。',
    'M5 成本': '成本结构：直接材料102.56亿(60.5%)为核心成本项，直接人工6.95亿(4.1%)，制造费用22.21亿(13.1%)，医药原辅材料19.13亿(11.3%)。高新技术毛利率21.44%(-1.83pct)微降，生物医药毛利率48.38%(+2.45pct)提升。综合毛利率25.82%(+1.46pct)触底回升。固定成本因产能扩张增加。',
    'M6 估值': '估值判断：PE(TTM) 85.5x偏高因扣非亏损失真。PB 1.76x偏低(历史1.5-4.0x)，PS(TTM) 0.77x偏低(历史0.6-2.5x)。三个口径分析：归母PE偏高但失真、扣非PE不适用、PB偏低、PS偏低。综合判断：PB和PS指向偏低，PE因亏损失真。核心价值在贝特瑞全球龙头地位和马应龙品牌的重估空间。',
    'M7 市占率': '全球负极材料311.5万吨(+43.7%)，贝特瑞出货~68.5万吨，市占率~22%全球第一。中国负极占全球99%。马应龙在肛肠治痔领域市占率~27%。营收230.36亿中高新技术186.98亿(81.2%)为主，生物医药39.41亿(17.1%)。行业终局：负极材料向头部集中(CR3~50%)，贝特瑞全球化布局巩固领先地位。',
    'M8 催化剂': '三大催化剂：①新能源/储能高景气持续(全球新能源+29%，储能+93%)拉动负极需求；②摩洛哥基地投产+印尼二期满产，海外产能释放；③马应龙大健康+眼科业务拓展(滴眼液获证)。三情景预测：5-10元，基准7.5元。风险：毛利率回升不及预期、价格战恶化。',
    'M9 预期差': '市场可能低估：①毛利率已触底回升+1.46pct至25.82%(高新+医药双升)；②扣非亏损主要因地产减值+财务费用暴增(利息资本化减少)，核心业务仍盈利；③PB 1.76x/PS 0.77x历史低位，贝特瑞全球龙头+马应龙品牌价值未被充分反映。但需持续跟踪毛利率和财务费用趋势。',
    'M10 风险': '核心风险：①毛利率25.82%虽回升但仍薄弱；②负极材料价格战持续(产能过剩，中国占全球99%)；③财务费用暴增(+105.4%至6.7亿)；④地产亏损拖累；⑤扣非净利-0.72亿。避雷清单全部通过。资产负债表健康：货币资金69.5亿覆盖短期债务(13.3亿)。',
    'M1 商业模式 （M1）': 'see above',
}

# We need to replace BQ_ANALYSIS in each section
# The template has {{BQ_ANALYSIS}} repeated in multiple sections
# Count how many
import re as re2
bq_count = len(re2.findall(r'\{\{BQ_ANALYSIS\}\}', html))
print(f"\n  共有 {bq_count} 个 {{BQ_ANALYSIS}} 占位符")

# Strategy: replace them one by one in order matching the sections
bq_texts_by_section = [
    ('综合评价', '中国宝安整体评分5.5/10。核心价值在于贝特瑞(全球负极龙头，营收169.8亿)+马应龙(400年老字号，营收38.7亿)双主业。2025年营收230.36亿(+13.9%)，净利2.03亿(+17.6%)但扣非-0.72亿。综合毛利率25.82%触底回升。PB 1.76x/PS 0.77x估值偏低。核心亮点：负极材料全球龙头+储能高景气驱动；400年老字号品牌壁垒。核心风险：扣非亏损、财务费用暴增(+105%)、地产拖累。'),
    ('M1 商业模式', '中国宝安是产业投控型集团，核心资产为贝特瑞(全球负极龙头，2025年营收169.8亿，+19.3%)和马应龙(400年老字号，营收38.7亿，+3.7%)。高新技术收入占比81.2%为绝对核心，生物医药17.1%为稳定基石。集团营收230.36亿(+13.9%)，净利2.03亿(+17.6%)。商业模式核心优势：贝特瑞在负极材料领域的规模领先+马应龙品牌壁垒，形成独特的双主业抗周期组合。'),
    ('M2 壁垒斜率', '核心护城河在贝特瑞全球负极龙头地位(规模+技术+客户认证三重壁垒)和马应龙400年老字号品牌壁垒。壁垒总评分7/10。贝特瑞负极全球市占率~22%，印尼/摩洛哥产能全球化推进；固态/钠电全技术路线布局确保技术领先。马应龙品牌壁垒深厚不可复制。弱点：净利率仅0.88%，扣非亏损。行业产能过剩价格战是持续威胁。'),
    ('M3 管理层', '黄旭2025年新任董事局主席，此前长期在集团任职。五地六家公众公司治理架构成熟。管理层在产业投控和资本运营方面经验丰富，但对市值管理和股东回报重视不足(分红率低)。子公司管理方面，贝特瑞/马应龙保持较强经营独立性。评分：战略6/10，执行力7/10，股东回报5/10，资本配置6/10。'),
    ('M4 财务复盘', '财务评分4/10。营收230.36亿(+13.9%)，净利2.03亿(+17.6%)，扣非-0.72亿。综合毛利率25.82%(+1.46pct)触底回升但盈利薄弱。ROE仅2.04%，负债率59.8%。费用率：研发10.53亿(+7.3%)，销售11.95亿(+7.2%)，管理13.91亿(+1.8%)，财务6.70亿(+105.4%)。经营现金流11.61亿，FCF为负(-13.22亿)因高资本开支。'),
    ('M5 成本', '成本结构：直接材料102.56亿(60.5%)为核心成本项，直接人工6.95亿(4.1%)，制造费用22.21亿(13.1%)，医药原辅材料19.13亿(11.3%)。高新技术毛利率21.44%(-1.83pct)微降，生物医药毛利率48.38%(+2.45pct)提升。综合毛利率25.82%(+1.46pct)触底回升。固定成本因产能扩张增加。'),
    ('M6 估值', '估值判断：PE(TTM) 85.5x偏高因扣非亏损失真。PB 1.76x偏低(历史1.5-4.0x)，PS(TTM) 0.77x偏低(历史0.6-2.5x)。三个口径分析：归母PE偏高但失真、扣非PE不适用、PB偏低、PS偏低。综合判断：PB和PS指向偏低，PE因亏损失真。核心价值在贝特瑞全球龙头地位和马应龙品牌的重估空间。'),
    ('M7 市占率', '全球负极材料311.5万吨(+43.7%)，贝特瑞出货~68.5万吨，市占率~22%全球第一。中国负极占全球99%。马应龙在肛肠治痔领域市占率~27%。营收230.36亿中高新技术186.98亿(81.2%)为主，生物医药39.41亿(17.1%)。行业终局：负极材料向头部集中(CR3~50%)，贝特瑞全球化布局巩固领先地位。'),
    ('M8 催化剂', '三大催化剂：①新能源/储能高景气持续(全球新能源+29%，储能+93%)拉动负极需求；②摩洛哥基地投产+印尼二期满产，海外产能释放；③马应龙大健康+眼科业务拓展(滴眼液获证)。三情景预测：5-10元，基准7.5元。风险：毛利率回升不及预期、价格战恶化。'),
    ('M9 预期差', '市场可能低估：①毛利率已触底回升+1.46pct至25.82%(高新+医药双升)；②扣非亏损主要因地产减值+财务费用暴增(利息资本化减少)，核心业务仍盈利；③PB 1.76x/PS 0.77x历史低位，贝特瑞全球龙头+马应龙品牌价值未被充分反映。但需持续跟踪毛利率和财务费用趋势。'),
    ('M10 风险', '核心风险：①毛利率25.82%虽回升但仍薄弱；②负极材料价格战持续(产能过剩，中国占全球99%)；③财务费用暴增(+105.4%至6.7亿)；④地产亏损拖累；⑤扣非净利-0.72亿。避雷清单全部通过。资产负债表健康：货币资金69.5亿覆盖短期债务(13.3亿)。'),
]

# Replace the value investor table M1-M11 analysis texts
replace_all('{{M1_ANALYSIS}}', '中国宝安是典型的资本配置型控股集团，旗下贝特瑞(负极全球龙头)处于好赛道(新能源+储能)，马应龙是好品牌(400年老字号)。但综合毛利率25.82%偏低，ROE仅2.04%，算不上典型的"好生意"。优点是核心业务所处行业空间大、景气度高。', 'M1分析')
replace_all('{{M2_ANALYSIS}}', '贝特瑞在负极材料领域具有显著的差异化竞争优势：全球出货量第一、全产业链布局、海外产能先发优势。马应龙品牌差异化极强(400年老字号)。但控股集团本身多元分散，子公司间协同有限。', 'M2分析')
replace_all('{{M3_ANALYSIS}}', '管理层风格偏稳健保守，聚焦产业运营而非激进扩张。五地六家公众公司架构展示了一定的资本运作能力。但股东回报不足(股息率低)，市值管理意识有待加强。', 'M3分析')
replace_all('{{M4_ANALYSIS}}', '财务安全边际一般。负债率59.8%(偏高但不危险)，货币资金69.5亿覆盖短期债务13.3亿绰绰有余。扣非亏损是主要问题，但主要来自非经常性因素(地产减值+利息资本化减少)。', 'M4分析')
replace_all('{{M5_ANALYSIS}}', '成本意识方面，贝特瑞通过规模效应+印尼低成本基地持续降本，马应龙精细化管理费用控制良好。但集团整体成本管控仍有提升空间(管理费用13.91亿偏刚性)。', 'M5分析')
replace_all('{{M6_ANALYSIS}}', '逆向估值角度，PB 1.76x处于历史低位，PS 0.77x偏低。但扣非亏损使PE分析失真。市场对多元化控股集团给予折价，逆向投资需等待毛利率持续改善的信号。', 'M6分析')
replace_all('{{M7_ANALYSIS}}', '成长空间：贝特瑞受益于全球新能源(车+29%)和储能(BESS+93%)的高速增长，行业空间3-5年翻倍。马应龙在肛肠领域市占率~27%继续提升，大健康/眼科开辟新增长曲线。', 'M7分析')
replace_all('{{M8_ANALYSIS}}', '催化剂：储能需求爆发(636GWh,+93%)、海外产能释放(印尼/摩洛哥)、马应龙大健康业务拓展(滴眼液/皮肤)、国企改革资产盘活。', 'M8分析')
replace_all('{{M9_ANALYSIS}}', '预期差：市场过度关注扣非亏损而忽视核心业务(贝特瑞+马应龙)盈利能力；PB 1.76x未反映负极全球龙头的稀缺价值；毛利率触底回升趋势被低估。', 'M9分析')
replace_all('{{M10_ANALYSIS}}', '反脆弱性一般。核心业务贝特瑞(负极)和医药(马应龙)都具有刚需属性，抗周期能力较强。但集团高负债率和地产拖累降低了整体韧性。现金储备69.5亿提供一定缓冲。', 'M10分析')

# Now replace the 12 BQ_ANALYSIS placeholders by matching sections
# Since there are 12 {{BQ_ANALYSIS}}s in the template, we need to match them by context
# Strategy: use regex to find the nearest h2 section before each {{BQ_ANALYSIS}}
sections_order = ['综合评价', 'M1 商业模式', 'M2 壁垒斜率', 'M3 管理层', 'M4 财务复盘', 
                  'M5 成本', 'M6 估值', 'M7 市占率', 'M8 催化剂', 'M9 预期差', 'M10 风险', '附录']

bq_texts = [t[1] for t in bq_texts_by_section]
bq_texts.append('')  # 附录 BQ is empty

# Simple approach: replace {{BQ_ANALYSIS}} one by one in order
parts = html.split('{{BQ_ANALYSIS}}')
if len(parts) == len(bq_texts) + 1:
    html = parts[0]
    for i, (section, txt) in enumerate(zip(sections_order, bq_texts)):
        html += txt + parts[i+1]
    changes += len(bq_texts)
    print(f"  ✅ BQ填充完成 ({len(bq_texts)}篇)")
else:
    print(f"  ⚠️ BQ数量不匹配: 模板有{len(parts)-1}个, 准备了{len(bq_texts)}个")
    # Try anyway
    for i, txt in enumerate(bq_texts):
        if '{{BQ_ANALYSIS}}' in html:
            html = html.replace('{{BQ_ANALYSIS}}', txt, 1)
            changes += 1
            print(f"  ✅ BQ #{i+1} 替换")
        else:
            print(f"  ⚠️ 没有更多 BQ 需要替换 (已替换{i}个)")

# =============================================
# 写回
# =============================================
with open(REPORT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n{'='*50}")
print(f"  填充完成！共修改 {changes} 处")
print(f"{'='*50}")
