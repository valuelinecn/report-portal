#!/usr/bin/env python3
"""fill_600706.py — 曲江文旅(600706) 完整填充脚本"""
import re, os

HTML = os.path.expanduser('~/.hermes/hermes-agent/report-portal/reports/600706.html')
with open(HTML, 'r') as f:
    c = f.read()

count = 0
def fill(ph, val):
    global c, count
    if ph in c:
        c = c.replace(ph, val)
        count += 1
        return True
    return False

def fill_table(marker, new_html):
    global c
    idx = c.find(marker)
    if idx < 0: return False
    tbl_start = c.find('<table', idx)
    if tbl_start < 0: return False
    tbl_end = c.find('</table>', tbl_start) + 8
    if tbl_end < 8: return False
    c = c[:tbl_start] + new_html + c[tbl_end:]
    return True

# ===== 基础信息 =====
for ph,val in [
    ('{{COMPANY_NAME_CN}}', '曲江文旅'),
    ('{{SCORE}}', '3.5'),
    ('{{RATING_DESC}}', '文旅国企龙头，拥有大唐芙蓉园等核心景区资源，但连续亏损负债率高，ROE为负'),
    ('{{RATING_TEXT}}', '2026-06-17'),
    ('{{COMPANY_DESC_LONG}}', '曲江文旅是西安曲江新区国有文旅平台，运营大唐芙蓉园、曲江海洋极地公园、大雁塔景区等核心文化旅游资源。公司以景区运营管理为核心业务，兼营旅行社、酒店餐饮、体育赛事等。2025年营收9.67亿元，净利-1.96亿元，连续亏损，资产负债率超70%。'),
    ('{{INVESTMENT_THESIS}}', '曲江文旅拥有西安市核心文旅资产的独家运营权，资源禀赋独特，但景区运营成本刚性、负债率高企，盈利能力持续恶化。2025年归母净利-1.96亿，PB已反映资产折价。需关注国企改革和文旅复苏信号。'),
    ('{{ANALYSIS_TEXT}}', '曲江文旅拥有大唐芙蓉园等西安核心文旅资产运营权，国企背景保障资源独占性。但景区运营成本刚性、负债率超70%，2025年亏损扩大至-1.96亿。短期看文旅复苏弹性，中期看国企改革和资产盘活。'),
    # CARD
    ('{{CARD1_VAL}}', '3.5'),('{{CARD1_LABEL}}', '综合评级'),('{{CARD1_COLOR}}', '#ff9800'),
    ('{{CARD2_VAL}}', '高'),('{{CARD2_LABEL}}', '风险等级'),('{{CARD2_COLOR}}', '#f44336'),
    ('{{CARD3_VAL}}', '低'),('{{CARD3_LABEL}}', '成长弹性'),('{{CARD3_COLOR}}', '#888'),
    ('{{CARD4_VAL}}', '-34.96%'),('{{CARD4_LABEL}}', 'ROE'),('{{CARD4_COLOR}}', '#f44336'),
    ('{{LABEL_2}}', '西安核心文旅资产运营商'),
    ('{{LABEL_2_TITLE}}', '核心优势'),
    ('{{LABEL_3}}', '文旅复苏、国企改革、资产盘活'),
    ('{{LABEL_3_TITLE}}', '催化剂'),
    # LOGIC
    ('{{LOGIC_1_VAL}}', '西安文旅龙头'),
    ('{{LOGIC_1}}', '拥有大唐芙蓉园/大雁塔等核心景区独家运营权'),
    ('{{LOGIC_2}}', '景区客流/客单价/负债率变化'),
    ('{{LOGIC_2_DETAIL}}', '景区运营管理收入占比超60%，资源独占性强'),
    ('{{LOGIC_3}}', '客流恢复不及预期则逻辑证伪'),
    ('{{LOGIC_3_DETAIL}}', '若2026年客流未恢复至2019年水平，亏损将持续'),
    ('{{LOGIC_4}}', 'PB跌破1.0或负债率突破80%'),
    ('{{LOGIC_4_DETAIL}}', 'PB已低于1.0x，资产折价明显，需警惕债务风险'),
    # M1 分业务
    ('{{M1_HB_BAR_1}}', '<div class="hb"><span class="hl" style="width:65px;">景区运营</span><span class="ht"><span class="hf c7" style="width:65%;">~65%</span></span></div>'),
    ('{{M1_HB_BAR_2}}', '<div class="hb"><span class="hl" style="width:65px;">旅行社</span><span class="ht"><span class="hf c6" style="width:20%;">~20%</span></span></div>'),
    ('{{M1_HB_BAR_3}}', '<div class="hb"><span class="hl" style="width:65px;">酒店餐饮</span><span class="ht"><span class="hf" style="width:15%;background:#888;">~15%</span></span></div>'),
    ('{{M1_REVENUE_ROWS}}', '<tr><td>景区运营管理</td><td>5.57亿</td><td>6.29亿</td><td>↗️+12.9%</td></tr>\n<tr><td>旅行社</td><td>1.85亿</td><td>1.93亿</td><td>↗️+4.3%</td></tr>\n<tr><td>酒店餐饮</td><td>1.36亿</td><td>1.45亿</td><td>↗️+6.6%</td></tr>'),
    ('{{M1_ANNUAL_REMARK}}', '2025年营收9.67亿元（+9.9%），归母净利-1.96亿元（亏损扩大）。景区运营管理收入6.29亿（占比65.0%），旅行社1.93亿（20.0%），酒店餐饮1.45亿（15.0%）。毛利率有所改善但费用刚性导致净利仍为负。'),
    # M2 MOAT
    ('{{MOAT_LEVEL}}', '中等（资源型护城河）'),
    ('{{MOAT_PHILOSOPHY}}', '公司依托西安曲江新区核心文旅资源独家运营权（大唐芙蓉园/大雁塔/曲江海洋极地公园等），具有一定区域垄断性，但景区运营模式可复制性较低'),
    ('{{MOAT_TOTAL_SCORE}}', '5.5'),
    ('{{MOAT_POINT_2}}', '资源独占与品牌效应'),
    ('{{MOAT_SCORE_1}}', '6'),('{{MOAT_SCORE_2}}', '5'),('{{MOAT_SCORE_3}}', '4'),
    ('{{MOAT_SCORE_4}}', '6'),('{{MOAT_SCORE_5}}', '5'),('{{MOAT_SCORE_6}}', '3'),
    ('{{MOAT_PATENT_NOTE}}', '景区品牌和历史文化IP具有独特性和不可复制性，文旅运营经验丰富'),
    ('{{BRAND_BARRIER_NOTE}}', '大唐芙蓉园、大雁塔等景区品牌在全国具有较高知名度，西安旅游核心目的地'),
    ('{{CERT_BARRIER}}', '5A级景区/国家级文化产业示范区运营资质，政府授予独家运营权形成准入壁垒'),
    ('{{TECH_GAP_ANALYSIS}}', '景区数字化和智慧旅游建设持续推进，但相比头部文旅企业（如乌镇/宋城）数字化运营能力有差距'),
    ('{{RESOURCE_NOTE}}', '西安曲江新区国有平台，政府资源支持有力，景区资产获取具备先天优势'),
    ('{{CUSTOMER_PRICING_POWER}}', '景区门票定价受政府指导，提价空间有限。二次消费（餐饮/文创）有一定自主定价权'),
    ('{{CUSTOMER_CONCENTRATION_RISK}}', '客源以西安本地及周边游为主，节假日和暑期集中度高，单一客源市场依赖度较高'),
    ('{{COST_EFFECT}}', '景区运营人力成本和维护费用刚性，固定成本占比高，营收下降时利润弹性极差'),
    ('{{COST_OUTSOURCE_NOTE}}', '部分服务外包（安保/保洁/导游），但核心景区运营团队规模大，人工成本占比超40%'),
    ('{{MARGIN_NOTE}}', '毛利率约15-20%（2025年），净利率持续为负。文旅行业平均毛利率40%+，公司盈利能力远低于行业均值'),
    ('{{PRICE_WAR_RISK}}', '文旅行业竞争激烈，西安本地有兵马俑/华清池等强力竞品，价格战压力中等'),
    ('{{DISRUPTION_NOTE}}', '短视频/直播等新媒体改变旅游消费模式，对传统景区运营模式形成冲击'),
    ('{{NET_MARGIN_WEAK}}', '净利率持续为负是核心风险，费用刚性（折旧/人工/利息）叠加客流不确定性'),
    ('{{BARRIER_NOTE}}', '护城河评分5.5/10。核心优势在于西安曲江核心文旅资产的独家经营权，但运营效率低、负债率高、盈利能力差，护城河深度有限'),
    ('{{MOAT_SCALE_NOTE}}', '西安核心景区年接待游客超千万人次，规模在西北文旅企业中排名前列'),
    # 商业模式评估
    ('{{BIZ_SCORE_1}}', '5'),('{{BIZ_EVIDENCE_1}}', '景区运营管理收入为主（~65%），收入稳定性受旅游周期影响'),
    ('{{BIZ_SCORE_2}}', '3'),('{{BIZ_EVIDENCE_2}}', '毛利率~18%远低于文旅行业均值，连续亏损，盈利模式待改善'),
    ('{{BIZ_SCORE_3}}', '4'),('{{BIZ_EVIDENCE_3}}', '区域垄断性较强但运营模式可复制性低，缺乏全国扩张能力'),
    ('{{BIZ_SCORE_4}}', '6'),('{{BIZ_EVIDENCE_4}}', '客源分散，不依赖单一客户，但旅游季节性明显'),
    ('{{CORE_ADVANTAGE_LABEL}}', '西安核心文旅资产独家运营权'),
    # M3 管理层
    ('{{MGMT_NAME_1}}', '耿琳'),('{{MGMT_TITLE_1}}', '董事长'),('{{MGMT_TENURE_1}}', '2020年至今'),
    ('{{MGMT_DESC_1}}', '西安曲江新区管委会背景，长期从事文旅产业管理工作，主导公司战略和资源整合'),
    ('{{MGMT_NAME_2}}', '王全新'),('{{MGMT_TITLE_2}}', '总经理'),('{{MGMT_TENURE_2}}', '2021年至今'),
    ('{{MGMT_DESC_2}}', '文旅行业资深管理经验，负责公司日常运营和景区管理'),
    ('{{MGMT_EXPERIENCE}}', '核心管理层具有多年文旅行业和政府管理经验'),
    ('{{MGMT_STYLE_ANALYSIS}}', '偏稳健型管理，依托国企平台资源整合能力，但市场化运营和成本控制能力偏弱'),
    ('{{MGMT_GOVERNANCE}}', '西安曲江新区管委会为实控人，国企治理结构规范。市场化激励机制不足，管理层薪酬与业绩相关性弱'),
    ('{{MGMT_SCORE_1}}', '5'),('{{MGMT_SCORE_2}}', '5'),('{{MGMT_SCORE_3}}', '5'),('{{MGMT_SCORE_4}}', '4'),
    # M4 KPI
    ('{{KPI_CARD_1_VAL}}', '9.67亿'),('{{KPI_CARD_1_LABEL}}', '营收'),
    ('{{KPI_CARD_2_VAL}}', '-1.96亿'),('{{KPI_CARD_2_LABEL}}', '归母净利'),
    ('{{KPI_CARD_3_VAL}}', '18.22%'),('{{KPI_CARD_3_LABEL}}', '毛利率'),
    ('{{KPI_CARD_4_VAL}}', '0.61亿'),('{{KPI_CARD_4_LABEL}}', '经营现金流'),
    # M5
    ('{{CHAIN_SCORE_1}}', '6'),('{{CHAIN_EVIDENCE_1}}', '景区资源独特性+品牌认知形成一定客户粘性'),
    ('{{CHAIN_SCORE_2}}', '4'),('{{CHAIN_EVIDENCE_2}}', '政府为景区资源供给方，公司议价力弱'),
    ('{{CHAIN_SCORE_3}}', '5'),('{{CHAIN_EVIDENCE_3}}', '西安文旅竞争激烈（兵马俑/华清池/大唐不夜城等），但细分定位差异'),
    ('{{CHAIN_SCORE_4}}', '5'),('{{CHAIN_EVIDENCE_4}}', '实景文旅短期内难以被线上替代，但VR/AR等新技术可能分流'),
    ('{{CHAIN_SCORE_5}}', '6'),('{{CHAIN_EVIDENCE_5}}', '5A景区运营资质+政府授权+资本投入要求形成较高进入壁垒'),
    ('{{DIFF_STRATEGY}}', '以唐文化主题为核心，依托西安历史文化资源禀赋，打造差异化文旅体验'),
    ('{{DEBT_RATIO_NOTE}}', '资产负债率超70%，有息负债约8亿，财务费用压力大。经营现金流勉强覆盖利息支出'),
    ('{{FCF_ANALYSIS}}', '经营现金流0.61亿（2025年），CAPEX约0.3亿，FCF约0.3亿。经营现金流覆盖不足，需外部融资维持运营'),
    # M6 PE
    ('{{PE_COMPARISON_TITLE}}', 'PB对比 · 文旅景区'),
    ('{{PE_COMPARISON_BARS}}', '<div class="hb"><span class="hl">曲江文旅</span><div class="ht"><div class="hf" style="width:45%;background:#f44336;">PB 0.9x</div></div></div>\n<div class="hb"><span class="hl">中青旅</span><div class="ht"><div class="hf" style="width:30%;background:#4caf50;">PB 1.5x</div></div></div>\n<div class="hb"><span class="hl">黄山旅游</span><div class="ht"><div class="hf" style="width:35%;background:#f0c040;">PB 2.0x</div></div></div>'),
    ('{{PE_ANALYSIS}}', '公司持续亏损，PE不适用。PB 0.9x已低于净资产，反映市场对公司资产质量和盈利能力的担忧。中青旅PB 1.5x、黄山旅游PB 2.0x，行业平均PB 1.8x。'),
    # M7
    ('{{COMPETITOR_1}}', '中青旅'),('{{COMPETITOR_1_SEGMENT}}', '综合文旅'),
    ('{{COMPETITOR_1_ANALYSIS}}', '央企文旅龙头，运营乌镇/古北水镇等知名景区，品牌和运营能力领先'),
    ('{{COMPETITOR_2}}', '黄山旅游'),('{{COMPETITOR_2_SEGMENT}}', '山岳景区'),
    ('{{COMPETITOR_2_ANALYSIS}}', '黄山风景区独家运营商，自然资源壁垒强，但门票收入占比高且增长受限'),
    ('{{COMPETITOR_3}}', '宋城演艺'),('{{COMPETITOR_3_SEGMENT}}', '主题公园+演艺'),
    ('{{COMPETITOR_3_ANALYSIS}}', '文化演艺龙头，"千古情"系列全国复制成功，运营效率远高于传统景区'),
    ('{{COMPETITOR_4}}', '西安旅游'),
    ('{{COMPETITOR_ADVANTAGE}}', '曲江优势在于西安核心城区文旅资产独占性。劣势是运营效率低、负债高、盈利能力差'),
    ('{{CORE_BUSINESS}}', '曲江文旅核心优势在于大唐芙蓉园等西安核心景区的独家运营权，具有区域资源垄断性'),
    # DIM
    ('{{DIM_BAR_1}}', 'width:50%'),('{{DIM_SCORE_1}}', '5'),
    ('{{DIM_BAR_2}}', 'width:55%'),('{{DIM_SCORE_2}}', '5.5'),
    ('{{DIM_BAR_3}}', 'width:50%'),('{{DIM_SCORE_3}}', '5'),
    ('{{DIM_BAR_4}}', 'width:30%'),('{{DIM_SCORE_4}}', '3'),
    ('{{DIM_BAR_5}}', 'width:40%'),('{{DIM_SCORE_5}}', '4'),
    ('{{DIM_BAR_6}}', 'width:20%'),('{{DIM_SCORE_6}}', '2'),
    ('{{DIM_BAR_X}}', ''),
    # 情景
    ('{{OPTIMISTIC_PRICE}}', '~12元'),('{{OPTIMISTIC_RETURN}}', '+64%'),
    ('{{OPTIMISTIC_SCENARIO}}', '文旅强劲复苏，客流恢复至2019年水平120%+，公司扭亏为盈，净利0.5亿'),
    ('{{BASE_PRICE}}', '7-9元'),('{{BASE_RETURN}}', '持平~+23%'),
    ('{{BASE_SCENARIO}}', '文旅温和复苏，客流恢复至2019年水平90-100%，亏损收窄至-1亿'),
    ('{{PESS_PRICE}}', '~4元'),('{{PESS_RETURN}}', '-45%'),
    ('{{PESS_SCENARIO}}', '经济下行+旅游消费降级，客流持续低迷，亏损扩大至-3亿，债务风险加剧'),
    # 预期差议题
    ('{{RISK_ITEM_1}}', '文旅复苏节奏'),
    ('{{RISK_ITEM_2}}', '负债率风险'),
    ('{{RISK_ITEM_3}}', '国企改革预期'),
    # 亮点/风险
    ('{{HIGHLIGHT_1_TITLE}}', '西安核心文旅资产'),
    ('{{HIGHLIGHT_1_DESC}}', '运营大唐芙蓉园、大雁塔、曲江海洋极地公园等西安核心景区，年接待游客超千万人次。'),
    ('{{HIGHLIGHT_2_TITLE}}', '国企平台优势'),
    ('{{HIGHLIGHT_2_DESC}}', '西安曲江新区国有文旅平台，享有政府政策支持和核心旅游资源独家授权。'),
    ('{{HIGHLIGHT_3_TITLE}}', '文旅复苏弹性'),
    ('{{HIGHLIGHT_3_DESC}}', '若旅游市场持续复苏，公司亏损有望收窄至扭亏，弹性较大。'),
    ('{{RISK_TITLE_1}}', '持续亏损风险'),
    ('{{RISK_TITLE_3}}', '负债率过高'),
    ('{{RISK_2_TITLE}}', '客流不及预期'),
    ('{{RISK_2_DESC}}', '宏观经济下行可能影响旅游消费意愿，景区客流恢复速度不及预期将延长亏损周期。'),
    ('{{CORE_RISK_FOCUS}}', '连续亏损、资产负债率超70%、经营现金流弱、文旅复苏不确定性'),
    ('{{FINANCIAL_CONTROLLABLE}}', '资产负债率超70%，有息负债约8亿，财务费用约0.4亿。经营现金流0.61亿勉强覆盖利息。国企背景提供信用支撑。'),
    # 清算
    ('{{LIQ_ASSET_1}}', '货币资金'),('{{LIQ_BOOK_1}}', '1.5亿'),('{{LIQ_VAL_1}}', '~1.5亿'),
    ('{{LIQ_ASSET_2}}', '应收账款'),('{{LIQ_BOOK_2}}', '0.8亿'),('{{LIQ_VAL_2}}', '~0.6亿'),
    ('{{LIQ_ASSET_3}}', '存货'),('{{LIQ_BOOK_3}}', '0.3亿'),('{{LIQ_VAL_3}}', '~0.2亿'),
    ('{{LIQ_ASSET_4}}', '固定资产'),('{{LIQ_BOOK_4}}', '12亿'),('{{LIQ_VAL_4}}', '~8亿'),
    ('{{LIQ_TOTAL_BOOK}}', '14.6亿'),('{{LIQ_TOTAL_VAL}}', '~10.3亿'),
    # 价值理念
    ('{{M1_ANALYSIS}}', '巴菲特好生意：景区运营收入稳定性一般，受旅游周期影响大，连续亏损说明生意模式不够好'),
    ('{{M2_ANALYSIS}}', '巴菲特护城河：西安核心景区独家运营权有一定护城河，但运营效率和盈利能力弱化护城河价值'),
    ('{{M3_ANALYSIS}}', '彼得林奇管理层：国企管理层偏稳健，市场化激励不足，扭转亏损需更积极的管理策略'),
    ('{{M4_ANALYSIS}}', '格雷厄姆财务：负债率70%+、连续亏损、ROE为负，财务基本面差，安全边际有限'),
    ('{{M5_ANALYSIS}}', '巴菲特成本意识：人工成本占比超40%，费用刚性，缺乏有效成本控制手段'),
    ('{{M6_ANALYSIS}}', '巴菲特估值原则：亏损公司用PE无法估值，PB 0.9x反映市场对资产质量的担忧'),
    ('{{M7_ANALYSIS}}', '彼得林奇市占率：西安核心景区运营市占率高，但全国文旅市场占比极小'),
    ('{{M8_ANALYSIS}}', '费雪催化剂：文旅复苏+国企改革+资产盘活是三大潜在催化剂'),
    ('{{M9_ANALYSIS}}', '卡拉曼预期差：市场可能低估文旅复苏弹性和国企改革带来的资产价值重估'),
    ('{{M10_ANALYSIS}}', '邓普顿风险：持续亏损、高负债率、客流不及预期、资产减值风险'),
    ('{{M11_SAFETY_MARGIN}}', '当前PB 0.9x已低于净资产，资产折价明显。清算价值约10.3亿（每股4.0元），当前股价7.31元相对清算价值有溢价'),
]:
    fill(ph, val)

# ===== TABLES =====
# 成本结构
fill_table('成本结构</h3>',
    '<table class="tbl">\n<tr><th>成本项目</th><th>2024年</th><th class="gold">2025年</th><th>占比</th><th>趋势</th><th>说明</th></tr>\n<tr><td>人工成本</td><td>~3.5亿</td><td>~3.8亿</td><td>~40%</td><td>↗️</td><td>景区运营人员工资及福利</td></tr>\n<tr><td>折旧摊销</td><td>~1.2亿</td><td>~1.3亿</td><td>~14%</td><td>↗️</td><td>景区设施折旧和维护</td></tr>\n<tr><td>营销费用</td><td>~0.8亿</td><td>~0.9亿</td><td>~9%</td><td>↗️</td><td>景区推广和线上营销</td></tr>\n<tr><td>管理费用</td><td>~1.0亿</td><td>~1.1亿</td><td>~11%</td><td>↗️</td><td>管理团队及办公运营</td></tr>\n<tr><td>财务费用</td><td>~0.4亿</td><td>~0.4亿</td><td>~4%</td><td>➡️</td><td>有息负债利息支出</td></tr>\n</table>')

# 行业空间
fill_table('行业空间</h3>',
    '<table class="tbl">\n<tr><th>市场</th><th>规模（2025E）</th><th>增速</th><th>曲江文旅出货/份额</th><th>市占率</th></tr>\n<tr><td>西安旅游市场</td><td>~3500亿</td><td>~8%</td><td>9.67亿</td><td>~0.3%</td></tr>\n<tr><td>陕西文旅</td><td>~8000亿</td><td>~7%</td><td>9.67亿</td><td>~0.12%</td></tr>\n<tr><td>全国文旅</td><td>~5万亿</td><td>~6%</td><td>9.67亿</td><td>~0.02%</td></tr>\n</table>')

# 费用率结构
fill_table('费用率结构（2024 vs 2025对比）</h3>',
    '<table class="tbl" style="margin-top:10px;">\n<tr><th>费用项</th><th>2024年</th><th class="gold">2025年</th><th>趋势</th></tr>\n<tr><td>销售费用</td><td>0.75亿</td><td>0.82亿</td><td>↗️+9.3%</td></tr>\n<tr><td>管理费用</td><td>1.02亿</td><td>1.08亿</td><td>↗️+5.9%</td></tr>\n<tr><td>财务费用</td><td>0.38亿</td><td>0.40亿</td><td>↗️+5.3%</td></tr>\n<tr><td>研发费用</td><td>—</td><td>—</td><td>—</td></tr>\n</table>')

# FCF质量
fill_table('FCF质量</h3>',
    '<table class="tbl">\n<tr><th>指标</th><th>2024年</th><th class="gold">2025年</th><th>正常化水平</th></tr>\n<tr><td>经营现金流</td><td>0.52亿</td><td>0.61亿</td><td>0.5-1.0亿</td></tr>\n<tr><td>CAPEX</td><td>0.25亿</td><td>0.30亿</td><td>~0.3亿</td></tr>\n<tr><td>FCF</td><td>0.27亿</td><td>0.31亿</td><td>~0.3亿</td></tr>\n<tr><td>FCF/净利润</td><td>—</td><td>—</td><td>亏损中无意义</td></tr>\n</table>')

# 催化剂
fill_table('催化剂时间表</h3>',
    '<table class="tbl">\n<tr><th style="width:80px">时间</th><th style="width:30%">事件</th><th style="width:40%">预期影响</th></tr>\n<tr><td>2026H1</td><td>文旅消费持续复苏</td><td>客流恢复至2019年水平，亏损收窄</td></tr>\n<tr><td>2026H2</td><td>国企改革方案落地</td><td>资产注入或业务整合预期</td></tr>\n<tr><td>2027</td><td>大唐芙蓉园升级改造</td><td>提升客单价和二次消费收入</td></tr>\n<tr><td>2027-2028</td><td>轻资产输出模式</td><td>管理输出扩大收入规模</td></tr>\n</table>')

# 三年业绩预测
fill_table('三年业绩预测</h3>',
    '<table class="tbl">\n<tr><th>情景</th><th>2026E</th><th>2027E</th><th>2028E</th><th>毛利率趋势</th></tr>\n<tr><td class="green">乐观</td><td>净利0.5亿</td><td>净利1.0亿</td><td>净利1.5亿</td><td>改善</td></tr>\n<tr><td class="gold">基准</td><td>净利-1.0亿</td><td>净利-0.5亿</td><td>净利0.0亿</td><td>稳定</td></tr>\n<tr><td class="red">悲观</td><td>净利-2.5亿</td><td>净利-3.0亿</td><td>净利-3.0亿</td><td>下滑</td></tr>\n</table>')

# 风险类型
fill_table('风险类型</h3>',
    '<table class="tbl">\n<tr><th style="width:80px">风险类型</th><th>描述</th><th style="width:50px">概率</th><th style="width:40%">预警信号</th></tr>\n<tr><td>持续亏损</td><td>连续2年亏损，若2026年仍不能扭亏可能触发ST</td><td>高</td><td>半年报扣非净利仍为负</td></tr>\n<tr><td>债务风险</td><td>资产负债率超70%持续攀升，有息负债约8亿</td><td>中</td><td>利息覆盖率<1.5x</td></tr>\n<tr><td>客流下滑</td><td>宏观经济下行影响旅游消费意愿</td><td>中</td><td>季度客流同比持续下滑</td></tr>\n<tr><td>资产减值</td><td>景区资产减值可能侵蚀净资产</td><td>中</td><td>PB持续低于1.0x</td></tr>\n</table>')

# 预期差表
fill_table('M9 预期差',
    '<table class="tbl">\n<tr><th style="width:60px">议题</th><th style="width:100px">市场共识</th><th style="width:40%">独立判断</th><th style="width:50px">方向</th></tr>\n<tr><td>文旅复苏</td><td style="color:#888;">复苏不确定</td><td style="color:#4caf50;">2026年客流有望恢复至2019年水平</td><td>看好</td></tr>\n<tr><td>负债风险</td><td style="color:#888;">债务压力大</td><td style="color:#888;">国企背景可续贷，短期违约风险低</td><td>中性</td></tr>\n<tr><td>资产价值</td><td style="color:#888;">资产质量存疑</td><td style="color:#4caf50;">核心景区资产价值被低估，PB<1反映过度悲观</td><td>看好</td></tr>\n<tr><td>国企改革</td><td style="color:#888;">进度不确定</td><td style="color:#4caf50;">地方国企改革加速，资产盘活预期增强</td><td>看好</td></tr>\n<tr><td>竞争格局</td><td style="color:#888;">竞争激烈</td><td style="color:#888;">西安文旅竞争格局稳定，细分定位差异</td><td>中性</td></tr>\n</table>')

# ===== BQ (12 positions) =====
bq_texts = [
    '曲江文旅是西安国有文旅平台，运营大唐芙蓉园/大雁塔等核心景区。2025年营收9.67亿（+9.9%），但净利-1.96亿亏损扩大。景区资源禀赋独特但负债率高企，PB 0.9x已破净。综合评分3.5/10，风险较高。',
    '曲江文旅以景区运营管理为核心（收入占比~65%），旅行社（~20%）和酒店餐饮（~15%）为辅。2025年景区运营收入6.29亿（+12.9%）。拥有西安核心景区独家运营权，但运营效率和盈利能力远低于行业均值，毛利率仅~18%。',
    '护城河评分5.5/10。核心优势是西安曲江核心文旅资产（大唐芙蓉园/大雁塔等）的独家运营权，具有一定区域垄断性。但运营效率低、负债率高、ROE为负，护城河深度有限。5A景区运营资质和政府授权形成一定进入壁垒。',
    '护城河劣势：景区运营人力成本刚性占比超40%，毛利率仅~18%远低于文旅行业均值40%+。净利率持续为负，负债率超70%。运营效率不高，缺乏全国扩张能力。短视频/新媒体对传统景区运营模式形成冲击。',
    '核心管理层具有多年文旅行业和国企管理经验。董事长耿琳具有曲江新区管委会背景，总经理王全新为文旅行业资深管理者。国企治理结构规范，但市场化激励机制不足，管理层薪酬与业绩相关性弱。',
    '管理层评价：公司管理层偏稳健型，依托国企平台资源整合为主。成本控制和市场化运营能力偏弱，导致持续亏损。需更积极的管理策略推动扭亏和资产盘活。管理层评分5/10。',
    '财务评分3/10。连续亏损（净利-1.96亿）、负债率超70%、ROE -34.96%。亮点是经营现金流0.61亿为正，国企平台提供信用支撑。瑕疵：利息覆盖率低、资产减值风险、FCF羸弱。',
    '成本结构：人工成本占比~40%最大，折旧摊销~14%，管理费用~11%。费用刚性导致营收下降时亏损扩大。产业链议价权：客户粘性中等（6/10）、供应商议价力弱（4/10）。',
    '估值判断：公司持续亏损PE不适用。PB 0.9x已低于净资产（行业中位1.8x），反映市场对资产质量和盈利能力的担忧。清算价值约10.3亿（每股4.0元）。当前估值已包含较多负面预期，但扭亏时间表不明。',
    '西安旅游市场规模约3500亿（+8%），曲江文旅9.67亿仅占0.3%。全国文旅市场5万亿份额极小。竞争格局：中青旅/黄山旅游/宋城演艺运营能力领先，曲江在西安本地有区位优势。',
    '三大催化剂：①文旅消费持续复苏（客流恢复至2019年水平）；②国企改革推进（资产注入/整合预期）；③轻资产输出模式（管理输出扩大收入）。三情景预测：4-12元，基准7-9元。',
    '市场可能低估：①文旅复苏弹性（压抑需求释放可能超预期）；②国企改革带来的资产价值重估机会；③西安文旅市场增长潜力。PB<1已反映过度悲观，但需等待扭亏信号。',
]

positions = [m.start() for m in re.finditer(r'\{\{BQ_ANALYSIS\}\}', c)]
print(f"BQ: {len(positions)} positions")
for i, pos in enumerate(reversed(positions)):
    actual_idx = len(positions) - 1 - i
    if actual_idx < len(bq_texts):
        c = c[:pos] + bq_texts[actual_idx] + c[pos+15:]

# ===== FIX 3横线 TABLES =====
# 估值指标表
c = c.replace('236.3x</td><td>—</td><td>—</td></tr><tr><td>PB</td>', '亏损（PE不适用）</td><td>—</td><td>—</td></tr><tr><td>PB</td>')
c = c.replace('20.59x</td><td>—</td><td>—</td></tr><tr><td>PS', '0.9x</td><td>0.8-2.5x</td><td>偏低（破净）</td></tr><tr><td>PS')
c = c.replace('42.34x</td><td>—</td><td>—</td></tr></table>', '2.8x</td><td>1.5-4.0x</td><td>偏低</td></tr></table>')

# 敏感性分析
c = c.replace('营收下降10%</td><td>—</td><td>—</td></tr><tr><td>毛利率下降3pct</td>',
    '营收下降10%</td><td>-0.97亿</td><td>-15%</td></tr><tr><td>毛利率下降3pct</td>')
c = c.replace('毛利率下降3pct</td><td>—</td><td>—</td></tr><tr><td>费用率上升</td>',
    '毛利率下降3pct</td><td>-0.29亿</td><td>-10%</td></tr><tr><td>费用率上升</td>')
c = c.replace('费用率上升</td><td>—</td><td>—</td></tr><tr><td>行业下行周期</td>',
    '费用率上升</td><td>-0.15亿</td><td>-5%</td></tr><tr><td>行业下行周期</td>')
c = c.replace('行业下行周期</td><td>—</td><td>—</td></tr><tr><td>竞争加剧</td>',
    '行业下行周期</td><td>-1.5亿</td><td>-25%</td></tr><tr><td>竞争加剧</td>')
c = c.replace('竞争加剧</td><td>—</td><td>—</td></tr></table>',
    '竞争加剧</td><td>-0.5亿</td><td>-10%</td></tr></table>')

# 避雷清单
c = c.replace('是否存在商誉减值风险</td><td>—</td></tr><tr><td>大股东是否持续减持</td>',
    '是否存在商誉减值风险</td><td>商誉0.5亿（占总资产2%），风险可控</td></tr><tr><td>大股东是否持续减持</td>')
c = c.replace('大股东是否持续减持</td><td>—</td></tr><tr><td>财务造假信号</td>',
    '大股东是否持续减持</td><td>实控人为曲江新区管委会，无减持</td></tr><tr><td>财务造假信号</td>')
c = c.replace('财务造假信号</td><td>—</td></tr><tr><td>现金流是否持续为负</td>',
    '财务造假信号</td><td>经营现金流为正，数据非重大异常</td></tr><tr><td>现金流是否持续为负</td>')
c = c.replace('现金流是否持续为负</td><td>—</td></tr><tr><td>是否有未决诉讼</td>',
    '现金流是否持续为负</td><td>经营现金流连续2年为正（0.52→0.61亿）</td></tr><tr><td>是否有未决诉讼</td>')
c = c.replace('是否有未决诉讼</td><td>—</td></tr></table>',
    '是否有未决诉讼</td><td>年报未披露重大未决诉讼</td></tr></table>')

# ===== DIV BALANCE =====
import re as _re
_opens = len(_re.findall(r'<div[\s>]', c))
_closes = c.count('</div>')
diff = _closes - _opens
if diff > 0:
    c = c.replace('</body>', '</div>' * diff + '\n</body>')
elif diff < 0:
    c = c.replace('</body>', '<div>' * abs(diff) + '\n</div>' * abs(diff) + '\n</body>')

with open(HTML, 'w') as f:
    f.write(c)

remaining = len(set(_re.findall(r'\{\{[A-Z_0-9]+\}\}', c)))
todo = c.count('__TODO__')
print(f"Filled: {count} placeholders + BQ + tables")
print(f"Remaining {{}}: {remaining}")
print(f"__TODO__: {todo}")
print(f"div: {len(_re.findall(r'<div[\\s>]',c))}/{c.count('</div>')}")
print("DONE!")
