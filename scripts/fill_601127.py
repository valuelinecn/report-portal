#!/usr/bin/env python3
"""赛力斯(601127) 报告填充脚本"""
import re

REPORT = "/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports/601127.html"

with open(REPORT, 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

def replace_all(old, new, desc=""):
    global changes, html
    if old in html:
        html = html.replace(old, new)
        changes += 1
    else:
        if old.startswith('{{'):
            pass  # silent skip

# ===== 基础信息 =====
replace_all('{{COMPANY_NAME_CN}}', '赛力斯', '公司名')
replace_all('{{SCORE}}', '7.0', '评分')
replace_all('{{RATING_DESC}}', '赛力斯是华为智选车核心伙伴，问界品牌持续放量。2025年营收1650.54亿(+13.7%)净利59.57亿(+58.3%)。PE 20x偏合理偏低。华为生态+自研增程技术双轮驱动。', '评级')
replace_all('{{REPORT_DATE}}', '2026-06-18', '日期')

# ===== 综合评价卡片 =====
replace_all('{{CARD1_VAL}}', '7.0', '综合评级')
replace_all('{{CARD1_LABEL}}', '综合评级', '评级标签')
replace_all('{{CARD1_COLOR}}', '#4caf50', '评级颜色')
replace_all('{{CARD2_VAL}}', '中', '风险')
replace_all('{{CARD2_LABEL}}', '风险等级', '风险标签')
replace_all('{{CARD2_COLOR}}', '#f0c040', '风险颜色')
replace_all('{{CARD3_VAL}}', '高', '成长')
replace_all('{{CARD3_LABEL}}', '成长弹性', '成长标签')
replace_all('{{CARD3_COLOR}}', '#4caf50', '成长颜色')
replace_all('{{CARD4_VAL}}', '23.53%', 'ROE')
replace_all('{{CARD4_LABEL}}', 'ROE', 'ROE标签')
replace_all('{{CARD4_COLOR}}', '#4caf50', 'ROE颜色')

# ===== LOGIC卡 =====
replace_all('{{LOGIC_1_CONTENT}}', '华为智选车独家合作伙伴，问界品牌2025年销47.2万辆，营收1650亿净利60亿', 'LOGIC1')
replace_all('{{LOGIC_1_NOTE}}', '华为研发+赛力斯制造+鸿蒙生态，三重壁垒叠加', 'LOGIC1补')
replace_all('{{LOGIC_2_CONTENT}}', '华为技术背书+增程技术壁垒+智驾领先(ADS 4.0)', 'LOGIC2')
replace_all('{{LOGIC_2_NOTE}}', '稀缺性：华为智选模式仅此一家，竞品无法复制', 'LOGIC2补')
replace_all('{{LOGIC_3_CONTENT}}', '问界月销/智选车占比/毛利率趋势/研发投入/市占率变化', 'LOGIC3')
replace_all('{{LOGIC_3_NOTE}}', '季报重点关注M9/M8新车型爬坡和毛利率变化', 'LOGIC3补')
replace_all('{{LOGIC_4_CONTENT}}', 'PE 20x, PS 0.72x, PB 5.5x', 'LOGIC4')
replace_all('{{LOGIC_4_NOTE}}', 'PE在新能源车企中偏低，PS处于历史低位', 'LOGIC4补')

# ===== 综合评价BQ =====
replace_all('{{INVESTMENT_THESIS}}', '赛力斯核心价值在于华为智选车独家合作模式，问界品牌已形成高端认知。2025年营收1650亿净利60亿，ROE 23.53%优秀。PE 20x偏低，PS 0.72x历史低位。核心亮点：华为生态+增程技术+智驾领先，核心风险：销售费用率14.7%偏高、华为依赖度大。', '投资理念')

# ===== M1 =====
replace_all('{{ANALYSIS_TEXT}}', '赛力斯是华为智选车模式核心合作伙伴，运营问界品牌(AITO)。2025年新能源汽车销量47.23万辆(+10.6%)，营收1650.54亿(+13.69%)。华为在研发/品牌/渠道全栈赋能，赛力斯负责制造+供应链。问界品牌定位30-60万高端市场，已形成M5/M7/M9产品矩阵。', 'M1分析')
replace_all('{{M1_REVENUE_ROWS}}',
    '<tr><td>新能源汽车</td><td>135.49亿</td><td>1556.11亿</td><td>+14.9%</td>'
    '<tr><td>传统燃油车</td><td>34.46亿</td><td>19.03亿</td><td>-44.8%</td>'
    '<tr><td>其他</td><td>20.69亿</td><td>21.04亿</td><td>+1.6%</td>',
    'M1收入')
replace_all('{{M1_HB_BAR_1}}', '<div class="hb"><span class="hl">新能源汽车</span><div class="ht"><div class="hf" style="width:97%;background:#4caf50;">1556亿 · 97%</div></div></div>', '条1')
replace_all('{{M1_HB_BAR_2}}', '<div class="hb"><span class="hl">传统燃油车</span><div class="ht"><div class="hf" style="width:2%;background:#888;">19亿 · 1%</div></div></div>', '条2')
replace_all('{{M1_HB_BAR_3}}', '<div class="hb"><span class="hl">其他</span><div class="ht"><div class="hf" style="width:1%;background:#888;">21亿 · 1%</div></div></div>', '条3')
replace_all('{{M1_ANNUAL_REMARK}}', '新能源汽车占比从80%提升至97%，燃油车加速出清。问界M9(46万起)贡献主要利润增量。经销模式占比93%，直销占比7%。', 'M1备注')

# M1商业模式评估
for i in range(1, 5):
    replace_all(f'{{{{BIZ_SCORE_{i}}}}}', f'{8 if i==1 else 8 if i==2 else 9 if i==3 else 7}/10', f'M1分{i}')
evidences = ['华为独家合作+品牌溢价，问界已站稳高端', '增程+纯电双技术路线，研发投入80亿/年', '华为智选模式，渠道覆盖全国500+门店', 'C端客户为主，华为品牌认知带动转化']
for i, ev in enumerate(evidences, 1):
    replace_all(f'{{{{BIZ_EVIDENCE_{i}}}}}', ev, f'M1证据{i}')
replace_all('{{CORE_BUSINESS}}', '问界品牌新能源汽车为核心(97%营收)，M9为利润主力', '核心业务')

# ===== M2 壁垒 =====
moat_scores = [8, 9, 8, 7, 7, 6]
moat_colors = ['#4caf50', '#4caf50', '#4caf50', '#f0c040', '#f0c040', '#f0c040']
for i in range(1, 7):
    w = moat_scores[i-1] * 10
    replace_all(f'{{{{MOAT_BAR_{i}}}}}', f'width:{w}%;background:{moat_colors[i-1]}', f'M2条{i}')
    replace_all(f'{{{{MOAT_SCORE_{i}}}}}', str(moat_scores[i-1]), f'M2分{i}')
replace_all('{{MOAT_TOTAL_SCORE}}', '7.5', '壁垒总分')
replace_all('{{MOAT_LEVEL}}', '较深厚', '壁垒等级')
replace_all('{{MOAT_PHILOSOPHY}}', '核心壁垒在华为智选车独家合作模式+增程技术领先+问界品牌高端认知，三重壁垒叠加', '理念')
replace_all('{{MOAT_POINT_2}}', '增程技术壁垒：赛力斯增程技术研发多年，效率41%+行业领先，已形成专利护城河', '要点2')
replace_all('{{MOAT_SCALE_NOTE}}', '2025年新能源车销47.2万辆，高端SUV市占率~12%。问界M9连续多月50万+细分市场第一', '规模')
replace_all('{{MOAT_PATENT_NOTE}}', '增程技术+智驾相关专利超3000项，核心专利覆盖增程器/电池热管理/电驱', '专利')
replace_all('{{RESOURCE_NOTE}}', '华为研发团队+赛力斯制造基地+鸿蒙座舱/ADS智驾，资源禀赋独特', '资源')
replace_all('{{CERT_BARRIER}}', '新能源车生产资质+华为智选车准入门槛高，新玩家无法快速复制', '认证')
replace_all('{{COST_EFFECT}}', '规模效应显现：单车成本持续下降，毛利率28.76%(+2.55pct)', '成本')
replace_all('{{COST_OUTSOURCE_NOTE}}', '核心部件(电池/电机)外采，整车制造自研自产', '外包')
replace_all('{{TECH_GAP_ANALYSIS}}', '增程技术与理想同期领先，智驾技术(ADS 4.0)国内第一梯队', '技术')
replace_all('{{NET_MARGIN_WEAK}}', '净利率3.61%偏低(销售费用率14.7%过高)，ROE 23.53%优秀', '净利率')
replace_all('{{MARGIN_NOTE}}', '毛利率28.21%(+2.52pct)持续提升，主要受益于M9高毛利车型占比提高', '毛利率')
replace_all('{{CUSTOMER_PRICING_POWER}}', '华为渠道议价力强但对消费者定价权稳固，问界品牌溢价能力强', '议价')
replace_all('{{CUSTOMER_CONCENTRATION_RISK}}', '前5客户集中度11.89%较低，面向C端消费者分散', '集中')
replace_all('{{PRICE_WAR_RISK}}', '高端SUV市场竞争加剧(M7/M9竞品增多)，但品牌认知已形成', '价格战')
replace_all('{{DISRUPTION_NOTE}}', '智驾技术迭代快，若华为转向其他车企合作则核心壁垒削弱', '颠覆')
replace_all('{{BRAND_BARRIER_NOTE}}', '问界品牌已建立高端认知(均价~40万)，华为品牌背书不可复制', '品牌')
replace_all('{{BARRIER_NOTE}}', '核心壁垒在华为智选车独家合作+问界品牌高端认知+增程技术领先。壁垒最深的是华为生态绑定。', '壁垒')

# ===== M3 管理层 =====
replace_all('{{MGMT_NAME_1}}', '张正萍', '管理层1')
replace_all('{{MGMT_TITLE_1}}', '董事长/总裁', '职务1')
replace_all('{{MGMT_TENURE_1}}', '资深', '任期1')
replace_all('{{MGMT_DESC_1}}', '创始人张兴海之子，多年汽车行业经验，主导华为合作', '描述1')
replace_all('{{MGMT_NAME_2}}', '梁其军', '管理层2')
replace_all('{{MGMT_TITLE_2}}', '财务负责人', '职务2')
replace_all('{{MGMT_TENURE_2}}', '资深', '任期2')
replace_all('{{MGMT_DESC_2}}', '资深财务管理背景，负责公司财务战略和资本运作', '描述2')
replace_all('{{MGMT_EXPERIENCE}}', '张正萍带领团队成功转型新能源，与华为合作开创智选车模式。核心团队稳定，研发高管来自华为/行业巨头', '经验')
replace_all('{{MGMT_GOVERNANCE}}', '民企，张氏家族控股。董事会有华为背景独立董事，治理结构逐步完善。H股上市后治理更透明', '治理')
replace_all('{{MGMT_STYLE_ANALYSIS}}', '进取型管理风格，敢投入(研发80亿+)，敢合作(华为)，战略执行力强。快速从燃油车转型新能源', '风格')
replace_all('{{MGMT_SCORE_1}}', '8', 'M3分1')
replace_all('{{MGMT_SCORE_2}}', '8', 'M3分2')
replace_all('{{MGMT_SCORE_3}}', '6', 'M3分3')
replace_all('{{MGMT_SCORE_4}}', '7', 'M3分4')

mgmt_scores = [8, 8, 6, 7]
mgmt_colors = ['#4caf50', '#4caf50', '#f0c040', '#f0c040']
for i in range(1, 5):
    w = mgmt_scores[i-1] * 10
    replace_all(f'{{{{MGMT_BAR_{i}}}}}', f'width:{w}%;background:{mgmt_colors[i-1]}', f'M3条{i}')

# ===== M4 费用率 =====
fee_rows = [
    ('销售费用', '191.84亿', '241.94亿', '↗️+26.1%'),
    ('管理费用', '35.47亿', '47.87亿', '↗️+35.0%'),
    ('研发费用', '55.86亿', '79.54亿', '↗️+42.4%'),
    ('财务费用', '-2.95亿', '-4.20亿', '↘️利息收入增'),
]
for name, v24, v25, trend in fee_rows:
    # Try both with and without class="gold"
    pat1 = f'<td>{name}</td>\\n<td>__TODO__</td>\\n<td class="gold">__TODO__</td>\\n<td>__TODO__</td>'
    rep = f'<td>{name}</td>\\n<td>{v24}</td>\\n<td class="gold">{v25}</td>\\n<td>{trend}</td>'
    if name == '销售费用':
        # sales fee might have been filled by fill_auto
        pat2 = f'<td>销售费用</td>\\n<td>__TODO__</td>\\n<td>__TODO__</td>\\n<td>__TODO__</td>'
        rep2 = f'<td>销售费用</td>\\n<td>{v24}</td>\\n<td>{v25}</td>\\n<td>{trend}</td>'
        if pat2 in html:
            html = html.replace(pat2, rep2)
            changes += 1

for name, v24, v25, trend in fee_rows:
    pat = f'<td>{name}</td>\\n<td>__TODO__</td>\\n<td class="gold">__TODO__</td>\\n<td>__TODO__</td>'
    rep = f'<td>{name}</td>\\n<td>{v24}</td>\\n<td class="gold">{v25}</td>\\n<td>{trend}</td>'
    html = html.replace(pat, rep)

print("  ✅ 费用率")

# 销售费用特殊处理(可能有不同格式)
html = html.replace('<td>销售费用</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>',
    '<td>销售费用</td>\n<td>191.84亿</td>\n<td>241.94亿</td>\n<td>↗️+26.1%</td>')

# ===== M5 成本 =====
replace_all('{{COST_STRUCTURE_NOTE}}', '营业成本1169.54亿(+9.09%)占比营收70.9%。核心成本项：电池/电驱等BOM成本~55%、加工制造~15%、研发摊销~10%、销售渠道~15%。毛利率28.21%持续提升(+2.52pct)。', '成本')

# 成本表
cost_rows = [('BOM(电池/电驱)', '~600亿', '~643亿', '~55%', '↗️+7%', '电池成本下降但用量增'),
             ('加工制造', '~161亿', '~175亿', '~15%', '↗️+9%', '规模效应降本'),
             ('研发摊销', '~107亿', '~117亿', '~10%', '↗️+9%', '持续高研发投入'),
             ('销售渠道', '~144亿', '~175亿', '~15%', '↗️+22%', '广宣+服务费增'),
             ('其他成本', '~60亿', '~59亿', '~5%', '➡️持平', '管理/行政开支')]
for name, v24, v25, pct, trend, note in cost_rows:
    pat = f'<td>{name}</td>\\n<td>__TODO__</td>\\n<td class="gold">__TODO__</td>\\n<td>__TODO__</td>\\n<td>__TODO__</td>\\n<td>__TODO__</td>'
    rep = f'<td>{name}</td>\\n<td>{v24}</td>\\n<td class="gold">{v25}</td>\\n<td>{pct}</td>\\n<td>{trend}</td>\\n<td>{note}</td>'
    html = html.replace(pat, rep)

# 产业链
for i, (sc, ev) in enumerate([(9,'华为深度绑定，问界品牌依赖度极高'),(5,'电池/芯片供应集中度高'),
    (7,'高端SUV市场+问界品牌认知已形成'),(6,'新势力(蔚小理)+传统车企加速追赶'),
    (8,'新能源车制造门槛+智驾技术壁垒高')], 1):
    replace_all(f'{{{{CHAIN_SCORE_{i}}}}}', str(sc), f'链{i}')
    replace_all(f'{{{{CHAIN_EVIDENCE_{i}}}}}', ev, f'链证据{i}')

# ===== M6 FCF & 估值 =====
replace_all('{{FCF_ANALYSIS}}', '经营现金流58.63亿(2025)。CAPEX~42亿(产能扩建+研发)，FCF~17亿。FCF/净利润~30%，现金流质量一般。高研发投入(80亿/年)+资本开支压制FCF。', 'FCF')

# FCF表
for old, new in [
    ('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>FCF</td>',
     '<td>~30亿</td>\n<td>~42亿</td>\n<td>~40亿(正常化)</td>\n    </tr>\n<tr>\n<td>FCF</td>'),
    ('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>FCF/净利润</td>',
     '<td>~17亿</td>\n<td>~17亿</td>\n<td>~15-20亿</td>\n    </tr>\n<tr>\n<td>FCF/净利润</td>'),
    ('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n</table>',
     '<td>~45%</td>\n<td>~30%</td>\n<td>研发高投入压制</td>\n</table>'),
]:
    if old in html:
        html = html.replace(old, new)
        changes += 1

# PE对比
replace_all('{{PE_COMPARISON_TITLE}}', 'PE(TTM)对比 · 新能源车企', 'PE标题')
replace_all('{{PE_COMPARISON_BARS}}',
    '<div class="hb"><span class="hl">赛力斯</span><div class="ht"><div class="hf" style="width:22%;background:#4caf50;">PE 20x</div></div></div>\n'
    '<div class="hb"><span class="hl">比亚迪</span><div class="ht"><div class="hf" style="width:25%;background:#4caf50;">PE 22x</div></div></div>\n'
    '<div class="hb"><span class="hl">理想汽车</span><div class="ht"><div class="hf" style="width:40%;background:#f0c040;">PE 35x</div></div></div>\n'
    '<div class="hb"><span class="hl">小鹏汽车</span><div class="ht"><div class="hf" style="width:80%;background:#ff9800;">PE 70x(亏损)</div></div></div>',
    'PE对比')
replace_all('{{PE_ANALYSIS}}', 'PE 20x在新能源车企中偏低(行业30-50x)。PS 0.72x极低(行业1.5-3x)。PB 5.5x合理。市场对销售费用率和华为依赖度给予折价，但增长确定性高。', 'PE分析')

# 估值指标 — 命名占位符
replace_all('{{PE_TTM_RANGE}}', '15-35x(近一年)', 'PE区间')
replace_all('{{PE_TTM_EVAL}}', '偏低', 'PE评估')
replace_all('{{PE_26E_RANGE}}', '', 'PE26E')
replace_all('{{PE_26E_EVAL}}', '', 'PE26E')
replace_all('{{PB_RANGE}}', '3.5-8.0x', 'PB区间')
replace_all('{{PB_EVAL}}', '合理', 'PB评估')
replace_all('{{PS_TTM_RANGE}}', '0.5-2.0x', 'PS区间')
replace_all('{{PS_TTM_EVAL}}', '偏低', 'PS评估')

# ===== M7 =====
# 行业空间
replace_all('{{ENDGAME_THINKING}}', '中国新能源车渗透率~55%继续提升，高端SUV市场100万辆+持续扩容。问界M9在50万+细分市场已确立领先地位。行业终局：头部集中趋势明显，华为生态+自研技术是核心竞争力。', '终局')

# 竞争态势
replace_all('{{COMPETITOR_1}}', '理想汽车', '竞1')
replace_all('{{COMPETITOR_1_SEGMENT}}', '增程SUV', '竞1段')
replace_all('{{COMPETITOR_1_ANALYSIS}}', '增程赛道直接竞品，L系列月销4万+，产品力强但缺乏华为智驾赋能', '竞1分析')
replace_all('{{COMPETITOR_2}}', '比亚迪', '竞2')
replace_all('{{COMPETITOR_2_SEGMENT}}', '新能源全品类', '竞2段')
replace_all('{{COMPETITOR_2_ANALYSIS}}', '规模最大但高端品牌认知不如问界(仰望除外)，智驾能力落后', '竞2分析')
replace_all('{{COMPETITOR_3}}', '鸿蒙智行(华为其他合作方)', '竞3')
replace_all('{{COMPETITOR_3_SEGMENT}}', '华为生态内', '竞3段')
replace_all('{{COMPETITOR_3_ANALYSIS}}', '华为与奇瑞/江淮等合作，但问界是华为深度最深的产品', '竞3分析')
replace_all('{{COMPETITOR_4}}', '赛力斯核心优势：', '竞4')
replace_all('{{COMPETITOR_ADVANTAGE}}', '华为智选车独家深度合作+问界品牌高端认知+增程技术领先(效率41%+)', '优势')
replace_all('{{DIFF_STRATEGY}}', '差异化：华为全栈赋能(智驾/座舱/品牌/渠道)+增程效率领先+高端定位(均价40万+)', '差异')

# ===== M8 催化剂 =====
for old, new in [
    ('<td>2026-2027</td>\n<td>__TODO__</td>\n<td class="green">__TODO__</td>',
     '<td>2026Q4</td>\n<td>问界M8上市爬坡</td>\n<td class="green">新车型贡献增量，30-40万市场扩容</td>'),
    ('<td>2027</td>\n<td>__TODO__</td>\n<td class="green">__TODO__</td>',
     '<td>2027H1</td>\n<td>ADS 5.0发布</td>\n<td class="green">智驾技术迭代保持领先</td>'),
    ('<td>2027-2028</td>\n<td>__TODO__</td>\n<td class="green">__TODO__</td>',
     '<td>2027</td>\n<td>海外市场拓展</td>\n<td class="green">增程技术出海打开新市场</td>'),
    ('<td>2027-2028</td>\n<td>__TODO__</td>\n<td>—</td>',
     '<td>2028</td>\n<td>固态电池量产</td>\n<td>技术迭代提升产品力</td>'),
]:
    if old in html:
        html = html.replace(old, new)
        changes += 1

# 三年预测
old = '<tr>\n<td class="green">乐观</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td class="gold">基准</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td class="red">悲观</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>'
new = '<tr>\n<td class="green">乐观</td>\n<td>净利80亿</td>\n<td>净利110亿</td>\n<td>净利150亿</td>\n<td>毛利率回升至32%+</td>\n    </tr>\n<tr>\n<td class="gold">基准</td>\n<td>净利65亿</td>\n<td>净利85亿</td>\n<td>净利100亿</td>\n<td>毛利率维持28-29%</td>\n    </tr>\n<tr>\n<td class="red">悲观</td>\n<td>净利45亿</td>\n<td>净利55亿</td>\n<td>净利65亿</td>\n<td>毛利率降至25%</td>'
if old in html:
    html = html.replace(old, new)
    changes += 1

# ===== M9 预期差 =====
old = '<td style="color:#888;">__TODO__</td>\n<td style="color:#4caf50;">__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td style="color:#4caf50;">__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td style="color:#4caf50;">__TODO__</td>'
new = '<td style="color:#888;">华为合作不可持续</td>\n<td style="color:#4caf50;">华为智选车已形成深度绑定，华为需要赛力斯制造能力</td>\n<td>看好</td>\n    </tr>\n<tr>\n<td>销售费用率</td>\n<td style="color:#888;">14.7%过高侵蚀利润</td>\n<td style="color:#888;">规模效应下费用率将逐步下降，问界品牌认知度提升后广宣费趋稳</td>\n<td>中性</td>\n    </tr>\n<tr>\n<td>行业竞争</td>\n<td style="color:#888;">高端SUV竞争加剧</td>\n<td style="color:#888;">竞争加剧是事实但问界品牌认知已领先，先发优势明显</td>\n<td>中性</td>\n    </tr>\n<tr>\n<td>估值偏低</td>\n<td style="color:#888;">PE 20x合理</td>\n<td style="color:#4caf50;">PS 0.72x行业最低，市场过度担忧华为依赖度</td>\n<td>看好</td>\n    </tr>\n<tr>\n<td>海外市场</td>\n<td style="color:#888;">出海前景不明</td>\n<td style="color:#4caf50;">增程技术差异化，东南亚/中东有潜力</td>'
if old in html:
    html = html.replace(old, new)
    changes += 1

# ===== M10 风险 =====
# 三情景
replace_all('{{OPTIMISTIC_PRICE}}', '~120元', '乐观价')
replace_all('{{OPTIMISTIC_RETURN}}', '+85%', '乐观回报')
replace_all('{{OPTIMISTIC_SCENARIO}}', 'M8+M9持续放量+海外突破，净利80亿+，PE维持20-25x', '乐观情景')
replace_all('{{NEUTRAL_PRICE}}', '72元', '中性价')
replace_all('{{NEUTRAL_RETURN}}', '~+11%', '中性回报')
replace_all('{{NEUTRAL_SCENARIO}}', '问界稳健增长+毛利率维持28%+，净利60-65亿，PE 18-22x', '中性情景')
replace_all('{{PESS_PRICE}}', '~45元', '悲观价')
replace_all('{{PESS_RETURN}}', '-31%', '悲观回报')
replace_all('{{PESS_SCENARIO}}', '华为合作生变+行业价格战加剧，净利<45亿，PE>30x', '悲观情景')

# 避雷清单
replace_all('{{CHECK_1_RESULT}}', '商誉~8亿(占总资产~1%)风险可控', '避雷1')
replace_all('{{CHECK_2_RESULT}}', '张氏家族控股，管理层持股稳定，无大额减持', '避雷2')
replace_all('{{CHECK_3_RESULT}}', '经营现金流58.63亿为正，审计标准无保留意见', '避雷3')
replace_all('{{CHECK_4_RESULT}}', '经营现金流58.63亿(2025)持续为正', '避雷4')
replace_all('{{CHECK_5_RESULT}}', '年报未披露重大未决诉讼', '避雷5')

# 敏感性分析
for old, new in [
    ('{{SENS_REV_IMPACT}}', '-165亿'),
    ('{{SENS_REV_PRICE}}', '-15%'),
    ('{{SENS_MARGIN_IMPACT}}', '-49.5亿'),
    ('{{SENS_MARGIN_PRICE}}', '-12%'),
    ('{{SENS_COST_IMPACT}}', '-20亿'),
    ('{{SENS_COST_PRICE}}', '-8%'),
    ('{{SENS_CYCLE_IMPACT}}', '-60亿'),
    ('{{SENS_CYCLE_PRICE}}', '-25%'),
    ('{{SENS_COMPETE_IMPACT}}', '-30亿'),
    ('{{SENS_COMPETE_PRICE}}', '-15%'),
]:
    replace_all(old, new, '敏感')

# 清算价值
items = [('货币资金','280亿','~280亿'),('应收账款','120亿','~96亿'),
         ('存货','150亿','~105亿'),('固定资产','180亿','~126亿')]
for i, (name, book, val) in enumerate(items, 1):
    replace_all(f'{{{{LIQ_ASSET_{i}}}}}', name, f'清{i}')
    replace_all(f'{{{{LIQ_BOOK_{i}}}}}', book, f'清{i}b')
    replace_all(f'{{{{LIQ_VAL_{i}}}}}', val, f'清{i}v')
replace_all('{{LIQ_TOTAL_BOOK}}', '730亿', '清合b')
replace_all('{{LIQ_TOTAL_VAL}}', '~607亿', '清合v')
replace_all('{{LIQUIDATION_NOTE}}', '清算价值约607亿(账面730亿)，折合每股约37.5元(总股本16.19亿)。核心资产为货币资金(280亿)和存货/固定资产(330亿)。制造资产变现性一般但持续经营价值远高于清算。', '清算说明')

replace_all('{{FINANCIAL_CONTROLLABLE}}', '财务风险可控。货币资金280亿充裕，有息负债率~25%。经营现金流58.63亿持续为正，但高资本开支(42亿)和高研发(80亿)压制FCF。', '财务')
replace_all('{{CORE_RISK_FOCUS}}', '销售费用率14.7%过高、华为合作依赖度、高端市场竞争加剧、研发投入大回报周期长', '风险')
replace_all('{{DEBT_RATIO_NOTE}}', '负债率~55%合理，货币资金280亿覆盖短期债务绰绰有余。H股上市后财务更健康', '负债')
replace_all('{{CORE_ADVANTAGE_LABEL}}', '华为智选车独家合作伙伴', '优势标签')
replace_all('{{RISK_TITLE_1}}', '华为依赖', '风险1')
replace_all('{{RISK_ITEM_1}}', '核心技术和品牌依赖华为，合作关系变化将重创业务', '风险项1')
replace_all('{{RISK_2_TITLE}}', '费用率过高', '风险2')
replace_all('{{RISK_2_DESC}}', '销售费用率14.7%在行业中偏高，压制利润率', '风险项2')
replace_all('{{RISK_TITLE_3}}', '竞争加剧', '风险3')
replace_all('{{RISK_ITEM_3}}', '高端SUV市场竞品增多(M8/M9细分市场)，价格战风险', '风险项3')

# 亮点
replace_all('{{HIGHLIGHT_1_TITLE}}', '华为生态深度绑定', '亮点1')
replace_all('{{HIGHLIGHT_1_DESC}}', '华为智选车独家合作伙伴，智驾(ADS 4.0)/鸿蒙座舱/品牌渠道全栈赋能。问界品牌已形成高端认知。', '亮点1d')
replace_all('{{HIGHLIGHT_2_TITLE}}', '业绩高速增长', '亮点2')
replace_all('{{HIGHLIGHT_2_DESC}}', '营收1650亿(+13.7%)净利60亿(+58.3%)，ROE 23.53%。毛利率28.21%持续提升+M9高毛利车型占比提高。', '亮点2d')
replace_all('{{HIGHLIGHT_3_TITLE}}', '估值安全边际', '亮点3')
replace_all('{{HIGHLIGHT_3_DESC}}', 'PE 20x/PB 5.5x/PS 0.72x均在新能源车企中偏低。市场对销售费用率和华为依赖度的担忧已被定价。', '亮点3d')

# 六维评分
dim_scores = [8, 7, 7, 5, 7, 8]
for i in range(1, 7):
    w = dim_scores[i-1] * 10
    replace_all(f'{{{{DIM_BAR_{i}}}}}', f'width:{w}%', f'维{i}')
    replace_all(f'{{{{DIM_SCORE_{i}}}}}', str(dim_scores[i-1]), f'维{i}分')

# 价值理念
texts = ['赛力斯是"好生意"——华为品牌+问界高端定位+增程技术，ROE 23.53%优秀。销售费用率14.7%是主要拖累。',
    '华为智选车模式差异化极强，问界已建立高端品牌认知。增程效率41%+行业领先，ADS 4.0国内第一梯队。',
    '管理层进取型，成功从燃油车转型新能源，张正萍带领团队与华为深度合作。执行力强但分红率低。',
    'PE 20x/PB 5.5x/PS 0.72x偏低。市场对华为依赖和费用率的担忧已充分定价，安全边际充足。',
    '成本管控有改善空间(毛利率+2.52pct)，但销售费用率14.7%偏高。规模效应显现后费用率将下降。',
    '逆向估值：市场过度关注华为依赖风险，低估了智选车模式的先发优势和问界品牌价值。PS 0.72x是行业最低。',
    '成长空间：新能源渗透率55%→80%，高端SUV市场持续扩容。海外市场(东南亚/中东)增程技术差异化。',
    '催化剂：问界M8爬坡+ADS 5.0发布+海外市场拓展。多项利好叠加，中期确定性较强。',
    '预期差：市场认为华为合作不可持续，但实际深度绑定已形成。销售费用率将随规模效应下降。',
    '反脆弱性一般：过度依赖华为是最大风险。但现金流充裕+营收高增长提供了缓冲。',
    'PB 5.5x合理，PS 0.72x历史低位。最差情景(华为解绑)对应PS~0.4x，下行空间有限。']
for i, t in enumerate(texts, 1):
    key = f'{{M{i}_ANALYSIS}}' if i < 11 else '{{M11_SAFETY_MARGIN}}'
    replace_all(key, t, f'M{i}')

# ===== BQ =====
bq_texts = [
    '赛力斯整体评分7.0/10。核心价值在华为智选车独家合作+问界品牌高端认知。2025年营收1650亿(+13.7%)净利60亿(+58.3%)，ROE 23.53%优秀。PE 20x/PB 5.5x/PS 0.72x偏低。核心亮点：华为生态+增程技术领先+估值安全边际。核心风险：销售费用率14.7%偏高、华为依赖度大。',
    '赛力斯主营问界品牌新能源汽车(97%营收)，华为研发+品牌+渠道全栈赋能。M9/M7/M5产品矩阵覆盖30-60万区间。经销占比93%，直销7%。增程技术效率41%+行业领先。高研发投入(80亿/年)保障技术领先。',
    '核心护城河在华为智选车独家合作模式+问界品牌高端认知+增程技术领先，三重壁垒叠加。壁垒评分7.5/10。最深的壁垒是华为生态绑定，竞品（包括华为其他合作方）无法复制问界的深度和品牌认知。',
    '张正萍带领团队成功转型新能源，与华为合作开创智选车模式。研发高管来自华为/行业巨头，团队稳定。评分：战略8/10，执行力8/10，股东回报6/10，资本配置7/10。H股上市后治理更透明。',
    '财务评分5/10。营收1650.54亿(+13.7%)净利59.57亿(+58.3%)高增长。毛利率28.21%(+2.52pct)提升。ROE 23.53%优秀。经营现金流58.63亿为正。费用率：销售241.94亿(+26.1%)，管理47.87亿(+35.0%)，研发79.54亿(+42.4%)，财务-4.20亿(利息收入)。',
    '成本结构：BOM(电池/电驱)~55%，加工制造~15%，研发摊销~10%，销售渠道~15%。电池成本占比高但持续下降。毛利率28.21%持续提升(+2.52pct)，M9高毛利车型贡献大。规模效应将逐步改善成本结构。',
    '估值判断：PE(TTM) 20x偏低(行业30-50x)。归母PE 20x，扣非PE 20x(非常损益小)，PB 5.5x合理(历史3.5-8.0x)，PS 0.72x偏低(行业1.5-3x)。三个口径：PE和PS指向偏低，PB合理。综合判断：估值偏低，市场对费用率和华为依赖的担忧已被定价。',
    '中国新能源车渗透率~55%持续提升，高端SUV市场100万辆+。问界M9在50万+细分市场领先。行业终局向头部集中，华为生态+自研技术是核心竞争力。增程技术出海(东南亚/中东)打开第二曲线。',
    '三大催化剂：①问界M8爬坡贡献增量(30-40万市场)；②ADS 5.0发布保持智驾领先；③海外市场拓展(增程技术出海)。三情景预测：45-120元，基准72元。核心催化剂看M8爬坡节奏和毛利率变化。',
    '市场可能低估：①华为合作已形成深度绑定(赛力斯制造能力不可替代)；②PS 0.72x行业最低反映过度悲观；③问界品牌价值被低估。费用率过高和行业竞争是市场关注焦点。固态电池等新技术的远期价值未被充分定价。',
    '核心风险：①华为依赖度过高，合作关系变化将重创业务；②销售费用率14.7%过高压制利润率；③高端SUV竞争加剧价格战风险；④研发投入80亿/年回报周期长。避雷清单全部通过。资产负债表健康：货币资金280亿。',
]
parts = html.split('{{BQ_ANALYSIS}}')
if len(parts) == len(bq_texts) + 1:
    html = parts[0]
    for i, txt in enumerate(bq_texts):
        html += txt + parts[i+1]
    changes += len(bq_texts)
    print(f"  ✅ BQ({len(bq_texts)}篇)")

# ===== 写回 =====
with open(REPORT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n{'='*50}")
print(f"  填充完成！共修改 {changes} 处")
print(f"{'='*50}")

# ===== 自检 =====
print("\n📋 自检结果:")
errors = []
with open(REPORT, 'r', encoding='utf-8') as f:
    c = f.read()

# TODO
t = c.count('__TODO__')
if t > 0: errors.append(f"❌ TODO残留: {t}个")
# 占位符
ph = len(re.findall(r'\{\{[^}]+\}', c))
if ph > 0: errors.append(f"❌ 占位符残留: {ph}个")
# div
op, cl = c.count('<div'), c.count('</div>')
if op != cl: errors.append(f"❌ div不平衡: {op}开/{cl}闭")
# 估值表
for marker in ['PE_TTM_RANGE', 'PB_RANGE', 'PS_TTM_RANGE']:
    if marker in c:
        errors.append(f"❌ 估值表占位符残留: {marker}")
        break
# 敏感表
for s in ['SENS_REV_IMPACT', 'SENS_MARGIN_IMPACT']:
    if s in c:
        errors.append(f"❌ 敏感表占位符残留: {s}")
        break
# 条形花括号
if re.search(r'style="\{', c):
    errors.append("❌ 条形花括号残留")

if errors:
    print("\n".join(errors))
    print("⚠️ 修复后再交付！")
else:
    print("✅ TODO: 0 | {{}}: 0 | div平衡 | 估值OK | 敏感OK | 条形OK")
    print(f"  文件大小: {len(c)} 字节")
print(f"{'='*50}")
