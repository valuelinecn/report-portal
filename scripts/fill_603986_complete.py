#!/usr/bin/env python3
"""
fill_603986_complete.py — 兆易创新(603986) 综合填充脚本
基于旧报告数据提取后应用
"""
import re, os

PORTAL = os.path.expanduser('~/.hermes/hermes-agent/report-portal')
path = os.path.join(PORTAL, 'reports', '603986.html')

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old = __import__('subprocess').run(
    f'cd {PORTAL} && git show test:reports/603986.html',
    capture_output=True, text=True, shell=True
).stdout

fixes = 0

def fix(old_text, new_text):
    global c, fixes
    if old_text in c:
        c = c.replace(old_text, new_text)
        fixes += 1
        return True
    return False

# ===== 基础信息 =====
fix('{{COMPANY_NAME_CN}}', '兆易创新')
fix('{{COMPANY_SHORT}}', '兆易创新')
fix('{{COMPANY_NAME_EN}}', 'GigaDevice')
fix('{{INDUSTRY}}', '半导体')
fix('{{REPORT_DATE}}', '2026-06-17')
fix('{{DATA_DATE}}', '2026-06-17')
fix('{{DATA_SOURCE}}', 'fin-table API + 年报')
fix('{{SCORE}}', '6.5')
fix('{{RATING_DESC}}', '国内存储+MCU双龙头，技术平台扎实，但高估值与周期底部待确认构成主要风险')
fix('{{RATING_TEXT}}', '2026-06-17')
fix('{{COMPANY_DESC_LONG}}', '兆易创新作为国内存储芯片与MCU双轮驱动的IC设计龙头，NOR Flash全球第三、MCU国内领先，具备较强的技术平台和产品线广度。但半导体行业强周期属性、当前PE估值超200x、产品价格底部尚未确认回升是多方面制约因素。综合评分为6.5/10，属中等偏上。')
fix('{{INVESTMENT_THESIS}}', '兆易创新是国内半导体设计领域稀缺的平台型公司，NOR Flash+MCU双轮驱动稳健，DRAM第三曲线打开想象空间。但当前估值已隐含了较高的增长预期，且半导体强周期属性使盈利可预测性差。建议等待PE回到合理区间后再行配置。')

# ===== 综合评价卡片 =====
fix('{{CARD1_VAL}}', '6.5')
fix('{{CARD1_LABEL}}', '综合评级')
fix('{{CARD1_COLOR}}', '#4caf50')
fix('{{CARD2_VAL}}', '中')
fix('{{CARD2_LABEL}}', '风险等级')
fix('{{CARD2_COLOR}}', '#ffc107')
fix('{{CARD3_VAL}}', '高')
fix('{{CARD3_LABEL}}', '成长弹性')
fix('{{CARD3_COLOR}}', '#4caf50')
fix('{{CARD4_VAL}}', '9.3%')
fix('{{CARD4_LABEL}}', 'ROE')
fix('{{CARD4_COLOR}}', '#888')
fix('{{LABEL_2}}', '双平台龙头')
fix('{{LABEL_2_TITLE}}', '核心优势')
fix('{{LABEL_3}}', 'DRAM突破、AI端侧NOR升级、车规MCU放量')
fix('{{LABEL_3_TITLE}}', '催化剂')

# ===== LOGIC卡 =====
fix('{{LOGIC_1_VAL}}', '6.5')
fix('{{LOGIC_1}}', '双平台（NOR+MCU）提供稳健基本盘，DRAM打开想象空间')
fix('{{LOGIC_2}}', '7.2/10')
fix('{{LOGIC_2_DETAIL}}', 'NOR Flash全球第三（~18%）、GD32 MCU国内领先，技术+认证壁垒稳固')
fix('{{LOGIC_3}}', '高弹性')
fix('{{LOGIC_3_DETAIL}}', 'DRAM从0到1突破+AI端侧NOR升级+车规MCU放量，三引擎驱动')
fix('{{LOGIC_4}}', '估值偏高')
fix('{{LOGIC_4_DETAIL}}', 'PE>200x已隐含极高预期，需持续超预期消化')

# ===== M1 分业务收入 + 年度 =====
# 分业务水平条（双年格式）
hb1 = '<div class="hb"><span class="hl" style="width:65px;">存储芯片</span><span class="ht"><span class="hf c7" style="width:71%;">71.3%</span></span></div>'
hb2 = '<div class="hb"><span class="hl" style="width:65px;">MCU</span><span class="ht"><span class="hf c6" style="width:21%;">20.8%</span></span></div>'
hb3 = '<div class="hb"><span class="hl" style="width:65px;">传感器+模拟</span><span class="ht"><span class="hf" style="width:8%;background:#888;">7.9%</span></span></div>'

fix('{{M1_HB_BAR_1}}', hb1)
fix('{{M1_HB_BAR_2}}', hb2)
fix('{{M1_HB_BAR_3}}', hb3)

# M1 revenue rows (双年格式)
rev_rows = '''<tr><td>存储芯片</td><td>51.93亿</td><td>65.66亿</td><td>↗️+26.4%</td></tr>
<tr><td>MCU</td><td>15.03亿</td><td>19.10亿</td><td>↗️+27.1%</td></tr>
<tr><td>传感器+模拟</td><td>6.43亿</td><td>7.27亿</td><td>↗️+13.1%</td></tr>'''
fix('{{M1_REVENUE_ROWS}}', rev_rows)

# M1年度备注
fix('{{M1_ANNUAL_REMARK}}', '2025年营收92.03亿元（+25%），归母净利16.48亿元（+49.8%）。存储芯片业务受益于NOR Flash量价齐升，MCU业务在汽车电子和IoT领域持续渗透。传感器业务恢复增长。综合毛利率42.84%，净利率17.92%，ROE 9.3%。')

# ===== M2 壁垒 =====
# 从旧报告提取MOAT数据
fix('{{MOAT_LEVEL}}', '中等（局部护城河）')
fix('{{MOAT_PHILOSOPHY}}', '公司通过技术积累（NOR Flash全球第三、GD32 MCU国内领先）和车规认证（AEC-Q100）构建了一定护城河，但芯片设计行业技术迭代快，护城河深度有限')
fix('{{MOAT_TOTAL_SCORE}}', '7.2')
fix('{{MOAT_POINT_2}}', '技术壁垒与客户粘性')
fix('{{MOAT_SCORE_1}}', '7')
fix('{{MOAT_SCORE_2}}', '7')
fix('{{MOAT_SCORE_3}}', '7')
fix('{{MOAT_SCORE_4}}', '7')
fix('{{MOAT_SCORE_5}}', '8')
fix('{{MOAT_SCORE_6}}', '7')
fix('{{MOAT_PATENT_NOTE}}', '累计专利超千项，涵盖存储器电路设计、MCU架构、接口技术等核心领域，是技术壁垒的重要支撑')
fix('{{BRAND_BARRIER_NOTE}}', 'GD32品牌在中国MCU市场具有较高知名度，Arm通用MCU领域出货量国内第一，形成了品牌粘性和用户习惯')
fix('{{CERT_BARRIER}}', 'AEC-Q100车规认证已完成，车规MCU进入量产出货阶段，车规认证周期长、门槛高，是重要的准入壁垒')
fix('{{TECH_GAP_ANALYSIS}}', '55nm主力制程与全球领先水平（28nm以下）存在代差，但在NOR Flash领域制程差距对成本影响有限')
fix('{{RESOURCE_NOTE}}', 'Fabless轻资产模式，晶圆代工依赖中芯国际、华虹等，无自有产能限制，但代工产能保障是供应链优势')
fix('{{CUSTOMER_PRICING_POWER}}', '下游客户分散（消费电子/工业/汽车/IoT），单一客户依赖度低，但与终端品牌客户议价能力一般')
fix('{{CUSTOMER_CONCENTRATION_RISK}}', '前五大客户占比约25%，集中度适中，但受中美科技竞争影响，华为等大客户占比有提升趋势')
fix('{{COST_EFFECT}}', 'Fabless模式下固定成本低，但随着产品线扩展和制程升级，研发投入持续增长（2025年研发费用11.17亿）')
fix('{{COST_OUTSOURCE_NOTE}}', '代工成本占比约65%，晶圆代工价格波动直接影响毛利率。2025年毛利率42.84%处于周期中位')
fix('{{MARGIN_NOTE}}', '存储芯片毛利率约45%，MCU毛利率约35%，传感器毛利率约30%。净利率从周期高点25%降至低点4%，波动剧烈')
fix('{{PRICE_WAR_RISK}}', 'NOR Flash行业价格战持续，尚未完全出清。华邦/旺宏/兆易三家竞争格局稳定但价格仍承压')
fix('{{DISRUPTION_NOTE}}', '新兴存储技术（MRAM/FRAM/RRAM）可能在5-10年对NOR Flash形成替代威胁，但目前成本差距大，风险可控')
fix('{{NET_MARGIN_WEAK}}', '净利率波动大是核心弱点，从21年25%降到23年4%，强周期属性影响盈利稳定性')
fix('{{BARRIER_NOTE}}', '护城河评分7.2/10。NOR Flash全球第三（~18%份额）、GD32 MCU国内领先形成双平台壁垒，但技术门槛相对有限（55nm主力制程），华邦/旺宏/普冉等竞争激烈')

# ===== M3 管理层 =====
fix('{{MGMT_NAME_1}}', '朱一明')
fix('{{MGMT_TITLE_1}}', '董事长（创始人）')
fix('{{MGMT_TENURE_1}}', '2005年至今')
fix('{{MGMT_DESC_1}}', '清华大学学士/硕士、美国石溪分校硕士。曾任IPolicy Networks资深工程师。2005年创立公司，主导战略布局。')
fix('{{MGMT_NAME_2}}', '何卫')
fix('{{MGMT_TITLE_2}}', '总经理/董事')
fix('{{MGMT_TENURE_2}}', '2018年至今')
fix('{{MGMT_DESC_2}}', '电子工程背景，多年半导体行业运营管理经验。负责公司日常运营和战略执行。')
fix('{{MGMT_EXPERIENCE}}', '核心管理层均具有15年以上半导体行业经验')
fix('{{MGMT_STYLE_ANALYSIS}}', '偏技术驱动型管理，注重产品研发和平台化布局，经营风格稳健')
fix('{{MGMT_GOVERNANCE}}', '董事会2024年完成换届，独立董事占比符合监管要求。2026年朱一明减持计划对短期市场情绪构成压力')
fix('{{MGMT_SCORE_1}}', '7')
fix('{{MGMT_SCORE_2}}', '7')
fix('{{MGMT_SCORE_3}}', '7')
fix('{{MGMT_SCORE_4}}', '7')

# ===== M4 KPI卡片 =====
fix('{{KPI_CARD_1_VAL}}', '92.03亿')
fix('{{KPI_CARD_1_LABEL}}', '营收')
fix('{{KPI_CARD_2_VAL}}', '16.48亿')
fix('{{KPI_CARD_2_LABEL}}', '归母净利')
fix('{{KPI_CARD_3_VAL}}', '42.84%')
fix('{{KPI_CARD_3_LABEL}}', '毛利率')
fix('{{KPI_CARD_4_VAL}}', '21.21亿')
fix('{{KPI_CARD_4_LABEL}}', '经营现金流')

# ===== M5 成本/费用 =====
# 费用率结构由引擎通过__TODO__替换，但模板有完整表格需要整表替换
fee_rows = '''<tr><td>研发费用</td><td>10.45亿</td><td class="gold">11.17亿</td><td>↘️+6.9%</td></tr>
<tr><td>销售费用</td><td>4.15亿</td><td class="gold">4.46亿</td><td>↗️+7.5%</td></tr>
<tr><td>管理费用</td><td>5.53亿</td><td class="gold">6.12亿</td><td>↗️+10.7%</td></tr>
<tr><td>财务费用</td><td>-4.43亿</td><td class="gold">-1.42亿</td><td>↗️利息支出减少</td></tr>'''
fix('费用率结构（2024 vs 2025对比）的表会被整表替换掉吗？', fee_rows)  # placeholder hint

# 成本结构表 (5行×6列)
cost_rows = '''<tr><td>代工成本（晶圆）</td><td>~30亿</td><td>~35亿</td><td>~55%</td><td>↗️</td><td>受晶圆厂产能和价格影响</td></tr>
<tr><td>研发费用</td><td>10.45亿</td><td>11.17亿</td><td>~12%</td><td>↗️</td><td>保持高研发投入，拓展DRAM产品线</td></tr>
<tr><td>销售费用</td><td>4.15亿</td><td>4.46亿</td><td>~5%</td><td>↗️</td><td>销售人员及市场推广增加</td></tr>
<tr><td>管理费用</td><td>5.53亿</td><td>6.12亿</td><td>~7%</td><td>↗️</td><td>管理人员增加及薪酬调整</td></tr>
<tr><td>封装测试</td><td>~9亿</td><td>~11亿</td><td>~12%</td><td>↗️</td><td>封测委外，随出货量增长</td></tr>'''

# 产业链议价权(5维度)
chain_rows = '''<tr><td>客户粘性</td><td>{{CHAIN_SCORE_1}}</td><td>{{CHAIN_EVIDENCE_1}}</td></tr>
<tr><td>供应商议价力</td><td>{{CHAIN_SCORE_2}}</td><td>{{CHAIN_EVIDENCE_2}}</td></tr>
<tr><td>竞争格局</td><td>{{CHAIN_SCORE_3}}</td><td>{{CHAIN_EVIDENCE_3}}</td></tr>
<tr><td>潜在替代</td><td>{{CHAIN_SCORE_4}}</td><td>{{CHAIN_EVIDENCE_4}}</td></tr>
<tr><td>进入壁垒</td><td>{{CHAIN_SCORE_5}}</td><td>{{CHAIN_EVIDENCE_5}}</td></tr>'''

fix('{{CHAIN_SCORE_1}}', '7')
fix('{{CHAIN_EVIDENCE_1}}', 'GD32 MCU生态粘性强，客户替换成本高')
fix('{{CHAIN_SCORE_2}}', '5')
fix('{{CHAIN_EVIDENCE_2}}', 'Fabless模式依赖代工厂，中芯国际等议价力强')
fix('{{CHAIN_SCORE_3}}', '6')
fix('{{CHAIN_EVIDENCE_3}}', 'NOR Flash三强格局稳定，但MCU竞争激烈')
fix('{{CHAIN_SCORE_4}}', '8')
fix('{{CHAIN_EVIDENCE_4}}', 'NOR Flash短期无有效替代技术，但长期MRAM等有威胁')
fix('{{CHAIN_SCORE_5}}', '7')
fix('{{CHAIN_EVIDENCE_5}}', 'IC设计需要技术和生态积累，但Fabless模式下进入门槛相对可控')
fix('{{DIFF_STRATEGY}}', '公司以NOR Flash为基、MCU为翼、DRAM为第三极，形成差异化产品矩阵。相比华邦专注于存储、ST专注于MCU，兆易创新在品类宽度上具有优势')

# ===== FCF分析 =====
fix('{{FCF_ANALYSIS}}', '经营现金流21.21亿（2025年）vs 20.35亿（2024年），覆盖净利润1.29倍。CAPEX约2-3亿（Fabless轻资产），FCF约18亿。FCF/营收比率约20%，FCF质量良好。')

# ===== M6 估值 =====
fix('{{PE_COMPARISON_TITLE}}', 'PE对比 · 半导体存储设计')
pe_bars = '''<div class="hb"><span class="hl">兆易创新</span><div class="ht"><div class="hf" style="width:95%;background:#f44336;">227x</div></div></div>
<div class="hb"><span class="hl">华邦电子</span><div class="ht"><div class="hf" style="width:30%;background:#4caf50;">30x</div></div></div>
<div class="hb"><span class="hl">旺宏电子</span><div class="ht"><div class="hf" style="width:55%;background:#f0c040;">45x</div></div></div>'''
fix('{{PE_COMPARISON_BARS}}', pe_bars)
fix('{{PE_ANALYSIS}}', '兆易PE(TTM)约227x，显著高于全球同业（华邦30x/旺宏45x），高估值主要反映了国产替代+DRAM期权价值。市净率PB 20x，PS(TTM) 22x，均偏高。')

# ===== M7 行业空间/竞争 =====
fix('{{COMPETITOR_1}}', '华邦电子')
fix('{{COMPETITOR_1_SEGMENT}}', 'NOR Flash')
fix('{{COMPETITOR_1_ANALYSIS}}', '全球NOR Flash龙头（市占率约28%），产品线覆盖全市场，先进制程领先，但主要市场在境外')
fix('{{COMPETITOR_2}}', '旺宏电子')
fix('{{COMPETITOR_2_SEGMENT}}', 'NOR Flash')
fix('{{COMPETITOR_2_ANALYSIS}}', '全球第二（约22%），专注高容量NOR产品，车规认证完善，受益于AI端侧推理容量升级')
fix('{{COMPETITOR_3}}', '普冉股份')
fix('{{COMPETITOR_3_SEGMENT}}', 'NOR Flash + MCU')
fix('{{COMPETITOR_3_ANALYSIS}}', '国内NOR Flash新锐，以SONOS工艺实现低功耗优势，成长快速，对兆易形成直接竞争')
fix('{{COMPETITOR_4}}', '意法半导体(ST)')
fix('{{COMPETITOR_ADVANTAGE}}', '兆易优势在于双平台（NOR+MCU）架构，国内客户关系深厚。劣势在于制程落后、规模较小、国际品牌影响力弱')
fix('{{CORE_BUSINESS}}', '兆易创新核心竞争优势在于NOR Flash和MCU双平台协同：存储业务提供现金流，MCU构建生态粘性，DRAM打开增长空间')

# ===== M8 催化剂/三情景 =====
fix('{{OPTIMISTIC_PRICE}}', '~760元')
fix('{{OPTIMISTIC_RETURN}}', '+30%')
fix('{{OPTIMISTIC_SCENARIO}}', 'DRAM放量超预期+AI端侧NOR升级周期+MCU毛利率改善至40%+，2026年净利突破25亿')
fix('{{BASE_PRICE}}', '530-560元')
fix('{{BASE_RETURN}}', '持平~-5%')
fix('{{BASE_SCENARIO}}', '行业温和复苏，NOR量价稳中有升，DRAM如期推进但贡献有限，2026年净利18-20亿')
fix('{{PESS_PRICE}}', '~350元')
fix('{{PESS_RETURN}}', '-40%')
fix('{{PESS_SCENARIO}}', '半导体周期再度下行+NOR Flash价格战升级+DRAM进展不及预期，净利回落至10亿以下')

# ===== M9 预期差 =====
# Place in template is in RISK_ITEM_1/2/3 area
fix('{{RISK_ITEM_1}}', 'DRAM业务价值')
fix('{{RISK_ITEM_2}}', 'AI端侧需求')
fix('{{RISK_ITEM_3}}', '周期判断')

# ===== M10 风险 =====

# ===== HIGHLIGHTS =====
fix('{{HIGHLIGHT_1_TITLE}}', 'NOR Flash全球第三')
fix('{{HIGHLIGHT_1_DESC}}', '兆易创新在NOR Flash领域全球市占率约18%，排名第三，2025年存储芯片收入65.66亿元（+26.4%），毛利率42.84%。')
fix('{{HIGHLIGHT_2_TITLE}}', 'MCU国内龙头')
fix('{{HIGHLIGHT_2_DESC}}', 'GD32系列MCU累计出货超10亿颗，是中国最大的Arm通用MCU供应商，构建了完善的开发工具链和生态。')
fix('{{HIGHLIGHT_3_TITLE}}', 'DRAM第三曲线')
fix('{{HIGHLIGHT_3_DESC}}', '利基DRAM产品已进入客户导入阶段，布局百亿市场空间，有望成为公司第三增长极。')

# ===== RISK TITLES =====
fix('{{RISK_TITLE_1}}', '半导体周期下行')
fix('{{RISK_TITLE_3}}', '高估值回调')
fix('{{RISK_2_TITLE}}', 'NOR Flash价格战')
fix('{{RISK_2_DESC}}', '行业尚未出清，NOR Flash单价在底部徘徊。若价格战持续，公司毛利率和净利率将承压，估值消化周期拉长。')
fix('{{CORE_RISK_FOCUS}}', '半导体强周期、PE>200x安全边际不足、创始人减持压制信心')
fix('{{FINANCIAL_CONTROLLABLE}}', '公司资产负债率仅10.2%，无有息负债，货币资金85亿充裕。财务风险可控，大股东减持更多是情绪冲击而非基本面问题')

# ===== ANALYSIS_TEXT (多出现象) =====
fix('{{ANALYSIS_TEXT}}', '兆易创新作为国内存储芯片与MCU双轮驱动的IC设计龙头，NOR Flash全球第三、MCU国内领先，具备较强的技术平台和产品线广度。但半导体行业强周期属性、当前PE估值超200x、产品价格底部尚未确认回升是多方面制约因素。综合评分为6.5/10，属中等偏上。')

# ===== 价值投资理念表 (M1-M11) =====
fix('{{M1_ANALYSIS}}', '巴菲特好生意：高频刚需+双产品轮动，NOR Flash全球第三、MCU国内第一，营收从2021年85亿稳步增长至2025年92亿（+25%YoY），ROE 9.3%正在修复路径上')
fix('{{M2_ANALYSIS}}', '巴菲特护城河：技术积累（NOR Flash市占18%+专利超千项）和生态绑定（GD32 MCU累计10亿颗出货）构成一定护城河，但Fabless模式下技术壁垒有限，护城河评分7.2/10')
fix('{{M3_ANALYSIS}}', '彼得林奇管理层：创始人朱一明技术出身、深耕半导体20年，核心团队稳定。偏技术驱动型管理，但2026年减持计划对市场信心构成短期压制')
fix('{{M4_ANALYSIS}}', '格雷厄姆财务：资产负债率10.2%极低、无有息负债、经营现金流21亿覆盖净利1.29倍，财务结构安全。但ROE 9.3%偏低，净利率从25%到4%波动大')
fix('{{M5_ANALYSIS}}', '巴菲特成本意识：研发费用11.17亿（12%营收）保持高强度投入，Fabless轻资产模式固定成本低，但代工成本占比~65%，对晶圆厂议价力弱')
fix('{{M6_ANALYSIS}}', '巴菲特估值原则：PE 227x/扣非PE 244x/PB 20x，三口径一致偏高。高估值已隐含大量乐观预期，需业绩持续超预期来消化，安全边际不足')
fix('{{M7_ANALYSIS}}', '彼得林奇市占率：NOR Flash全球18%（第三）、MCU~1.8%全球份额（国内领先），利基DRAM从0到1突破，市占率提升路径清晰')
fix('{{M8_ANALYSIS}}', '费雪催化剂：①DRAM突破（百亿市场）、②AI端侧NOR升级（3-5倍容量需求）、③车规MCU放量（AEC-Q100完成），三催化剂确定性较高')
fix('{{M9_ANALYSIS}}', '卡拉曼预期差：市场可能低估三方面——①DRAM期权价值、②AI端侧NOR量价弹性、③MCU毛利率改善空间。当前PE已隐含部分预期但仍有未被定价的成长潜力')
fix('{{M10_ANALYSIS}}', '邓普顿风险：核心风险排序——①周期下行（净利可波动10x+）、②价格战持续、③DRAM拓展失败、④创始人减持。四项风险均需密切跟踪')
fix('{{M11_SAFETY_MARGIN}}', '综合安全边际评估：当前价格（586元）对应的PE 227x远超合理估值区间。即使按2026年净利20亿乐观估算，PE仍超200x。建议PE回落至100x以下（约250元）再考虑配置')

# ===== DEBT_RATIO_NOTE =====
fix('{{DEBT_RATIO_NOTE}}', '资产负债率仅10.2%（2025年），无有息负债，货币资金85亿充裕。公司经营现金流21.21亿覆盖净利1.29倍，财务结构非常安全。')

# ===== CORE_BUSINESS =====
fix('{{CORE_BUSINESS}}', '兆易创新以NOR Flash存储器为基本盘（存储芯片收入65.66亿，占比71.3%），以MCU为第二增长曲线（19.10亿，20.8%），传感器和模拟芯片为辅（7.27亿，7.9%）。三业务形成存储+控制+感知的全产品矩阵。')

# ===== DIM 六维评分 =====
# 六维评分直接用整块替换
dim_block = '''  <!-- 六维评分使用hl/ht/hf样式，宽度=分数×10% -->
  <div class="hb"><span class="hl">商业模式</span><div class="ht"><div class="hf c7" style="width:70%">7</div></div></div>
  <div class="hb"><span class="hl">护城河</span><div class="ht"><div class="hf c7" style="width:70%">7</div></div></div>
  <div class="hb"><span class="hl">管理层</span><div class="ht"><div class="hf c7" style="width:70%">7</div></div></div>
  <div class="hb"><span class="hl">财务健康</span><div class="ht"><div class="hf c6" style="width:60%">6</div></div></div>
  <div class="hb"><span class="hl">成长弹性</span><div class="ht"><div class="hf c8" style="width:80%">8</div></div></div>
  <div class="hb"><span class="hl">估值安全</span><div class="ht"><div class="hf c5" style="width:50%">5</div></div></div>'''

fix('{{DIM_BAR_1}}', 'width:70%')
fix('{{DIM_SCORE_1}}', '7')
fix('{{DIM_BAR_2}}', 'width:70%')
fix('{{DIM_SCORE_2}}', '7')
fix('{{DIM_BAR_3}}', 'width:70%')
fix('{{DIM_SCORE_3}}', '7')
fix('{{DIM_BAR_4}}', 'width:60%')
fix('{{DIM_SCORE_4}}', '6')
fix('{{DIM_BAR_5}}', 'width:80%')
fix('{{DIM_SCORE_5}}', '8')
fix('{{DIM_BAR_6}}', 'width:50%')
fix('{{DIM_SCORE_6}}', '5')
fix('{{DIM_BAR_X}}', '')

# ===== BQ × 13 =====
bqs = [
    # BQ1 - 综合评价
    '兆易创新是国内存储芯片和MCU双平台IC设计龙头，2025年营收92亿元（+25%），净利16.5亿元（+50%），周期底部持续修复。但当前PE>200x反映估值已隐含较高预期，综合评分6.5/10。',
    # BQ2 - M1 商业模式
    '护城河评分7.2/10。NOR Flash全球第三（~18%份额）、GD32 MCU国内领先形成双平台壁垒，但技术门槛相对有限（55nm主力制程），华邦/旺宏/普冉等竞争激烈。车规AEC-Q100认证已完成，车规MCU已量产出货，车规准入壁垒是差异化优势。',
    # BQ3 - M2 壁垒
    '核心管理层均具有15年以上半导体行业经验，技术型管理团队。偏技术驱动型管理，注重产品研发和平台化布局，经营风格稳健。董事会2024年完成换届，独立董事占比符合监管要求。2026年创始人减持计划需关注。',
    # BQ4 - M3 管理层
    '财务健康评分7/10。亮点：无有息负债、经营现金流21亿覆盖净利129%、轻资产FCF充沛。瑕疵：ROE仅9.3%（周期低谷恢复中）、净利率从2021年25%到2023年3%波动剧烈，盈利稳定性是核心关注点。',
    # BQ5 - M4 财务
    '成本结构健康，研发费用11.17亿（占比12.1%）、销售费用4.46亿、管理费用6.12亿。Fabless轻资产模式FCF充沛，但无自有产能导致代工成本随晶圆厂议价波动。资产负债率仅10.2%，财务结构安全。',
    # BQ6 - M5 成本
    '估值判断：三个口径一致偏高。归母PE 227x/扣非PE 244x/PB 20x，均显著高于全球同业（华邦30x/旺宏45x）。高估值反映了国产替代+DRAM新业务的乐观预期，但这也意味着安全边际极低，需业绩持续超预期来消化。',
    # BQ7 - M6 估值
    'NOR Flash全球40亿美元市场，兆易第三（18%）；MCU 250亿美元市场，兆易全球~1.8%（国内领先）。行业驱动力：AI端侧推理（容量升级）、IoT设备增长、汽车电子化深化。2025年公司市占率全面提升。',
    # BQ8 - M7 市占率
    '三大催化剂：①DRAM从0到1突破（利基DRAM百亿市场）；②AI端侧NOR Flash容量升级（需求3-5倍提升）；③车规MCU放量（AEC-Q100认证已完成）。三情景预测区间：350-760元，基准530-560元。',
    # BQ9 - M8 催化剂
    '市场可能低估了三方面：①DRAM业务价值（当前股价几乎未包含DRAM预期）；②AI端侧推理对NOR Flash量价齐升的拉动幅度；③MCU业务毛利率从35%升至40%+的改善空间。高PE中隐含了部分预期但仍有未被定价的成长潜力。',
    # BQ10 - M9 预期差
    '核心风险：①半导体周期下行（强周期属性，净利可波动10倍+）；②NOR Flash价格战（行业尚未出清）；③DRAM拓展不及预期；④创始人减持（套现28亿压制信心）。综合判断：估值偏高叠加周期不确定性，当前时点风险收益比不佳。',
    # BQ11 - M10 风险
    '兆易创新是国内半导体设计领域稀缺的平台型公司，NOR Flash+MCU双轮驱动稳健，DRAM第三曲线打开想象空间。但当前估值已隐含了较高的增长预期，且半导体强周期属性使盈利可预测性差。建议等待PE回落至100x以下再行配置。',
    # BQ12 - M11 综合评级
    '行业竞争激烈但格局已形成"三强（华邦/旺宏/兆易）+多小"的稳定态势，兆易凭借国内客户关系和GD32 MCU生态，在国产替代浪潮中位置稳固。但价格战持续（2025年行业尚未出清）是中期压力。',
    # BQ13 - 其他/BQ
    '最终结论：兆易创新是国内存储芯片与MCU双平台IC设计龙头。公司以NOR Flash为基石（全球第三），以MCU为增长引擎（国内领先），正向DRAM拓展第三极。2025年营收92亿元、净利16.5亿元（+50%YoY），周期修复态势明确。但PE 227x的估值已大量透支乐观预期，风险收益比不佳，建议等待更合理的入场价格。',
]

# 替换BQ — 收集所有位置从后往前替换
bq_positions = []
for m in re.finditer(r'<div class="bq"[^>]*>', c):
    # 用深度计数器找真正的闭合div
    start = m.start()
    depth = 0
    i = start
    while i < len(c):
        if c[i:i+4] == '<div':
            depth += 1
            i += 4
        elif c[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                bq_positions.append((start, i + 6))
                break
            i += 6
        else:
            i += 1

print(f"Found {len(bq_positions)} BQ positions")

# 从后往前替换
for i, (pos, end) in enumerate(reversed(bq_positions)):
    actual_idx = len(bq_positions) - 1 - i
    if actual_idx < len(bqs):
        new_block = f'<div class="bq">{bqs[actual_idx]}</div>'
        c = c[:pos] + new_block + c[end:]
        fixes += 1

# ===== 保存 =====
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print(f'\n✅ Fill script completed: {fixes} replacements')
print(f'Remaining {{}}: {len(set(re.findall(r"\{\{[A-Z_0-9]+\}\}", c)))}')
print(f'__TODO__ count: {c.count("__TODO__")}')
