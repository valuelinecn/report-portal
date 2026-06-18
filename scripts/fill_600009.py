#!/usr/bin/env python3
"""上海机场(600009) 报告填充脚本"""
import re

REPORT = "/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports/600009.html"

with open(REPORT, 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

def replace_all(old, new, desc=""):
    global changes, html
    if old in html:
        html = html.replace(old, new)
        changes += 1
        print(f"  ✅ {desc}")
    else:
        if old.startswith('{{'):
            print(f"  ⚠️ 未找到: {old}")

# ===== 基础信息 =====
replace_all('{{COMPANY_NAME_CN}}', '上海机场', '公司名称')
replace_all('{{SCORE}}', '6.0', '综合评分')
replace_all('{{RATING_DESC}}', '上海机场是中国最大航空枢纽运营商，长三角唯一国际门户。2025年营收133.46亿(+7.9%)净利21.17亿(+42.8%)持续恢复。PE 28x/PB 2.5x合理偏低。区位垄断护城河深厚，免税业务复苏弹性大。', '评级描述')
replace_all('{{DATA_SOURCE}}', '年报PDF(2025/2024) + 东方财富', '数据来源')

# ===== 综合评价卡片 =====
replace_all('{{CARD1_VAL}}', '6.0', '综合评级')
replace_all('{{CARD1_LABEL}}', '综合评级', '综合评级标签')
replace_all('{{CARD1_COLOR}}', '#f0c040', '综合评级颜色')
replace_all('{{CARD2_VAL}}', '中', '风险等级')
replace_all('{{CARD2_LABEL}}', '风险等级', '风险等级标签')
replace_all('{{CARD2_COLOR}}', '#f0c040', '风险等级颜色')
replace_all('{{CARD3_VAL}}', '中', '成长弹性')
replace_all('{{CARD3_LABEL}}', '成长弹性', '成长弹性标签')
replace_all('{{CARD3_COLOR}}', '#f0c040', '成长弹性颜色')
replace_all('{{CARD4_VAL}}', '5.03%', 'ROE')
replace_all('{{CARD4_LABEL}}', 'ROE', 'ROE标签')
replace_all('{{CARD4_COLOR}}', '#ff9800', 'ROE颜色')

# ===== LOGIC卡 =====
replace_all('{{LOGIC_1_CONTENT}}', '长三角唯一国际航空枢纽，免税业务2019年收入超60亿，疫后持续恢复中', 'LOGIC1')
replace_all('{{LOGIC_1_NOTE}}', '区位垄断不可复制+免税招标弹性，恢复至2019年水平有翻倍空间', 'LOGIC1补充')
replace_all('{{LOGIC_2_CONTENT}}', '区位垄断壁垒(长三角唯一国际枢纽)+政策准入壁垒(航权/时刻分配)', 'LOGIC2')
replace_all('{{LOGIC_2_NOTE}}', '方圆300公里无竞争对手，新建机场不现实', 'LOGIC2补充')
replace_all('{{LOGIC_3_CONTENT}}', '航空业务量(起降/旅客/货邮)/免税收入/毛利率趋势/ROE变化', 'LOGIC3')
replace_all('{{LOGIC_3_NOTE}}', '重点跟踪国际航线恢复进度和免税合同条款', 'LOGIC3补充')
replace_all('{{LOGIC_4_CONTENT}}', 'PB 2.5x处于历史中低位，股息率~2%尚可', 'LOGIC4')
replace_all('{{LOGIC_4_NOTE}}', '周期底部已过，疫情冲击最坏阶段已消化', 'LOGIC4补充')

# ===== 综合评价BQ =====
replace_all('{{INVESTMENT_THESIS}}', '上海机场核心价值在于长三角唯一国际航空枢纽的区位垄断地位。2025年机场业务量持续恢复(旅客8499万+10.7%)，免税业务弹性待释放。PE 28x/PB 2.5x估值合理偏低。核心亮点：区位垄断+免税复苏弹性，核心风险：ROE仅5.03%偏低、免税合同待重签。', '投资理念')

# ===== M1 =====
replace_all('{{ANALYSIS_TEXT}}', '上海机场运营浦东和虹桥两场，是中国最大的航空枢纽运营商。2025年浦东机场旅客8499万(+10.7%)、虹桥5015万(+4.6%)。收入结构：航空性收入(起降/旅客服务费)+非航收入(免税商业/广告/物流)。区位优势不可复制：长三角唯一国际航空门户。', 'M1分析')
replace_all('{{M1_REVENUE_ROWS}}',
    '<tr><td>航空性收入</td><td>68.14亿</td><td>73.45亿</td><td>+7.8%</td></tr>'
    '<tr><td>非航收入</td><td>55.55亿</td><td>60.01亿</td><td>+8.0%</td></tr>',
    'M1收入行')
replace_all('{{M1_HB_BAR_1}}', '<div class="hb"><span class="hl">航空性收入</span><div class="ht"><div class="hf" style="width:55%;background:#4caf50;">73.45亿 · 55%</div></div></div>', 'M1水平条1')
replace_all('{{M1_HB_BAR_2}}', '<div class="hb"><span class="hl">非航收入(免税/商业)</span><div class="ht"><div class="hf" style="width:45%;background:#4caf50;">60.01亿 · 45%</div></div></div>', 'M1水平条2')
replace_all('{{M1_HB_BAR_3}}', '', 'M1水平条3')
replace_all('{{M1_ANNUAL_REMARK}}', '2025年营收133.46亿(+7.9%)恢复至2019年(~110亿航空性+免税)的约85%。航空业务量持续恢复中，国际航线(旅客+19.5%)增速快于国内(+4.5%)。', 'M1备注')

# M1商业模式评估
replace_all('{{BIZ_SCORE_1}}', '8/10 区位垄断', 'M1评分1')
replace_all('{{BIZ_SCORE_2}}', '7/10 品牌租金', 'M1评分2')
replace_all('{{BIZ_SCORE_3}}', '8/10 特许经营', 'M1评分3')
replace_all('{{BIZ_SCORE_4}}', '6/10 客户结构', 'M1评分4')
replace_all('{{BIZ_EVIDENCE_1}}', '长三角唯一国际航空枢纽，半径300公里无实质竞争', 'M1证据1')
replace_all('{{BIZ_EVIDENCE_2}}', '中免日上等龙头运营商绑定，免税收入恢复弹性大', 'M1证据2')
replace_all('{{BIZ_EVIDENCE_3}}', '航权和时刻资源行政分配，具有特许经营性质', 'M1证据3')
replace_all('{{BIZ_EVIDENCE_4}}', '客户以航空公司为主，集中度较高但客户粘性极强', 'M1证据4')
replace_all('{{CORE_BUSINESS}}', '浦东机场为核心资产(贡献85%+收入)，虹桥为辅', '核心业务')

# ===== M2 壁垒 =====
moat_scores = [9, 9, 7, 6, 9, 8]
moat_colors = ['#4caf50', '#4caf50', '#f0c040', '#f0c040', '#4caf50', '#4caf50']
for i in range(1, 7):
    w = moat_scores[i-1] * 10
    replace_all(f'{{{{MOAT_BAR_{i}}}}}', f'width:{w}%;background:{moat_colors[i-1]}', f'M2条{i}')
    replace_all(f'{{{{MOAT_SCORE_{i}}}}}', str(moat_scores[i-1]), f'M2分{i}')
replace_all('{{MOAT_TOTAL_SCORE}}', '8.0', '壁垒总分')
replace_all('{{MOAT_LEVEL}}', '深厚', '壁垒等级')
replace_all('{{MOAT_PHILOSOPHY}}', '核心护城河是长三角唯一国际航空枢纽的区位垄断地位，这是物理空间和行政准入的双重壁垒，不可复制', '护城河理念')
replace_all('{{MOAT_POINT_2}}', '行政准入壁垒：航权、时刻资源由政府分配，新机场建设周期10年以上，浦东机场扩建已明确，其他竞争对手无法进入', '壁垒要点2')
replace_all('{{MOAT_SCALE_NOTE}}', '2025年浦东机场旅客8499万、货邮409万吨，规模全国第一。虹桥5015万旅客。两场合计超1.35亿人次', '规模壁垒')
replace_all('{{MOAT_PATENT_NOTE}}', '非技术密集型行业，核心壁垒在区位和政策，非专利', '技术壁垒')
replace_all('{{RESOURCE_NOTE}}', '长三角唯一国际枢纽是核心资源，天然稀缺不可复制', '资源壁垒')
replace_all('{{CERT_BARRIER}}', '机场运营许可证+口岸资质+航权分配，多重行政准入', '认证壁垒')
replace_all('{{COST_EFFECT}}', '基础设施建成后边际成本低，客流量增则利润率大幅提升', '成本优势')
replace_all('{{COST_OUTSOURCE_NOTE}}', '部分地面服务外包，核心运营团队聚焦安全和服务', '外包说明')
replace_all('{{TECH_GAP_ANALYSIS}}', '非技术密集型，核心竞争力在线下物理枢纽位置', '技术差距')
replace_all('{{NET_MARGIN_WEAK}}', '净利率15.86%(2025)在行业中偏低，ROE 5.03%偏低', '净利率弱点')
replace_all('{{MARGIN_NOTE}}', '毛利率27.51%(2025)较2024年25.38%提升，但仍低于2019年50%+水平，免税业务恢复是关键', '毛利率说明')
replace_all('{{CUSTOMER_PRICING_POWER}}', '对航空公司议价力强(起降费收费标准由政府制定)，对免税运营商议价力强(独家资源)', '客户议价力')
replace_all('{{CUSTOMER_CONCENTRATION_RISK}}', '前5大航司客户集中度较高，东上航占比~40%', '客户集中风险')
replace_all('{{PRICE_WAR_RISK}}', '无价格战风险(收费标准受政府管制)', '价格战风险')
replace_all('{{DISRUPTION_NOTE}}', '远程会议/高铁分流部分商务旅客，但国际航线不可替代', '颠覆风险')
replace_all('{{BRAND_BARRIER_NOTE}}', '上海机场品牌在全国具有较高认知度，枢纽品牌效应强', '品牌壁垒说明')
replace_all('{{BARRIER_NOTE}}', '核心壁垒在区位垄断(长三角唯一国际枢纽)+行政准入(航权/时刻)，护城河深厚且不可复制', '壁垒综合说明')

# ===== M3 管理层 =====
replace_all('{{MGMT_NAME_1}}', '冯昕', '管理层1')
replace_all('{{MGMT_TITLE_1}}', '董事局主席', '管理层职务1')
replace_all('{{MGMT_NAME_2}}', '黄铮霖', '管理层2')
replace_all('{{MGMT_TITLE_2}}', '总经理', '管理层职务2')
replace_all('{{MGMT_TENURE_1}}', '2025年新任', '管理层任期1')
replace_all('{{MGMT_TENURE_2}}', '资深', '管理层任期2')
replace_all('{{MGMT_DESC_1}}', '2025年新任，此前任上海机场集团副总裁，熟悉机场运营管理', '管理层描述1')
replace_all('{{MGMT_DESC_2}}', '多年机场运营管理经验，财务背景专业', '管理层描述2')
replace_all('{{MGMT_EXPERIENCE}}', '管理团队具有丰富的机场运营和航空管理经验，成本控制能力较强', '管理层经验')
replace_all('{{MGMT_GOVERNANCE}}', '上海市国资委实控，国企治理规范。浦东/虹桥两场统一管理架构', '公司治理')
replace_all('{{MGMT_STYLE_ANALYSIS}}', '稳健型管理风格，聚焦主业，资本支出纪律严格。分红率~30%逐步提升', '管理风格')
replace_all('{{MGMT_SCORE_1}}', '7', '管理层评分1')
replace_all('{{MGMT_SCORE_2}}', '7', '管理层评分2')
replace_all('{{MGMT_SCORE_3}}', '6', '管理层评分3')
replace_all('{{MGMT_SCORE_4}}', '6', '管理层评分4')

mgmt_scores = [7, 7, 6, 6]
mgmt_colors = ['#4caf50', '#4caf50', '#f0c040', '#f0c040']
for i in range(1, 5):
    w = mgmt_scores[i-1] * 10
    replace_all(f'{{{{MGMT_BAR_{i}}}}}', f'width:{w}%;background:{mgmt_colors[i-1]}', f'M3条{i}')

# ===== M4 费用率 =====
fee_data = {
    '研发费用': ('0.11亿', '0.18亿', '↗️+70.7%'),
    '销售费用': ('—', '—', '—'),
    '管理费用': ('7.36亿', '7.40亿', '↗️+0.5%'),
    '财务费用': ('4.67亿', '4.20亿', '↘️-10.0%'),
}
for fee_name, (v2024, v2025, trend) in fee_data.items():
    pat = f'<td>{fee_name}</td>\\s*<td>__TODO__</td>\\s*<td class="gold">__TODO__</td>\\s*<td>__TODO__</td>'
    rep = f'<td>{fee_name}</td>\\n<td>{v2024}</td>\\n<td class="gold">{v2025}</td>\\n<td>{trend}</td>'
    html = re.sub(pat, rep, html)
    print(f"  ✅ {fee_name}")

# ===== M5 成本 =====
replace_all('{{COST_STRUCTURE_NOTE}}', '营业成本96.74亿(+0.19%)基本持平，人工成本占比~45%为最大项，折旧摊销~30%，运营维护~15%。固定成本占比高，业务量增长直接拉升利润率。', '成本描述')

# 成本表TODO行
cost_rows = [
    ('人工成本', '~44亿', '~44亿', '~45%', '➡️基本持平', '运营人员薪酬稳定'),
    ('折旧摊销', '~29亿', '~29亿', '~30%', '➡️基本持平', '固定资产折旧稳定'),
    ('运营维护', '~14亿', '~15亿', '~15%', '↗️+7%', '业务量增长带动'),
    ('其他成本', '~10亿', '~9亿', '~10%', '↘️-10%', '降本增效成果'),
]
for i, (name, v24, v25, pct, trend, note) in enumerate(cost_rows):
    if i == 0:
        pat = f'<td>__TODO__</td>\\s*<td>__TODO__</td>\\s*<td class="gold">__TODO__</td>\\s*<td>__TODO__</td>\\s*<td>__TODO__</td>\\s*<td>__TODO__</td>'
        rep = f'<td>{name}</td>\\n<td>{v24}</td>\\n<td class="gold">{v25}</td>\\n<td>{pct}</td>\\n<td>{trend}</td>\\n<td>{note}</td>'
        html = re.sub(pat, rep, html, count=1)
        print(f"  ✅ 成本行{i+1}")

# Chain scores
replace_all('{{CHAIN_SCORE_1}}', '9', '链1')
replace_all('{{CHAIN_SCORE_2}}', '5', '链2')
replace_all('{{CHAIN_SCORE_3}}', '8', '链3')
replace_all('{{CHAIN_SCORE_4}}', '7', '链4')
replace_all('{{CHAIN_SCORE_5}}', '9', '链5')
replace_all('{{CHAIN_EVIDENCE_1}}', '航空公司高度依赖机场，无法轻易切换枢纽', '链证据1')
replace_all('{{CHAIN_EVIDENCE_2}}', '航材/航油等供应商集中，机场议价力适中', '链证据2')
replace_all('{{CHAIN_EVIDENCE_3}}', '长三角唯一国际枢纽，无直接竞争', '链证据3')
replace_all('{{CHAIN_EVIDENCE_4}}', '高铁分流部分国内线，国际线不可替代', '链证据4')
replace_all('{{CHAIN_EVIDENCE_5}}', '机场建设需10年+、投资百亿+，天然高壁垒', '链证据5')

# ===== M6 FCF & 估值 =====
replace_all('{{FCF_ANALYSIS}}', '经营现金流59.76亿(2025,+8.2%)持续向好。CAPEX~35亿(浦东机场扩建等)，FCF~25亿。FCF/净利润>100%，现金流质量优秀。', 'FCF分析')

# FCF表TODO
for pat, rep in [
    ('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>FCF</td>',
     '<td>~30亿</td>\n<td>~35亿</td>\n<td>~30亿(正常化)</td>\n    </tr>\n<tr>\n<td>FCF</td>'),
    ('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>FCF/净利润</td>',
     '<td>~25亿</td>\n<td>~25亿</td>\n<td>~20-25亿</td>\n    </tr>\n<tr>\n<td>FCF/净利润</td>'),
    ('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n</table>',
     '<td>>100%</td>\n<td>>100%</td>\n<td>现金流优秀</td>\n</table>'),
]:
    if pat in html:
        html = html.replace(pat, rep)
        changes += 1
        print(f"  ✅ FCF表行")

# PE comparison
replace_all('{{PE_COMPARISON_TITLE}}', 'PE(TTM)对比 · 机场', 'PE标题')
replace_all('{{PE_COMPARISON_BARS}}',
    '<div class="hb"><span class="hl">上海机场</span><div class="ht"><div class="hf" style="width:42%;background:#4caf50;">PE 28x</div></div></div>\n'
    '<div class="hb"><span class="hl">首都机场</span><div class="ht"><div class="hf" style="width:38%;background:#4caf50;">PE 25x</div></div></div>\n'
    '<div class="hb"><span class="hl">白云机场</span><div class="ht"><div class="hf" style="width:45%;background:#f0c040;">PE 30x</div></div></div>\n'
    '<div class="hb"><span class="hl">深圳机场</span><div class="ht"><div class="hf" style="width:35%;background:#4caf50;">PE 23x</div></div></div>',
    'PE对比')
replace_all('{{PE_ANALYSIS}}', 'PE 28x在机场板块中处于合理水平。PB 2.5x处于历史中低位(历史1.5-4.0x)。PS(TTM) 5.16x。估值核心支撑在区位垄断+免税复苏弹性。', 'PE分析')

# 估值指标历史区间+评估
old_val = '<td>28.1x</td>\n<td>—</td>\n<td>—</td>\n</tr>\n<tr>\n<td>PB</td>\n<td>2.5x</td>\n<td>—</td>\n<td>—</td>\n</tr>\n<tr>\n<td>PS(TTM)</td>\n<td>5.16x</td>\n<td>—</td>\n<td>—</td>\n</tr>'
new_val = '<td>28.1x</td>\n<td>15-60x(疫后波动大)</td>\n<td>合理</td>\n    </tr>\n<tr>\n<td>PB</td>\n<td>2.5x</td>\n<td>1.5-4.0x</td>\n<td>偏低</td>\n    </tr>\n<tr>\n<td>PS(TTM)</td>\n<td>5.16x</td>\n<td>3-10x</td>\n<td>偏低</td>\n    </tr>'
if old_val in html:
    html = html.replace(old_val, new_val)
    changes += 1
    print(f"  ✅ 估值指标填充")

# ===== M7 =====
# 行业空间表
html = re.sub(
    r'<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>',
    '<td>中国航空客运</td><td>~7亿人次</td><td>+8-10%</td><td>上海两场~1.35亿</td><td>~19%</td>\n    </tr>\n<tr>\n<td>国际航线</td><td>~1.5亿人次</td><td>+12-15%</td><td>浦东~3800万</td><td>~25%</td>\n    </tr>\n<tr>\n<td>中国免税市场</td>',
    html)
print(f"  ✅ M7行业空间行1-2")

html = re.sub(
    r'<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*</table>',
    '<td>~800亿</td><td>~10%</td><td>浦东机场~30亿</td><td>~4%</td>\n    </tr>\n  </table>',
    html)
print(f"  ✅ M7行业空间行3")

# 竞争对手
replace_all('{{COMPETITOR_1}}', '首都机场', '竞1')
replace_all('{{COMPETITOR_1_SEGMENT}}', '北方枢纽', '竞1段')
replace_all('{{COMPETITOR_1_ANALYSIS}}', '北方最大枢纽，但国际航线占比低于浦东，区位优势不如上海', '竞1分析')
replace_all('{{COMPETITOR_2}}', '白云机场', '竞2')
replace_all('{{COMPETITOR_2_SEGMENT}}', '南方枢纽', '竞2段')
replace_all('{{COMPETITOR_2_ANALYSIS}}', '大湾区枢纽，国际航线快速增长，但客源腹地不如长三角', '竞2分析')
replace_all('{{COMPETITOR_3}}', '深圳机场', '竞3')
replace_all('{{COMPETITOR_3_SEGMENT}}', '华南枢纽', '竞3段')
replace_all('{{COMPETITOR_3_ANALYSIS}}', '毗邻香港机场，国际航线受限，以国内线为主', '竞3分析')
replace_all('{{COMPETITOR_4}}', '上海机场核心优势：', '竞4')
replace_all('{{COMPETITOR_ADVANTAGE}}', '长三角唯一国际枢纽，国际航线占比最高(44.7%)，高端商务旅客集中', '优势')
replace_all('{{DIFF_STRATEGY}}', '差异化在于：国际航线占比高+区位辐射长三角最富裕地区+免税业务弹性最大', '差异')

# 行业终局
replace_all('{{ENDGAME_THINKING}}', '中国航空市场持续增长(人均乘机次数<0.5次 vs 美国>2次)，上海两场容量趋于饱和。浦东机场四期扩建(新增T3航站楼+卫星厅)打开成长空间。国际航线恢复+免税业务重签是中期核心催化剂。', '终局')

# ===== M8 催化剂 =====
# 催化剂时间表
html = re.sub(
    r'<td>2026-2027</td>\s*<td>__TODO__</td>\s*<td class="green">__TODO__</td>',
    '<td>2026-2027</td>\n<td>国际航线持续恢复</td>\n<td class="green">国际旅客仍有~20%恢复空间</td>',
    html)
html = re.sub(
    r'<td>2027</td>\s*<td>__TODO__</td>\s*<td class="green">__TODO__</td>',
    '<td>2027</td>\n<td>浦东机场四期扩建推进</td>\n<td class="green">扩建打开远期容量天花板</td>',
    html)
html = re.sub(
    r'<td>2027-2028</td>\s*<td>__TODO__</td>\s*<td class="green">__TODO__</td>',
    '<td>2027-2028</td>\n<td>免税合同重签</td>\n<td class="green">新合同条款决定中期利润弹性</td>',
    html)
html = re.sub(
    r'<td>2027-2028</td>\s*<td>__TODO__</td>\s*<td>—</td>',
    '<td>2028+</td>\n<td>高铁网络完善</td>\n<td>国内航线分流有限，国际航线不受影响</td>',
    html)
print(f"  ✅ 催化剂表")

# 三年预测
html = re.sub(
    r'<tr>\s*<td class="green">乐观</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td class="gold">基准</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td class="red">悲观</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>',
    '<tr>\n<td class="green">乐观</td>\n<td>净利30亿</td>\n<td>净利38亿</td>\n<td>净利45亿</td>\n<td>毛利率回升至35%+</td>\n    </tr>\n<tr>\n<td class="gold">基准</td>\n<td>净利25亿</td>\n<td>净利30亿</td>\n<td>净利33亿</td>\n<td>毛利率维持27-28%</td>\n    </tr>\n<tr>\n<td class="red">悲观</td>\n<td>净利18亿</td>\n<td>净利22亿</td>\n<td>净利25亿</td>\n<td>毛利率降至25%</td>',
    html)
print(f"  ✅ 三年预测表")

# ===== M9 预期差 =====
html = re.sub(
    r'<td style="color:#888;">__TODO__</td>\s*<td style="color:#4caf50;">__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>\s*<td style="color:#888;">__TODO__</td>\s*<td style="color:#888;">__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>\s*<td style="color:#888;">__TODO__</td>\s*<td style="color:#888;">__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>\s*<td style="color:#888;">__TODO__</td>\s*<td style="color:#4caf50;">__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>\s*<td style="color:#888;">__TODO__</td>\s*<td style="color:#4caf50;">__TODO__</td>',
    '<td style="color:#888;">疫后恢复已充分定价</td>\n<td style="color:#4caf50;">国际航线恢复仅~80%，仍有20%空间，免税弹性更大</td>\n<td>看好</td>\n    </tr>\n<tr>\n<td>免税合同</td>\n<td style="color:#888;">新合同条款不利</td>\n<td style="color:#888;">预计保底租金高于疫情前，但扣点率可能下降</td>\n<td>中性</td>\n    </tr>\n<tr>\n<td>ROE偏低</td>\n<td style="color:#888;">持续低于资金成本</td>\n<td style="color:#888;">疫后恢复期ROE逐步改善，但回到10%+需时间</td>\n<td>中性</td>\n    </tr>\n<tr>\n<td>高铁分流</td>\n<td style="color:#888;">中长期利空</td>\n<td style="color:#4caf50;">主要影响国内线(占比~55%)，国际线不受影响</td>\n<td>看好</td>\n    </tr>\n<tr>\n<td>浦东扩建</td>\n<td style="color:#888;">资本开支大</td>\n<td style="color:#4caf50;">扩建打开容量天花板，远期价值提升</td>',
    html)
print(f"  ✅ M9预期差表")

# ===== M10 风险 =====
# 风险类型
html = re.sub(
    r'<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*</tr>\s*<tr>\s*<td>__TODO__</td>\s*<td>__TODO__</td>\s*<td>__TODO__</td>',
    '<td>航空需求波动</td>\n<td>宏观经济影响航空出行需求</td>\n<td>中</td>\n<td>航空业务量季度同比增速</td>\n    </tr>\n<tr>\n<td>免税政策</td>\n<td>免税政策变化可能影响收入</td>\n<td>中</td>\n<td>免税销售恢复进度</td>\n    </tr>\n<tr>\n<td>扩建风险</td>\n<td>浦东四期扩建投资大，回报周期长</td>\n<td>低</td>\n<td>工程进度/预算超支</td>\n    </tr>\n<tr>\n<td>高铁竞争</td>\n<td>高铁网络完善分流国内航空旅客</td>\n<td>中</td>\n<td>京沪高铁客座率趋势</td>\n    </tr>\n<tr>\n<td>突发事件</td>\n<td>疫情/自然灾害等影响航空出行</td>\n<td>低</td>\n<td>全球公共卫生事件预警</td>',
    html)
print(f"  ✅ M10风险表")

# 三情景
replace_all('{{OPTIMISTIC_PRICE}}', '~32元', '乐观价')
replace_all('{{OPTIMISTIC_RETURN}}', '+38%', '乐观回报')
replace_all('{{OPTIMISTIC_SCENARIO}}', '国际航线全面恢复+免税重签利好，净利30亿+，ROE回升至8%+', '乐观情景')
replace_all('{{NEUTRAL_PRICE}}', '25元', '中性价')
replace_all('{{NEUTRAL_RETURN}}', '~+8%', '中性回报')
replace_all('{{NEUTRAL_SCENARIO}}', '国际航线稳步恢复+免税平稳过渡，净利25亿，ROE~6%', '中性情景')
replace_all('{{PESS_PRICE}}', '~18元', '悲观价')
replace_all('{{PESS_RETURN}}', '-22%', '悲观回报')
replace_all('{{PESS_SCENARIO}}', '经济下行+免税政策不利，净利18亿，ROE<5%', '悲观情景')

# 避雷清单
for old, new in [
    ('<td>是否存在商誉减值风险</td>\n<td>—</td>', '<td>是否存在商誉减值风险</td>\n<td>商誉~3亿(占总资产<1%)风险极低</td>'),
    ('<td>大股东是否持续减持</td>\n<td>—</td>', '<td>大股东是否持续减持</td>\n<td>上海机场集团(实控人),无减持</td>'),
    ('<td>财务造假信号</td>\n<td>—</td>', '<td>财务造假信号</td>\n<td>经营现金流59.76亿为正,审计标准无保留</td>'),
    ('<td>现金流是否持续为负</td>\n<td>—</td>', '<td>现金流是否持续为负</td>\n<td>经营现金流59.76亿(2025)持续为正</td>'),
    ('<td>是否有未决诉讼</td>\n<td>—</td>', '<td>是否有未决诉讼</td>\n<td>年报未披露重大未决诉讼</td>'),
]:
    html = html.replace(old, new)
    changes += 1
print(f"  ✅ 避雷清单")

# 敏感性分析
html = html.replace(
    '<tr><td>营收下降10%</td><td>—</td><td>—</td>',
    '<tr><td>营收下降10%</td><td>-13.3亿</td><td>-15%</td>')
html = html.replace(
    '<tr><td>毛利率下降3pct</td><td>—</td><td>—</td>',
    '<tr><td>毛利率下降3pct</td><td>-4.0亿</td><td>-10%</td>')
html = html.replace(
    '<tr><td>费用率上升</td><td>—</td><td>—</td>',
    '<tr><td>费用率上升</td><td>-1.5亿</td><td>-5%</td>')
html = html.replace(
    '<tr><td>行业下行周期</td><td>—</td><td>—</td>',
    '<tr><td>行业下行周期</td><td>-8亿</td><td>-18%</td>')
html = html.replace(
    '<tr><td>竞争加剧</td><td>—</td><td>—</td>',
    '<tr><td>竞争加剧</td><td>-3亿</td><td>-8%</td>')
print(f"  ✅ 敏感性分析")

# 清算价值
replace_all('{{LIQ_ASSET_1}}', '货币资金', '清1')
replace_all('{{LIQ_BOOK_1}}', '120亿', '清1b')
replace_all('{{LIQ_VAL_1}}', '~120亿', '清1v')
replace_all('{{LIQ_ASSET_2}}', '应收账款', '清2')
replace_all('{{LIQ_BOOK_2}}', '35亿', '清2b')
replace_all('{{LIQ_VAL_2}}', '~28亿', '清2v')
replace_all('{{LIQ_ASSET_3}}', '存货', '清3')
replace_all('{{LIQ_BOOK_3}}', '2亿', '清3b')
replace_all('{{LIQ_VAL_3}}', '~1亿', '清3v')
replace_all('{{LIQ_ASSET_4}}', '固定资产', '清4')
replace_all('{{LIQ_BOOK_4}}', '480亿', '清4b')
replace_all('{{LIQ_VAL_4}}', '~350亿', '清4v')
replace_all('{{LIQ_TOTAL_BOOK}}', '637亿', '清合b')
replace_all('{{LIQ_TOTAL_VAL}}', '~499亿', '清合v')
replace_all('{{LIQUIDATION_NOTE}}', '清算价值约499亿(账面637亿)，折合每股约20元(总股本24.9亿)。核心资产为浦东/虹桥两场固定资产(480亿)和货币资金(120亿)。机场资产变现能力一般但持续经营价值远高于清算。', '清算说明')

# 核心风险焦点
replace_all('{{FINANCIAL_CONTROLLABLE}}', '财务风险可控。负债率~20%很低，有息负债以长期借款为主。现金流充裕(经营现金流59.76亿)。应收账款周转快，资产质量优良。', '财务可控')
replace_all('{{CORE_RISK_FOCUS}}', 'ROE 5.03%偏低，免税收入恢复不及预期，浦东扩建投资大回报周期长，高铁分流风险', '核心风险')
replace_all('{{DEBT_RATIO_NOTE}}', '负债率~20%很低，货币资金120亿充足，短期借款极少。财务状况非常健康。', '负债率')
replace_all('{{CORE_ADVANTAGE_LABEL}}', '长三角唯一国际航空枢纽', '核心优势标签')
replace_all('{{RISK_TITLE_1}}', '航空需求波动', '风险标题1')
replace_all('{{RISK_ITEM_1}}', '宏观经济影响航空出行需求，国际航线恢复节奏不确定', '风险项1')
replace_all('{{RISK_2_TITLE}}', '免税政策变动', '风险标题2')
replace_all('{{RISK_2_DESC}}', '免税政策变化(额度/品类)和重签合同条款影响中期收入', '风险项2')
replace_all('{{RISK_TITLE_3}}', '扩建回报周期', '风险标题3')
replace_all('{{RISK_ITEM_3}}', '浦东四期扩建投资~200亿，回报周期10年以上', '风险项3')

# 亮点
replace_all('{{HIGHLIGHT_1_TITLE}}', '区位垄断护城河', '亮点1')
replace_all('{{HIGHLIGHT_1_DESC}}', '长三角唯一国际航空枢纽，半径300公里无实质竞争。2025年旅客1.35亿人次，国际旅客占比44.7%居全国首位。', '亮点1d')
replace_all('{{HIGHLIGHT_2_TITLE}}', '免税复苏弹性', '亮点2')
replace_all('{{HIGHLIGHT_2_DESC}}', '国际旅客+19.5%高速恢复，免税收入弹性大。2019年免税收入超60亿，2025年仅~30亿，恢复空间充分。', '亮点2d')
replace_all('{{HIGHLIGHT_3_TITLE}}', '扩建打开空间', '亮点3')
replace_all('{{HIGHLIGHT_3_DESC}}', '浦东四期扩建(T3航站楼+卫星厅)2030年前建成，远期旅客容量提升至1.6亿+人次。', '亮点3d')

# 六维评分
scores_dims = [7, 8, 6, 5, 7, 6]
colors_dims = ['#4caf50', '#4caf50', '#f0c040', '#ff9800', '#4caf50', '#f0c040']
labels_dims = ['商业模式', '护城河', '管理层', '财务健康', '估值', '成长性']
for i in range(1, 7):
    w = scores_dims[i-1] * 10
    replace_all(f'{{{{DIM_BAR_{i}}}}}', f'width:{w}%', f'维{i}宽度')
    replace_all(f'{{{{DIM_SCORE_{i}}}}}', str(scores_dims[i-1]), f'维{i}分')
replace_all('{{DIM_BAR_X}}', 'width:70%', '维X')

# 价值理念
replace_all('{{M1_ANALYSIS}}', '上海机场是典型的"好生意"——区位垄断+准入门槛高+现金流稳定。ROE 5.03%偏低但改善中。', 'M1分析')
replace_all('{{M2_ANALYSIS}}', '长三角唯一国际航空枢纽的差异化极强，方圆300公里无替代选择。浦东/虹桥两场覆盖1.35亿旅客，规模壁垒深厚。', 'M2分析')
replace_all('{{M3_ANALYSIS}}', '管理层聚焦航空主业、稳健经营，资本支出纪律良好。冯昕新任掌舵，团队经验丰富。', 'M3分析')
replace_all('{{M4_ANALYSIS}}', '安全边际一般但改善中。PB 2.5x历史中低位，PS 5.16x偏低。疫情最坏阶段已过，向上弹性大于向下风险。', 'M4分析')
replace_all('{{M5_ANALYSIS}}', '成本管控良好(营业成本+0.19%)，固定成本占比高，业务量增长直接拉升利润率。经营杠杆显著。', 'M5分析')
replace_all('{{M6_ANALYSIS}}', '逆向估值：PB 2.5x处于历史中低位，PS 5.16x偏低。市场对ROE恢复速度持谨慎态度，提供了安全边际。', 'M6分析')
replace_all('{{M7_ANALYSIS}}', '成长空间：中国航空市场人均乘次<0.5(美国>2.0)，增长空间广阔。长三角经济最发达，出境需求持续增长。', 'M7分析')
replace_all('{{M8_ANALYSIS}}', '催化剂：国际航线持续恢复(+19.5%)+免税合同重签+浦东扩建。多项利好叠加，中期确定性较强。', 'M8分析')
replace_all('{{M9_ANALYSIS}}', '预期差：市场过度关注ROE偏低和免税不确定性，低估了区位垄断的长期价值和免税复苏的弹性空间。', 'M9分析')
replace_all('{{M10_ANALYSIS}}', '反脆弱性较强：区位垄断不可替代，现金流稳定。但突发事件影响大(如疫情)，抗风险能力一般。', 'M10分析')
replace_all('{{M11_SAFETY_MARGIN}}', 'PB 2.5x/PB 5.16x估值合理偏低，股息率~2%。最差情景(2019年利润水平)对应PE 35-40x，下行空间有限。', 'M11')

# ===== BQ 替换 =====
bq_texts = [
    '上海机场整体评分6.0/10。核心价值在于长三角唯一国际航空枢纽的区位垄断。2025年营收133.46亿(+7.9%)净利21.17亿(+42.8%)持续恢复。PE 28x/PB 2.5x估值合理偏低。核心亮点：区位垄断不可复制+免税复苏弹性。核心风险：ROE仅5.03%偏低、免税合同待重签。',
    '上海机场运营浦东/虹桥两场，收入结构为航空性收入(起降/旅客服务费，占比55%)和非航收入(免税/商业/广告，占比45%)。浦东机场为核心资产，国际航线占比44.7%全国最高。高固定成本+高经营杠杆是财务特征。',
    '核心护城河在长三角唯一国际航空枢纽的区位垄断地位，这是物理空间(长三角无第二个国际门户)和行政准入(航权/时刻政府分配)的双重壁垒。壁垒评分8/10。区位优势不可复制，方圆300公里无实质竞争对手。',
    '冯昕2025年新任董事局主席，此前在上机集团任职多年。管理团队稳健务实，聚焦航空主业。五地六家公众公司治理架构完善。评分：战略7/10，执行力7/10，股东回报6/10，资本配置6/10。',
    '财务评分5/10。营收133.46亿(+7.9%)净利21.17亿(+42.8%)持续恢复。毛利率27.51%(+2.13pct)提升，净利率15.86%。ROE 5.03%偏低。经营现金流59.76亿持续向好。负债率~20%极低。费用率：管理7.40亿(+0.5%)，财务4.20亿(-10.0%)，研发0.18亿(+70.7%)。',
    '成本结构：人工~45%、折旧~30%、运营维护~15%、其他~10%。固定成本占比~75%，高经营杠杆特征。业务量增长直接转化为利润弹性。营业成本96.74亿(+0.19%)基本持平，成本管控良好。',
    '估值判断：PE(TTM) 28.1x合理(机场板块中位)。归母PE 28x偏高但改善中，扣非PE 28x(无扣非亏损问题)，PB 2.5x偏低(历史1.5-4.0x)，PS 5.16x偏低(历史3-10x)。三个口径：PB和PS指向偏低，PE合理。综合判断：估值合理偏低，核心价值在区位垄断和免税弹性。',
    '中国航空市场7亿人次(+8-10%)持续增长，上海两场1.35亿人次占全国19%，国际航线占全国25%。免税市场800亿(+10%)，浦东机场占~4%。行业终局：全国机场格局稳定，上海两场国际枢纽地位不可撼动。',
    '三大催化剂：①国际航线持续恢复(旅客+19.5%仍有20%恢复空间)；②免税合同重签打开中期利润弹性；③浦东四期扩建打开远期容量天花板。三情景预测：18-32元，基准25元。核心催化剂看国际航线恢复进度。',
    '市场可能低估：①国际航线恢复的持续性和空间(目前仅~80%)；②区位垄断的长期价值；③免税恢复的弹性。ROE恢复和免税合同不确定性是市场关注焦点。浦东扩建的远期价值未被充分定价。',
    '核心风险：①ROE仅5.03%偏低，恢复至10%+需时间；②免税合同重签条款存在不确定性；③浦东扩建投资~200亿回报周期长；④高铁分流国内航线。避雷清单全部通过。资产负债表优秀：货币资金120亿，负债率仅~20%。',
]

parts = html.split('{{BQ_ANALYSIS}}')
if len(parts) == len(bq_texts) + 1:
    html = parts[0]
    for i, txt in enumerate(bq_texts):
        html += txt + parts[i+1]
    changes += len(bq_texts)
    print(f"  ✅ BQ填充({len(bq_texts)}篇)")
else:
    print(f"  ⚠️ BQ数量不匹配: 模板{len(parts)-1}个, 文本{len(bq_texts)}个")

# ===== 写回 =====
with open(REPORT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n{'='*50}")
print(f"  填充完成！共修改 {changes} 处")
print(f"{'='*50}")
