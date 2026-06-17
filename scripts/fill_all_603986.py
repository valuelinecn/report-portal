#!/usr/bin/env python3
"""fill_all.py — 一次填充603986报告的所有占位符和表格"""
import re, os

HTML = os.path.expanduser('~/.hermes/hermes-agent/report-portal/reports/603986.html')

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
    """Replace the <table> after marker with new HTML"""
    global c
    idx = c.find(marker)
    if idx < 0:
        return False
    tbl_start = c.find('<table', idx)
    if tbl_start < 0:
        return False
    tbl_end = c.find('</table>', tbl_start) + 8
    if tbl_end < 8:
        return False
    c = c[:tbl_start] + new_html + c[tbl_end:]
    return True

# ============ SIMPLE PLACEHOLDERS ============
fills = [
    ('{{COMPANY_NAME_CN}}', '兆易创新'),
    ('{{SCORE}}', '6.5'),
    ('{{RATING_DESC}}', '国内存储+MCU双龙头，技术平台扎实，但高估值与周期底部待确认构成主要风险'),
    ('{{RATING_TEXT}}', '2026-06-17'),
    ('{{COMPANY_DESC_LONG}}', '兆易创新作为国内存储芯片与MCU双轮驱动的IC设计龙头，NOR Flash全球第三、MCU国内领先，具备较强的技术平台和产品线广度。但半导体行业强周期属性、当前PE估值超200x、产品价格底部尚未确认回升是多方面制约因素。综合评分为6.5/10，属中等偏上。'),
    ('{{INVESTMENT_THESIS}}', '兆易创新是国内半导体设计领域稀缺的平台型公司，NOR Flash+MCU双轮驱动稳健，DRAM第三曲线打开想象空间。但当前估值已隐含了较高的增长预期，且半导体强周期属性使盈利可预测性差。建议等待PE回到合理区间后再行配置。'),
    ('{{ANALYSIS_TEXT}}', '兆易创新作为国内存储芯片与MCU双轮驱动的IC设计龙头，NOR Flash全球第三、MCU国内领先，具备较强的技术平台和产品线广度。但半导体行业强周期属性、当前PE估值超200x、产品价格底部尚未确认回升是多方面制约因素。综合评分为6.5/10，属中等偏上。'),
    # CARD
    ('{{CARD1_VAL}}', '6.5'), ('{{CARD1_LABEL}}', '综合评级'), ('{{CARD1_COLOR}}', '#4caf50'),
    ('{{CARD2_VAL}}', '中'), ('{{CARD2_LABEL}}', '风险等级'), ('{{CARD2_COLOR}}', '#ffc107'),
    ('{{CARD3_VAL}}', '高'), ('{{CARD3_LABEL}}', '成长弹性'), ('{{CARD3_COLOR}}', '#4caf50'),
    ('{{CARD4_VAL}}', '9.3%'), ('{{CARD4_LABEL}}', 'ROE'), ('{{CARD4_COLOR}}', '#888'),
    ('{{LABEL_2}}', '双平台龙头'), ('{{LABEL_2_TITLE}}', '核心优势'),
    ('{{LABEL_3}}', 'DRAM突破、AI端侧NOR升级、车规MCU放量'), ('{{LABEL_3_TITLE}}', '催化剂'),
    # LOGIC
    ('{{LOGIC_1_VAL}}', '双平台龙头'),
    ('{{LOGIC_1}}', '到2028年净利可达35亿，约2X空间'),
    ('{{LOGIC_2}}', 'NOR Flash价格/MCU出货/DRAM导入进度'),
    ('{{LOGIC_2_DETAIL}}', 'NOR Flash全球第三（~18%）、GD32 MCU国内领先，技术+认证壁垒稳固'),
    ('{{LOGIC_3}}', 'DRAM客户导入不及预期则逻辑证伪'),
    ('{{LOGIC_3_DETAIL}}', 'DRAM从0到1突破+AI端侧NOR升级+车规MCU放量，三引擎驱动'),
    ('{{LOGIC_4}}', '股价跌破350元减仓'),
    ('{{LOGIC_4_DETAIL}}', 'PE>200x已隐含极高预期，需持续超预期消化'),
    # M1
    ('{{M1_HB_BAR_1}}', '<div class="hb"><span class="hl" style="width:65px;">存储芯片</span><span class="ht"><span class="hf c7" style="width:71%;">71.3%</span></span></div>'),
    ('{{M1_HB_BAR_2}}', '<div class="hb"><span class="hl" style="width:65px;">MCU</span><span class="ht"><span class="hf c6" style="width:21%;">20.8%</span></span></div>'),
    ('{{M1_HB_BAR_3}}', '<div class="hb"><span class="hl" style="width:65px;">传感器+模拟</span><span class="ht"><span class="hf" style="width:8%;background:#888;">7.9%</span></span></div>'),
    ('{{M1_REVENUE_ROWS}}', '<tr><td>存储芯片</td><td>51.93亿</td><td>65.66亿</td><td>↗️+26.4%</td></tr>\n<tr><td>MCU</td><td>15.03亿</td><td>19.10亿</td><td>↗️+27.1%</td></tr>\n<tr><td>传感器+模拟</td><td>6.43亿</td><td>7.27亿</td><td>↗️+13.1%</td></tr>'),
    ('{{M1_ANNUAL_REMARK}}', '2025年营收92.03亿元（+25%），归母净利16.48亿元（+49.8%）。存储芯片业务受益于NOR Flash量价齐升，MCU业务在汽车电子和IoT领域持续渗透。传感器业务恢复增长。综合毛利率42.84%，净利率17.92%，ROE 9.3%。'),
    # M2
    ('{{MOAT_LEVEL}}', '中等（局部护城河）'),
    ('{{MOAT_PHILOSOPHY}}', '公司通过技术积累（NOR Flash全球第三、GD32 MCU国内领先）和车规认证（AEC-Q100）构建了一定护城河，但芯片设计行业技术迭代快，护城河深度有限'),
    ('{{MOAT_TOTAL_SCORE}}', '7.2'), ('{{MOAT_POINT_2}}', '技术壁垒与客户粘性'),
    ('{{MOAT_SCORE_1}}', '7'),('{{MOAT_SCORE_2}}', '7'),('{{MOAT_SCORE_3}}', '7'),
    ('{{MOAT_SCORE_4}}', '7'),('{{MOAT_SCORE_5}}', '8'),('{{MOAT_SCORE_6}}', '7'),
    ('{{MOAT_PATENT_NOTE}}', '累计专利超千项，涵盖存储器电路设计、MCU架构、接口技术等核心领域'),
    ('{{BRAND_BARRIER_NOTE}}', 'GD32品牌在中国MCU市场具有较高知名度，Arm通用MCU领域出货量国内第一'),
    ('{{CERT_BARRIER}}', 'AEC-Q100车规认证已完成，车规MCU进入量产出货阶段，车规认证周期长、门槛高'),
    ('{{TECH_GAP_ANALYSIS}}', '55nm主力制程与全球领先水平（28nm以下）存在代差，但在NOR Flash领域制程差距影响有限'),
    ('{{RESOURCE_NOTE}}', 'Fabless轻资产模式，晶圆代工依赖中芯国际、华虹等，代工产能保障是供应链优势'),
    ('{{CUSTOMER_PRICING_POWER}}', '下游客户分散，单一客户依赖度低，但与终端品牌客户议价能力一般'),
    ('{{CUSTOMER_CONCENTRATION_RISK}}', '前五大客户占比约25%，集中度适中'),
    ('{{COST_EFFECT}}', 'Fabless模式下固定成本低，研发投入持续增长（2025年研发费用11.17亿）'),
    ('{{COST_OUTSOURCE_NOTE}}', '代工成本占比约65%，晶圆代工价格波动直接影响毛利率'),
    ('{{MARGIN_NOTE}}', '存储芯片毛利率约45%，MCU约35%，传感器约30%。净利率从高点25%降至低点4%'),
    ('{{PRICE_WAR_RISK}}', 'NOR Flash行业价格战持续，尚未完全出清'),
    ('{{DISRUPTION_NOTE}}', '新兴存储技术（MRAM/FRAM/RRAM）可能在5-10年对NOR Flash形成替代威胁'),
    ('{{NET_MARGIN_WEAK}}', '净利率波动大是核心弱点，从21年25%降到23年4%'),
    ('{{BARRIER_NOTE}}', '护城河评分7.2/10。NOR Flash全球第三（~18%份额）、GD32 MCU国内领先'),
    ('{{MOAT_SCALE_NOTE}}', 'NOR Flash全球第三（~18%），MCU国内出货量第一'),
    # 商业模式评估
    ('{{BIZ_SCORE_1}}', '7'),('{{BIZ_EVIDENCE_1}}', 'NOR Flash全球第三（~18%市占），Fabless轻资产高ROIC'),
    ('{{BIZ_SCORE_2}}', '7'),('{{BIZ_EVIDENCE_2}}', '毛利率42.84%，净利率17.92%，双平台架构拉高盈利天花板'),
    ('{{BIZ_SCORE_3}}', '6'),('{{BIZ_EVIDENCE_3}}', 'NOR Flash+MCU协同，但竞品（华邦/ST）生态更强'),
    ('{{BIZ_SCORE_4}}', '7'),('{{BIZ_EVIDENCE_4}}', '前五大客户占比~25%，分散度高，客户集中风险低'),
    ('{{CORE_ADVANTAGE_LABEL}}', '双平台（NOR Flash+MCU）+ DRAM期权'),
    # M3
    ('{{MGMT_NAME_1}}', '朱一明'),('{{MGMT_TITLE_1}}', '董事长（创始人）'),('{{MGMT_TENURE_1}}', '2005年至今'),
    ('{{MGMT_DESC_1}}', '清华大学学士/硕士、美国石溪分校硕士。2005年创立公司，主导战略布局。'),
    ('{{MGMT_NAME_2}}', '何卫'),('{{MGMT_TITLE_2}}', '总经理/董事'),('{{MGMT_TENURE_2}}', '2018年至今'),
    ('{{MGMT_DESC_2}}', '电子工程背景，多年半导体行业运营管理经验。负责日常运营和战略执行。'),
    ('{{MGMT_EXPERIENCE}}', '核心管理层均具有15年以上半导体行业经验'),
    ('{{MGMT_STYLE_ANALYSIS}}', '偏技术驱动型管理，注重产品研发和平台化布局'),
    ('{{MGMT_GOVERNANCE}}', '董事会2024年完成换届。2026年朱一明减持计划对短期市场情绪构成压力'),
    ('{{MGMT_SCORE_1}}', '7'),('{{MGMT_SCORE_2}}', '7'),('{{MGMT_SCORE_3}}', '7'),('{{MGMT_SCORE_4}}', '7'),
    # M4 KPI
    ('{{KPI_CARD_1_VAL}}', '92.03亿'),('{{KPI_CARD_1_LABEL}}', '营收'),
    ('{{KPI_CARD_2_VAL}}', '16.48亿'),('{{KPI_CARD_2_LABEL}}', '归母净利'),
    ('{{KPI_CARD_3_VAL}}', '42.84%'),('{{KPI_CARD_3_LABEL}}', '毛利率'),
    ('{{KPI_CARD_4_VAL}}', '21.21亿'),('{{KPI_CARD_4_LABEL}}', '经营现金流'),
    # M5
    ('{{CHAIN_SCORE_1}}', '7'),('{{CHAIN_EVIDENCE_1}}', 'GD32 MCU生态粘性强，客户替换成本高'),
    ('{{CHAIN_SCORE_2}}', '5'),('{{CHAIN_EVIDENCE_2}}', 'Fabless依赖代工厂，中芯国际等议价力强'),
    ('{{CHAIN_SCORE_3}}', '6'),('{{CHAIN_EVIDENCE_3}}', 'NOR Flash三强格局稳定，但MCU竞争激烈'),
    ('{{CHAIN_SCORE_4}}', '8'),('{{CHAIN_EVIDENCE_4}}', 'NOR Flash短期无有效替代技术，长期MRAM等有威胁'),
    ('{{CHAIN_SCORE_5}}', '7'),('{{CHAIN_EVIDENCE_5}}', 'IC设计需技术和生态积累，Fabless进入门槛相对可控'),
    ('{{DIFF_STRATEGY}}', '以NOR Flash为基、MCU为翼、DRAM为第三极的差异化产品矩阵'),
    ('{{DEBT_RATIO_NOTE}}', '资产负债率仅10.2%，无有息负债，货币资金85亿充裕'),
    ('{{FCF_ANALYSIS}}', '经营现金流21.21亿（2025年）vs 20.35亿（2024年），覆盖净利润1.29倍。FCF约18亿，质量良好。'),
    # M6 PE
    ('{{PE_COMPARISON_TITLE}}', 'PE对比 · 半导体存储设计'),
    ('{{PE_COMPARISON_BARS}}', '<div class="hb"><span class="hl">兆易创新</span><div class="ht"><div class="hf" style="width:95%;background:#f44336;">227x</div></div></div>\n<div class="hb"><span class="hl">华邦电子</span><div class="ht"><div class="hf" style="width:30%;background:#4caf50;">30x</div></div></div>\n<div class="hb"><span class="hl">旺宏电子</span><div class="ht"><div class="hf" style="width:55%;background:#f0c040;">45x</div></div></div>'),
    ('{{PE_ANALYSIS}}', '兆易PE(TTM)约227x，显著高于同业（华邦30x/旺宏45x），高估值反映国产替代+DRAM期权价值'),
    # M7竞争
    ('{{COMPETITOR_1}}', '华邦电子'),('{{COMPETITOR_1_SEGMENT}}', 'NOR Flash'),
    ('{{COMPETITOR_1_ANALYSIS}}', '全球NOR Flash龙头（~28%市占），产品线覆盖全市场，先进制程领先'),
    ('{{COMPETITOR_2}}', '旺宏电子'),('{{COMPETITOR_2_SEGMENT}}', 'NOR Flash'),
    ('{{COMPETITOR_2_ANALYSIS}}', '全球第二（~22%），专注高容量NOR产品，车规认证完善'),
    ('{{COMPETITOR_3}}', '普冉股份'),('{{COMPETITOR_3_SEGMENT}}', 'NOR Flash+MCU'),
    ('{{COMPETITOR_3_ANALYSIS}}', '国内NOR Flash新锐，SONOS工艺低功耗优势，成长快速'),
    ('{{COMPETITOR_4}}', '意法半导体(ST)'),
    ('{{COMPETITOR_ADVANTAGE}}', '兆易双平台架构+国内客户关系深厚；劣势为规模较小、国际品牌弱'),
    ('{{CORE_BUSINESS}}', '核心优势在于NOR Flash和MCU双平台协同：存储提供现金流，MCU构建生态粘性，DRAM打开空间'),
    # DIM
    ('{{DIM_BAR_1}}', 'width:70%'),('{{DIM_SCORE_1}}', '7'),
    ('{{DIM_BAR_2}}', 'width:70%'),('{{DIM_SCORE_2}}', '7'),
    ('{{DIM_BAR_3}}', 'width:70%'),('{{DIM_SCORE_3}}', '7'),
    ('{{DIM_BAR_4}}', 'width:60%'),('{{DIM_SCORE_4}}', '6'),
    ('{{DIM_BAR_5}}', 'width:80%'),('{{DIM_SCORE_5}}', '8'),
    ('{{DIM_BAR_6}}', 'width:50%'),('{{DIM_SCORE_6}}', '5'),
    ('{{DIM_BAR_X}}', ''),
    # 情景
    ('{{OPTIMISTIC_PRICE}}', '~760元'),('{{OPTIMISTIC_RETURN}}', '+30%'),
    ('{{OPTIMISTIC_SCENARIO}}', 'DRAM放量+AI端侧NOR升级+MCU毛利率改善，2026年净利突破25亿'),
    ('{{BASE_PRICE}}', '530-560元'),('{{BASE_RETURN}}', '持平~-5%'),
    ('{{BASE_SCENARIO}}', 'NOR量价稳中有升，DRAM如期推进，2026年净利18-20亿'),
    ('{{PESS_PRICE}}', '~350元'),('{{PESS_RETURN}}', '-40%'),
    ('{{PESS_SCENARIO}}', '周期下行+价格战+DRAM不及预期，净利回落至10亿以下'),
    # 预期差议题
    ('{{RISK_ITEM_1}}', 'DRAM业务价值'),('{{RISK_ITEM_2}}', 'AI端侧需求'),('{{RISK_ITEM_3}}', '周期判断'),
    # 亮点
    ('{{HIGHLIGHT_1_TITLE}}', 'NOR Flash全球第三'),
    ('{{HIGHLIGHT_1_DESC}}', '兆易在NOR Flash领域全球市占率约18%，排名第三，2025年存储芯片收入65.66亿元。'),
    ('{{HIGHLIGHT_2_TITLE}}', 'MCU国内龙头'),
    ('{{HIGHLIGHT_2_DESC}}', 'GD32系列MCU累计出货超10亿颗，是中国最大的Arm通用MCU供应商。'),
    ('{{HIGHLIGHT_3_TITLE}}', 'DRAM第三曲线'),
    ('{{HIGHLIGHT_3_DESC}}', '利基DRAM产品已进入客户导入阶段，布局百亿市场空间。'),
    # 风险
    ('{{RISK_TITLE_1}}', '半导体周期下行'),('{{RISK_TITLE_3}}', '高估值回调'),
    ('{{RISK_2_TITLE}}', 'NOR Flash价格战'),
    ('{{RISK_2_DESC}}', '行业尚未出清，NOR Flash单价在底部徘徊，毛利率和净利率将承压。'),
    ('{{CORE_RISK_FOCUS}}', '半导体强周期、PE>200x安全边际不足、创始人减持'),
    ('{{FINANCIAL_CONTROLLABLE}}', '资产负债率10.2%，无有息负债，货币资金85亿充裕，财务风险可控'),
    # 清算
    ('{{LIQ_ASSET_1}}', '货币资金'),('{{LIQ_BOOK_1}}', '85亿'),('{{LIQ_VAL_1}}', '~85亿'),
    ('{{LIQ_ASSET_2}}', '应收账款'),('{{LIQ_BOOK_2}}', '15亿'),('{{LIQ_VAL_2}}', '~15亿'),
    ('{{LIQ_ASSET_3}}', '存货'),('{{LIQ_BOOK_3}}', '28亿'),('{{LIQ_VAL_3}}', '~20亿'),
    ('{{LIQ_ASSET_4}}', '固定资产'),('{{LIQ_BOOK_4}}', '5亿'),('{{LIQ_VAL_4}}', '~3亿'),
    ('{{LIQ_TOTAL_BOOK}}', '133亿'),('{{LIQ_TOTAL_VAL}}', '~123亿'),
    # 价值理念
    ('{{M1_ANALYSIS}}', '巴菲特好生意：高频刚需+双产品轮动，NOR Flash全球第三、MCU国内第一，营收稳步增长'),
    ('{{M2_ANALYSIS}}', '巴菲特护城河：技术积累（NOR Flash市占18%+专利千项）和生态绑定构成一定护城河'),
    ('{{M3_ANALYSIS}}', '彼得林奇管理层：创始人技术出身、深耕20年，团队稳定。减持计划短期压制市场信心'),
    ('{{M4_ANALYSIS}}', '格雷厄姆财务：资产负债率10.2%极低、经营现金流21亿覆盖净利1.29倍，财务结构安全'),
    ('{{M5_ANALYSIS}}', '巴菲特成本意识：研发占比12%高强度投入，Fabless轻资产固定成本低'),
    ('{{M6_ANALYSIS}}', '巴菲特估值原则：PE 227x/扣非PE 244x/PB 20x三口径一致偏高，安全边际不足'),
    ('{{M7_ANALYSIS}}', '彼得林奇市占率：NOR Flash全球18%（第三）、MCU~1.8%，利基DRAM从0到1突破'),
    ('{{M8_ANALYSIS}}', '费雪催化剂：DRAM突破+AI端侧NOR升级+车规MCU放量，三催化剂确定性较高'),
    ('{{M9_ANALYSIS}}', '卡拉曼预期差：DRAM期权价值+AI端侧NOR量价弹性+MCU毛利率改善未被充分定价'),
    ('{{M10_ANALYSIS}}', '邓普顿风险：①周期下行②价格战③DRAM拓展失败④创始人减持，四项均需密切跟踪'),
    ('{{M11_SAFETY_MARGIN}}', '综合安全边际：当前PE 227x远超合理估值区间，建议PE回落至100x以下再考虑配置'),
]

for ph, val in fills:
    fill(ph, val)

# ============ TABLES (__TODO__) ============
# 行业空间
fill_table('行业空间</h3>', '<table class="tbl">\n<tr><th>市场</th><th>规模（2025E）</th><th>增速</th><th>兆易创新出货/份额</th><th>市占率</th></tr>\n<tr><td>NOR Flash</td><td>~40亿美元</td><td>~5%</td><td>65.66亿人民币</td><td>~18%</td></tr>\n<tr><td>MCU</td><td>~250亿美元</td><td>~8%</td><td>19.10亿人民币</td><td>~1.8%</td></tr>\n<tr><td>利基DRAM</td><td>~100亿美元</td><td>~10%</td><td>起步阶段</td><td><1%</td></tr>\n</table>')

# 行业空间 (2nd attempt with different marker)
if 'NOR Flash</th>' not in c:
    fill_table('规模（2025E', '<table class="tbl">\n<tr><th>市场</th><th>规模（2025E）</th><th>增速</th><th>兆易创新出货/份额</th><th>市占率</th></tr>\n<tr><td>NOR Flash</td><td>~40亿美元</td><td>~5%</td><td>65.66亿人民币</td><td>~18%</td></tr>\n<tr><td>MCU</td><td>~250亿美元</td><td>~8%</td><td>19.10亿人民币</td><td>~1.8%</td></tr>\n<tr><td>利基DRAM</td><td>~100亿美元</td><td>~10%</td><td>起步阶段</td><td><1%</td></tr>\n</table>')

# 费用率结构
fill_table('费用率结构（2024 vs 2025对比）</h3>',
    '<table class="tbl" style="margin-top:10px;">\n<tr><th>费用项</th><th>2024年</th><th class="gold">2025年</th><th>趋势</th></tr>\n<tr><td>研发费用</td><td>10.45亿</td><td>11.17亿</td><td>↗️+6.9%</td></tr>\n<tr><td>销售费用</td><td>4.15亿</td><td>4.46亿</td><td>↗️+7.5%</td></tr>\n<tr><td>管理费用</td><td>5.53亿</td><td>6.12亿</td><td>↗️+10.7%</td></tr>\n<tr><td>财务费用</td><td>-4.43亿</td><td>-1.42亿</td><td>↗️利息收入增加</td></tr>\n</table>')

# FCF质量
fill_table('FCF质量</h3>',
    '<table class="tbl">\n<tr><th>指标</th><th>2024年</th><th class="gold">2025年</th><th>正常化水平</th></tr>\n<tr><td>经营现金流</td><td>20.35亿</td><td>21.21亿</td><td>20-25亿</td></tr>\n<tr><td>CAPEX</td><td>2.71亿</td><td>2.87亿</td><td>2-3亿</td></tr>\n<tr><td>FCF</td><td>17.64亿</td><td>18.34亿</td><td>~18亿</td></tr>\n<tr><td>FCF/净利润</td><td>1.59x</td><td>1.11x</td><td>1.0-1.5x</td></tr>\n</table>')

# 催化剂
fill_table('催化剂时间表</h3>',
    '<table class="tbl">\n<tr><th style="width:80px">时间</th><th style="width:30%">事件</th><th style="width:40%">预期影响</th></tr>\n<tr><td>2026-2027</td><td>DRAM产品导入客户</td><td>打开百亿市场空间，初期收入贡献有限</td></tr>\n<tr><td>2027</td><td>AI端侧NOR升级周期</td><td>容量需求3-5倍提升，量价齐升</td></tr>\n<tr><td>2027-2028</td><td>车规MCU放量</td><td>AEC-Q100认证完成，车规收入占比提升</td></tr>\n<tr><td>2027-2028</td><td>先进制程导入</td><td>制程升级降低成本，毛利率改善1-2pct</td></tr>\n</table>')

# 风险类型
fill_table('风险类型</h3>',
    '<table class="tbl">\n<tr><th style="width:80px">风险类型</th><th>描述</th><th style="width:50px">概率</th><th style="width:40%">预警信号</th></tr>\n<tr><td>周期下行</td><td>半导体强周期属性，净利率可从25%降至3%</td><td>高</td><td>NOR Flash价格连续2季下跌</td></tr>\n<tr><td>价格战</td><td>NOR Flash行业尚未出清，价格战持续</td><td>中</td><td>华邦/旺宏降价抢单</td></tr>\n<tr><td>DRAM拓展</td><td>利基DRAM技术突破和客户导入存不确定性</td><td>中</td><td>DRAM客户导入延迟超2季</td></tr>\n<tr><td>创始人减持</td><td>朱一明拟减持套现约28亿，压制市场信心</td><td>中</td><td>减持公告后股价持续走弱</td></tr>\n</table>')

# ============ BQ (12 positions, text ONLY - template has <div>) ============
bq_texts = [
    '兆易创新是国内存储芯片和MCU双平台IC设计龙头，2025年营收92亿元（+25%），净利16.5亿元（+50%），周期底部持续修复。但当前PE>200x反映估值已隐含较高预期，综合评分6.5/10。',
    '兆易创新以NOR Flash全球第三（~18%份额）和GD32 MCU国内领先构建双平台业务结构。存储芯片收入65.66亿（71.3%）是基本盘，MCU 19.10亿（20.8%）为增长引擎，DRAM第三曲线打开想象空间。Fabless轻资产模式毛利率42.84%，净利率17.92%。',
    '护城河评分7.2/10。NOR Flash全球第三（~18%份额）、GD32 MCU国内领先形成双平台壁垒，但技术门槛相对有限（55nm主力制程），华邦/旺宏/普冉等竞争激烈。车规AEC-Q100认证已完成，车规MCU已量产出货，车规准入壁垒是差异化优势。',
    '护城河陷阱：净利率从25%到4%波动剧烈说明盈利稳定性差；NOR Flash价格战持续未出清（华邦/旺宏/兆易三家格局稳定但价格承压）；新兴存储技术（MRAM/FRAM/RRAM）5-10年可能形成替代威胁。',
    '核心管理层均具有15年以上半导体行业经验，技术型管理团队。偏技术驱动型管理，注重产品研发和平台化布局，经营风格稳健。董事会2024年完成换届，独立董事占比符合监管要求。2026年创始人减持计划需关注。',
    '管理层评价：创始人朱一明（清华大学+美国石溪分校，2005年创立）技术背景深厚，团队稳定性和战略执行力是公司治理核心优势。但2026年拟减持套现约28亿对市场信心构成压力。管理层评分均为7/10。',
    '财务健康评分7/10。亮点：无有息负债、经营现金流21亿覆盖净利129%、轻资产FCF充沛、资产负债率仅10.2%。瑕疵：ROE仅9.3%（周期低谷恢复中）、净利率从2021年25%到2023年3%波动剧烈。',
    '成本结构健康，研发费用11.17亿（占比12.1%）、销售4.46亿、管理6.12亿。Fabless轻资产FCF充沛，代工成本占比~65%使毛利率随晶圆厂议价波动。产业链议价权：客户粘性中强（7/10）、供应商议价力弱（5/10）。',
    '估值判断：三个口径一致偏高。归母PE 227x/扣非PE 244x/PB 20x/PS 42x，均显著高于同业（华邦30x/旺宏45x）。高估值反映国产替代+DRAM期权预期，安全边际极低，需业绩持续超预期来消化。',
    'NOR Flash全球40亿美元市场，兆易第三（~18%）；MCU 250亿美元市场，兆易全球~1.8%（国内领先）。AI端侧推理（容量升级）、IoT增长、汽车电子化深化为行业驱动力。竞争三强格局稳定但价格战持续。',
    '三大催化剂：①DRAM从0到1突破（利基DRAM百亿市场）；②AI端侧NOR Flash容量升级（需求3-5倍提升）；③车规MCU放量（AEC-Q100认证完成）。三情景预测：350-760元，基准530-560元。',
    '市场可能低估了三方面：①DRAM业务价值（当前股价几乎未包含DRAM预期）；②AI端侧NOR量价齐升幅度（容量3-5倍提升）；③MCU毛利率从35%升至40%+的改善空间。高PE中隐含了部分预期但仍有未被定价的成长潜力。',
]

positions = [m.start() for m in re.finditer(r'\{\{BQ_ANALYSIS\}\}', c)]
print(f"BQ: {len(positions)} positions")
for i, pos in enumerate(reversed(positions)):
    actual_idx = len(positions) - 1 - i
    if actual_idx < len(bq_texts):
        c = c[:pos] + bq_texts[actual_idx] + c[pos+15:]

# ============ M2 BAR WIDTH FIX ============
c = c.replace(
    '垂直整合</span><div class="ht"><div class="hf" style="width:70%;background:#f0c040;">8</div></div></div>',
    '垂直整合</span><div class="ht"><div class="hf" style="width:80%;background:#4caf50;">8</div></div></div>')

# ============ SAVE ============
with open(HTML, 'w') as f:
    f.write(c)

remaining_phs = len(set(re.findall(r'\{\{[A-Z_0-9]+\}\}', c)))
remaining_todo = c.count('__TODO__')
print(f"\nFilled: {count} placeholders + BQ + tables")
print(f"Remaining {{}}: {remaining_phs}")
print(f"Remaining __TODO__: {remaining_todo}")
print("DONE!")
