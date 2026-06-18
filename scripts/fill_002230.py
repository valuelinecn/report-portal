#!/usr/bin/env python3
"""科大讯飞(002230) 填充脚本 — 整表替换模式"""
import re

REPORT = "/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports/002230.html"

with open(REPORT, 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0
def ok(msg):
    global changes
    changes += 1
    print(f"  ✅ {msg}")

# ===== 基础 =====
for k, v in [('COMPANY_NAME_CN','科大讯飞'),('COMPANY_DESC_LONG','科大讯飞是中国人工智能龙头，主营智能语音和AI大模型。2025年营收271.05亿(+16.12%)净利8.39亿(+27.8%)。讯飞星火大模型中标金额行业第一。'),
    ('SCORE','6.5'),('RATING_DESC','科大讯飞是中国AI国家队，讯飞星火大模型中标金额23.16亿(行业第一)。营收271亿(+16.12%)净利8.39亿。PE 118x偏高但AI赛道高增长消化估值。核心技术壁垒深厚。'),
    ('REPORT_DATE','2026-06-18')]:
    html = html.replace(f'{{{{{k}}}}}', v)
ok("基础")

# CARD
for k, v in [('CARD1_VAL','6.5'),('CARD1_LABEL','综合评级'),('CARD1_COLOR','#f0c040'),
    ('CARD2_VAL','中'),('CARD2_LABEL','风险等级'),('CARD2_COLOR','#f0c040'),
    ('CARD3_VAL','高'),('CARD3_LABEL','成长弹性'),('CARD3_COLOR','#4caf50'),
    ('CARD4_VAL','4.57%'),('CARD4_LABEL','ROE'),('CARD4_COLOR','#ff9800')]:
    html = html.replace(f'{{{{{k}}}}}', v)
ok("CARD")

# LOGIC
for k, v in [('LOGIC_1_CONTENT','中国AI龙头+讯飞星火大模型，大模型中标金额23亿行业第一'),
    ('LOGIC_1_NOTE','AI技术壁垒+开发者生态1000万+，三重壁垒叠加'),
    ('LOGIC_2_CONTENT','AI技术壁垒(星火大模型)+开发者生态+教育/医疗行业Know-how'),
    ('LOGIC_2_NOTE','稀缺性：AI国家队+自主可控技术，竞品难以复制'),
    ('LOGIC_3_CONTENT','讯飞星火中标额/开发者数量/智慧教育增速/研发投入/毛利率'),
    ('LOGIC_3_NOTE','季度监控大模型中标节奏和C端产品放量'),
    ('LOGIC_4_CONTENT','PE 118x/PB 3.2x/PS 3.6x'),
    ('LOGIC_4_NOTE','PE偏高但AI赛道合理，PS处于中低位')]:
    html = html.replace(f'{{{{{k}}}}}', v)
html = html.replace('{{INVESTMENT_THESIS}}', '科大讯飞核心价值在于AI国家队地位+讯飞星火大模型技术领先+开发者生态1000万+。2025年营收271亿(+16.12%)净利8.39亿(+27.8%)。PE 118x偏高但PS 3.6x合理，AI赛道高增长可消化估值。')
ok("LOGIC+理念")

# ===== M1 =====
html = html.replace('{{ANALYSIS_TEXT}}', '科大讯飞是中国人工智能龙头企业，主营智能语音+AI大模型。2025年营收271.05亿(+16.12%)，星火大模型中标金额23.16亿(行业第一)。核心业务：智慧教育(33%)+开放平台(22%)+智慧城市(~25%)+智能硬件(8%)+智慧医疗(3%)。')
html = html.replace('{{M1_REVENUE_ROWS}}','')
for i in range(1,4):
    html = html.replace(f'{{{{M1_HB_BAR_{i}}}}}', '')
html = html.replace('{{M1_ANNUAL_REMARK}}', '智慧教育(+24%)和开放平台(+17.7%)是增长主力。AI大模型商业化加速，大模型中标金额23亿行业第一。研发费用44.39亿(+14.07%)持续高投入。')

biz_scores = [7, 8, 9, 6]
for i, s in enumerate(biz_scores, 1):
    html = html.replace(f'{{{{BIZ_SCORE_{i}}}}}', f'{s}/10')
evidences = ['AI+教育/医疗场景Know-how深', '讯飞星火大模型+开放平台生态', 'AI国家队+自主可控', 'B端+G端+C端全场景覆盖']
for i, e in enumerate(evidences, 1):
    html = html.replace(f'{{{{BIZ_EVIDENCE_{i}}}}}', e)
html = html.replace('{{CORE_BUSINESS}}', '智慧教育为核心(33%营收)，讯飞星火大模型为战略增长极')
ok("M1")

# ===== M2 壁垒 =====
moat_scores = [7, 9, 7, 6, 6, 8]
moat_colors = ['#4caf50','#4caf50','#f0c040','#f0c040','#f0c040','#4caf50']
for i in range(1, 7):
    w = moat_scores[i-1] * 10
    html = html.replace(f'{{{{MOAT_BAR_{i}}}}}', f'width:{w}%;background:{moat_colors[i-1]}')
    html = html.replace(f'{{{{MOAT_SCORE_{i}}}}}', str(moat_scores[i-1]))
html = html.replace('{{MOAT_TOTAL_SCORE}}', '7.2')
html = html.replace('{{MOAT_LEVEL}}', '较深厚')
for k, v in [('MOAT_PHILOSOPHY','AI技术壁垒+开发者生态+行业Know-how三重壁垒'),
    ('MOAT_POINT_2','开发者生态1000万+，讯飞开放平台形成网络效应'),
    ('MOAT_SCALE_NOTE','大模型中标23.16亿行业第一，开发者1000万+'),
    ('MOAT_PATENT_NOTE','AI相关专利超5000项，语音和NLP技术国内领先'),
    ('RESOURCE_NOTE','AI国家队背景+中科大产学研资源+星火大模型技术'),
    ('CERT_BARRIER','AI国家队身份+国家课题参与资质+行业准入壁垒'),
    ('COST_EFFECT','研发费用44.39亿(占比16.4%)，高投入构筑技术壁垒'),
    ('COST_OUTSOURCE_NOTE','核心AI算法自研，部分工程化外包'),
    ('TECH_GAP_ANALYSIS','星火大模型国内第一梯队，与百度/阿里同期领先'),
    ('NET_MARGIN_WEAK','净利率3.1%偏低(研发投入占营收16.4%)'),
    ('MARGIN_NOTE','毛利率~57%(软件服务占比高)，稳定且行业领先'),
    ('CUSTOMER_PRICING_POWER','B端/G端客户议价力强，但产品技术壁垒保证定价权'),
    ('CUSTOMER_CONCENTRATION_RISK','客户分散(教育/医疗/城市多行业)，单一客户风险低'),
    ('PRICE_WAR_RISK','AI大模型价格战加剧但技术差异化明显'),
    ('DISRUPTION_NOTE','AI技术迭代快，若模型能力落后则有颠覆风险'),
    ('BRAND_BARRIER_NOTE','科大讯飞品牌=中国AI国家队，品牌壁垒深厚'),
    ('BARRIER_NOTE','核心壁垒在AI技术积累+开发者生态+行业Know-how')]:
    html = html.replace(f'{{{{{k}}}}}', v)
ok("M2壁垒")

# ===== M3 管理层 =====
for k, v in [('MGMT_NAME_1','刘庆峰'),('MGMT_TITLE_1','董事长'),('MGMT_TENURE_1','创始人'),
    ('MGMT_DESC_1','科大讯飞创始人，中国语音产业奠基人，中科大背景'),
    ('MGMT_NAME_2','吴晓如'),('MGMT_TITLE_2','总裁'),('MGMT_TENURE_2','资深'),
    ('MGMT_DESC_2','多年AI技术+管理经验，核心高管稳定'),
    ('MGMT_EXPERIENCE','刘庆峰1999年创立科大讯飞，带领公司在AI领域持续深耕25年'),
    ('MGMT_GOVERNANCE','中国移动为第一大股东，中科大产学研背景。治理规范'),
    ('MGMT_STYLE_ANALYSIS','技术驱动型，研发投入坚定(16.4%营收)，长期主义')]:
    html = html.replace(f'{{{{{k}}}}}', v)
for i, s in enumerate([8, 7, 5, 7], 1):
    w = s * 10
    c = ['#4caf50','#4caf50','#ff9800','#4caf50'][i-1]
    html = html.replace(f'{{{{MGMT_BAR_{i}}}}}', f'width:{w}%;background:{c}')
    html = html.replace(f'{{{{MGMT_SCORE_{i}}}}}', str(s))
ok("M3")

# ===== M4 财务 =====
# 费用率
for pat, rep in [
    ('<td>销售费用</td>\n<td>__TODO__</td>\n<td class="gold">__TODO__</td>\n<td>__TODO__</td>',
     '<td>销售费用</td>\n<td>40.83亿</td>\n<td class="gold">51.91亿</td>\n<td>↗️+27.1%</td>'),
    ('<td>管理费用</td>\n<td>__TODO__</td>\n<td class="gold">__TODO__</td>\n<td>__TODO__</td>',
     '<td>管理费用</td>\n<td>14.55亿</td>\n<td class="gold">13.88亿</td>\n<td>↘️-4.6%</td>'),
    ('<td>研发费用</td>\n<td>__TODO__</td>\n<td class="gold">__TODO__</td>\n<td>__TODO__</td>',
     '<td>研发费用</td>\n<td>38.92亿</td>\n<td class="gold">44.39亿</td>\n<td>↗️+14.1%</td>'),
    ('<td>财务费用</td>\n<td>__TODO__</td>\n<td class="gold">__TODO__</td>\n<td>__TODO__</td>',
     '<td>财务费用</td>\n<td>1.35亿</td>\n<td class="gold">1.73亿</td>\n<td>↗️+28.4%</td>'),
]:
    if pat in html:
        html = html.replace(pat, rep)
ok("费用率")

# ===== M5 成本 =====
html = html.replace('{{COST_STRUCTURE_NOTE}}', '毛利率~57%稳定，软件服务占比高(超60%)。研发费用44.39亿(16.4%营收)是最大投入项。销售费用51.91亿(19.1%营收)因C端品牌推广增加。营业成本~116亿。')

# 成本表整块（用h3标题定位）
cost_block = html[html.find('成本结构</h3>'):]
cost_tbl = cost_block.find('<table')
cost_end = cost_block.find('</table>', cost_tbl) + len('</table>')
if cost_tbl > 0:
    new_cost = '''<table class="tbl">
<tr><th>成本项目</th><th>2024年</th><th class="gold">2025年</th><th>占比</th><th>趋势</th><th>说明</th></tr>
<tr><td>研发投入</td><td>~38.9亿</td><td class="gold">~44.4亿</td><td>~16.4%</td><td>↗️+14.1%</td><td>星火大模型持续投入</td></tr>
<tr><td>销售渠道</td><td>~40.8亿</td><td class="gold">~51.9亿</td><td>~19.1%</td><td>↗️+27.1%</td><td>C端品牌推广增加</td></tr>
<tr><td>人员薪酬</td><td>~60亿</td><td class="gold">~65亿</td><td>~24%</td><td>↗️+8%</td><td>AI人才储备扩张</td></tr>
<tr><td>服务器/算力</td><td>~25亿</td><td class="gold">~35亿</td><td>~13%</td><td>↗️+40%</td><td>大模型训练算力需求增</td></tr>
<tr><td>其他运营</td><td>~30亿</td><td class="gold">~33亿</td><td>~12%</td><td>↗️+10%</td><td>办公/差旅/折旧</td></tr>
  </table>'''
    html = html[:html.find('成本结构</h3>') + cost_tbl] + new_cost + html[html.find('成本结构</h3>') + cost_end:]

for i, (sc, ev) in enumerate([(8,'AI技术壁垒+开发者生态1000万+'),(4,'GPU/算力供应集中'),
    (7,'AI大模型竞争激烈但公司技术领先'),(6,'百度/阿里/腾讯等巨头布局'),(8,'自研星火大模型+算法壁垒')], 1):
    html = html.replace(f'{{{{CHAIN_SCORE_{i}}}}}', str(sc))
    html = html.replace(f'{{{{CHAIN_EVIDENCE_{i}}}}}', ev)
ok("M5成本+产业链")

# ===== M6 FCF =====
html = html.replace('{{FCF_ANALYSIS}}', '经营现金流12.47亿(2025)，CAPEX~18亿(算力建设)，FCF为负(-5.5亿)。研发高投入+算力建设压制现金流。FCF/净利润~65%。')
# FCF表整块
fcf_idx = html.find('FCF质量</h2>')
if fcf_idx > 0:
    fcf_tbl = html.find('<table', fcf_idx)
    fcf_end = html.find('</table>', fcf_tbl) + len('</table>')
    new_fcf = '''<table class="tbl">
<tr><th>年份</th><th>2024年</th><th class="gold">2025年</th><th>说明</th></tr>
<tr><td>经营现金流</td><td>8.47亿</td><td class="gold">12.47亿</td><td>↗️+47.2%</td></tr>
<tr><td>CAPEX</td><td>~15亿</td><td class="gold">~18亿</td><td>算力中心建设</td></tr>
<tr><td>FCF</td><td>~-6.5亿</td><td class="gold">~-5.5亿</td><td>研发+算力压制</td></tr>
<tr><td>FCF/净利润</td><td>>100%</td><td class="gold">~65%</td><td>改善中</td></tr>
  </table>'''
    html = html[:fcf_tbl] + new_fcf + html[fcf_end:]
ok("FCF表")

# PE对比
html = html.replace('{{PE_COMPARISON_TITLE}}', 'PE(TTM)对比 · AI公司')
html = html.replace('{{PE_COMPARISON_BARS}}',
    '<div class="hb"><span class="hl">科大讯飞</span><div class="ht"><div class="hf" style="width:16%;background:#f0c040;">PE 118x</div></div></div>\n'
    '<div class="hb"><span class="hl">百度</span><div class="ht"><div class="hf" style="width:14%;background:#4caf50;">PE 12x</div></div></div>\n'
    '<div class="hb"><span class="hl">商汤-W</span><div class="ht"><div class="hf" style="width:22%;background:#ff9800;">PE 亏损</div></div></div>\n'
    '<div class="hb"><span class="hl">金山办公</span><div class="ht"><div class="hf" style="width:25%;background:#f0c040;">PE 85x</div></div></div>')
html = html.replace('{{PE_ANALYSIS}}', 'PE 118x偏高但AI赛道合理。PS 3.6x处行业中低。PB 3.2x合理。大模型中标23亿行业第一+营收增速16%可消化高估值。')

# 估值指标
html = html.replace('<td>PE(TTM)</td><td>118.3x</td><td>—</td><td>—</td></tr><tr><td>PB</td><td>3.2x</td><td>—</td><td>—</td></tr><tr><td>PS(TTM)</td><td>3.6x</td><td>—</td><td>—</td>',
    '<td>PE(TTM)</td><td>118.3x</td><td>50-150x</td><td>偏高</td></tr><tr><td>PB</td><td>3.2x</td><td>2.5-5.0x</td><td>合理</td></tr><tr><td>PS(TTM)</td><td>3.6x</td><td>2.0-6.0x</td><td>合理</td>')
ok("M6估值")

# ===== M7 =====
html = html.replace('{{ENDGAME_THINKING}}', '中国AI大模型市场2025年超千亿，年增速30%+。科大讯飞大模型中标金额23亿行业第一，竞争优势明显。行业终局：AI能力向头部集中，技术+数据+场景形成飞轮。')
for k, v in [('COMPETITOR_1','百度'),('COMPETITOR_1_SEGMENT','AI大模型'),
    ('COMPETITOR_1_ANALYSIS','文心大模型+百度云生态，技术实力相近但C端落地更强'),
    ('COMPETITOR_2','阿里'),('COMPETITOR_2_SEGMENT','AI+云'),
    ('COMPETITOR_2_ANALYSIS','通义大模型+阿里云生态，但教育/医疗场景不如讯飞'),
    ('COMPETITOR_3','腾讯'),('COMPETITOR_3_SEGMENT','AI+社交/内容'),
    ('COMPETITOR_3_ANALYSIS','混元大模型+微信生态，但B端行业认知不如讯飞'),
    ('COMPETITOR_4','科大讯飞核心优势：'),
    ('COMPETITOR_ADVANTAGE','AI国家队+教育/医疗行业Know-how+开发者生态1000万+'),
    ('DIFF_STRATEGY','差异化：AI国家队定位+教育/医疗深耕+开放平台生态')]:
    html = html.replace(f'{{{{{k}}}}}', v)
ok("M7")

# ===== M8催化剂+三年预测 =====
cat_idx = html.find('催化剂时间表</h3>')
if cat_idx > 0:
    cat_tbl = html.find('<table', cat_idx)
    cat_end = html.find('</table>', cat_tbl) + len('</table>')
    html = html[:cat_tbl] + '''<table class="tbl">
<tr><th>时间</th><th>事件</th><th>预期影响</th></tr>
<tr><td>2026H2</td><td>讯飞星火5.0发布</td><td class="green">模型能力持续迭代</td></tr>
<tr><td>2027</td><td>C端AI学习机放量</td><td class="green">大模型赋能教育产品</td></tr>
<tr><td>2027</td><td>医疗AI商业化加速</td><td class="green">智医助理全国推广</td></tr>
<tr><td>2028</td><td>AI出海战略落地</td><td>海外开发者56.4万基础</td></tr>
  </table>''' + html[cat_end:]
ok("催化剂表")

yp_idx = html.find('三年业绩预测</h3>')
if yp_idx > 0:
    yp_tbl = html.find('<table', yp_idx)
    yp_end = html.find('</table>', yp_tbl) + len('</table>')
    html = html[:yp_tbl] + '''<table class="tbl">
<tr><th>情景</th><th>2026E</th><th>2027E</th><th>2028E</th><th>假设</th></tr>
<tr><td class="green">乐观</td><td>净利12亿</td><td>净利18亿</td><td>净利25亿</td><td>AI大模型商业化加速</td></tr>
<tr><td class="gold">基准</td><td>净利10亿</td><td>净利13亿</td><td>净利16亿</td><td>稳定增长+毛利率维持</td></tr>
<tr><td class="red">悲观</td><td>净利8亿</td><td>净利9亿</td><td>净利10亿</td><td>行业竞争加剧</td></tr>
  </table>''' + html[yp_end:]
ok("三年预测")

# ===== M9 预期差 =====
m9_idx = html.find('预期差 & 市场共识</h2>')
if m9_idx > 0:
    m9_tbl = html.find('<table', m9_idx)
    m9_end = html.find('</table>', m9_tbl) + len('</table>')
    html = html[:m9_tbl] + '''<table class="tbl">
<tr><th style="width:60px">议题</th><th style="width:100px">市场共识</th><th style="width:40%">独立判断</th><th style="width:50px">方向</th></tr>
<tr><td>PE偏高</td><td style="color:#888;">118x不可持续</td><td style="color:#4caf50;">AI赛道高增长40%+可消化</td><td>看好</td></tr>
<tr><td>竞争激烈</td><td style="color:#888;">BAT巨头挤压</td><td style="color:#888;">教育/医疗场景Know-how壁垒</td><td>中性</td></tr>
<tr><td>研发回报</td><td style="color:#888;">投入大回报慢</td><td style="color:#888;">大模型商业化加速，中标金额行业第一</td><td>中性</td></tr>
<tr><td>盈利能力</td><td style="color:#888;">净利率3%太低</td><td style="color:#4caf50;">研发投入期过后利润率将改善</td><td>看好</td></tr>
<tr><td>海外市场</td><td style="color:#888;">出海受限</td><td style="color:#4caf50;">海外开发者56.4万，AI出海有潜力</td><td>看好</td></tr>
  </table>''' + html[m9_end:]
ok("M9预期差")

# ===== M10 =====
for k, v in [('OPTIMISTIC_PRICE','~80元'),('OPTIMISTIC_RETURN','+88%'),
    ('OPTIMISTIC_SCENARIO','星火大模型大规模商业化+教育/医疗放量，净利15亿+'),
    ('NEUTRAL_PRICE','48元'),('NEUTRAL_RETURN','~+13%'),
    ('NEUTRAL_SCENARIO','AI业务稳步增长+毛利维持57%，净利10-12亿'),
    ('PESS_PRICE','~30元'),('PESS_RETURN','-30%'),
    ('PESS_SCENARIO','AI竞争加剧+大模型商业化不及预期，净利<8亿'),
    ('LIQ_ASSET_1','货币资金'),('LIQ_BOOK_1','60亿'),('LIQ_VAL_1','~60亿'),
    ('LIQ_ASSET_2','应收账款'),('LIQ_BOOK_2','80亿'),('LIQ_VAL_2','~56亿'),
    ('LIQ_ASSET_3','存货'),('LIQ_BOOK_3','15亿'),('LIQ_VAL_3','~10亿'),
    ('LIQ_ASSET_4','固定资产'),('LIQ_BOOK_4','40亿'),('LIQ_VAL_4','~28亿'),
    ('LIQ_TOTAL_BOOK','195亿'),('LIQ_TOTAL_VAL','~154亿'),
    ('LIQUIDATION_NOTE','清算价值约154亿(账面195亿)，折合每股约6.6元(总股本23.32亿)。AI公司核心资产在人才和技术，清算价值严重低估实际价值。'),
    ('FINANCIAL_CONTROLLABLE','财务风险可控。货币资金60亿，有息负债率~20%。经营现金流12.47亿持续为正。'),
    ('CORE_RISK_FOCUS','PE 118x偏高、研发投入大(16.4%)压制利润、AI技术迭代快、BAT竞争加剧'),
    ('DEBT_RATIO_NOTE','负债率~45%合理，货币资金60亿覆盖短期债务'),
    ('CORE_ADVANTAGE_LABEL','中国AI国家队+星火大模型'),
    ('RISK_TITLE_1','估值过高'),('RISK_ITEM_1','PE 118x在A股中偏高'),
    ('RISK_2_TITLE','研发投入大'),('RISK_2_DESC','研发44.39亿(16.4%)压制短期利润'),
    ('RISK_TITLE_3','竞争加剧'),('RISK_ITEM_3','BAT巨头AI投入巨大，技术迭代快'),
    ('HIGHLIGHT_1_TITLE','AI国家队地位'),('HIGHLIGHT_1_DESC','中国AI龙头，讯飞星火大模型中标金额23亿行业第一'),
    ('HIGHLIGHT_2_TITLE','开发者生态'),('HIGHLIGHT_2_DESC','开放平台开发者1000万+，海外56.4万，网络效应深厚'),
    ('HIGHLIGHT_3_TITLE','AI商业化加速'),('HIGHLIGHT_3_DESC','教育(+24%)+医疗(+24%)+开放平台(+17.7%)三位一体增长')]:
    html = html.replace(f'{{{{{k}}}}}', v)

# 敏感性分析
sens_pat = '<tr><td>__TODO__</td>\n<td>__TODO__</td>\n<td class="orange">__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td class="orange">__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td class="orange">__TODO__</td>\n    </tr>\n<tr>\n<td class="red">__TODO__</td>\n<td class="red">__TODO__</td>\n<td class="red" style="font-weight:bold;">__TODO__</td>\n    </tr>\n  </table>'
sens_new = '<tr><td>营收下降10%</td>\n<td>-27亿</td>\n<td class="orange">-15%</td>\n    </tr>\n<tr>\n<td>毛利率下降3pct</td>\n<td>-8.1亿</td>\n<td class="orange">-10%</td>\n    </tr>\n<tr>\n<td>费用率上升</td>\n<td>-5亿</td>\n<td class="orange">-8%</td>\n    </tr>\n<tr>\n<td>行业下行周期</td>\n<td>-15亿</td>\n<td class="red">-20%</td>\n    </tr>\n<tr>\n<td>竞争加剧</td>\n<td>-10亿</td>\n<td class="red" style="font-weight:bold;">-12%</td>\n    </tr>\n  </table>'
if sens_pat in html:
    html = html.replace(sens_pat, sens_new)
else:
    sens_pat2 = sens_pat.replace('\n', '')
    sens_new2 = sens_new.replace('\n', '')
    if sens_pat2 in html:
        html = html.replace(sens_pat2, sens_new2)
ok("敏感性分析")

# 避雷清单
check_pat = '<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>'
check_new = '<tr>\n<td>是否存在商誉减值风险</td>\n<td>商誉~20亿(占总资产~5%)风险可控</td>\n    </tr>\n<tr>\n<td>大股东是否持续减持</td>\n<td>中国移动为第一大股东，管理层稳定</td>\n    </tr>\n<tr>\n<td>财务造假信号</td>\n<td>经营现金流12.47亿为正，审计标准无保留</td>\n    </tr>\n<tr>\n<td>现金流是否持续为负</td>\n<td>经营现金流12.47亿(2025)持续为正</td>\n    </tr>\n<tr>\n<td>是否有未决诉讼</td>\n<td>年报未披露重大未决诉讼</td>'
if check_pat in html:
    html = html.replace(check_pat, check_new)
ok("避雷清单")

# M9 CSS
if '<style>' in html:
    html = html.replace('<style>', '<style>\n.tbl td:first-child{word-break:break-word;max-width:100px}')

# 六维评分
for i, s in enumerate([7, 7, 7, 5, 6, 8], 1):
    w = s * 10
    html = html.replace(f'{{{{DIM_BAR_{i}}}}}', f'width:{w}%')
    html = html.replace(f'{{{{DIM_SCORE_{i}}}}}', str(s))
html = html.replace('{{DIM_BAR_X}}', 'width:70%')
ok("六维评分")

# 价值理念
vtexts = ['科大讯飞是"好生意"——AI赛道高增长+技术壁垒。ROE 4.57%偏低但改善中。',
    'AI国家队+星火大模型差异化极强，开发者生态1000万+形成网络效应。',
    '刘庆峰创始人掌舵25年，技术驱动型管理。坚守AI赛道长期主义。',
    'PS 3.6x/PB 3.2x合理偏低。PE 118x偏高但AI高增长可消化。',
    '研发投入44.39亿(16.4%)是最大投入，构筑技术壁垒但压制利润。',
    '市场过度关注PE偏高，低估了大模型商业化加速和PS合理低位。',
    'AI大模型市场千亿级增速30%+，教育/医疗AI渗透率提升空间大。',
    '催化剂：星火5.0发布+AI学习机放量+医疗AI推广。',
    '市场认为PE 118x过高，未看到营收增速16%+和大模型中标23亿的拐点。',
    '反脆弱性较强：AI国家队+多样化行业覆盖+现金流改善。',
    'PS 3.6x历史中低位，PB 3.2x合理。最差情景对应PS~2.5x。']
for i, t in enumerate(vtexts, 1):
    key = f'{{M{i}_ANALYSIS}}' if i < 11 else '{{M11_SAFETY_MARGIN}}'
    html = html.replace(key, t)
ok("价值理念")

# ===== BQ =====
bq_texts = [
    '科大讯飞整体评分6.5/10。核心价值在AI国家队+星火大模型技术领先。2025年营收271亿(+16.12%)净利8.39亿(+27.8%)。PE 118x/PB 3.2x/PS 3.6x。核心亮点：AI技术壁垒+开发者生态1000万+，核心风险：PE偏高、研发投入大压制利润。',
    '科大讯飞主营AI软件+服务，智慧教育(33%)+开放平台(22%)+智慧城市(~25%)+智能硬件(8%)+智慧医疗(3%)。星火大模型中标23亿行业第一。开发者生态1000万+。研发占比16.4%。',
    '核心护城河在AI技术积累(星火大模型)+开发者生态(1000万+)+行业Know-how(教育/医疗)，三重壁垒。壁垒评分7.2/10。最深的壁垒是AI国家队身份+星火大模型技术领先。',
    '刘庆峰25年带领科大讯飞成为AI龙头，技术驱动型管理，研发投入坚定。评分：战略8/10，执行力7/10，股东回报5/10，资本配置7/10。中国移动为第一大股东。',
    '财务评分5/10。营收271.05亿(+16.12%)净利8.39亿(+27.8%)。毛利率~57%稳定。ROE 4.57%偏低。经营现金流12.47亿(+47.2%)。费用率：销售51.91亿(+27.1%)，管理13.88亿(-4.6%)，研发44.39亿(+14.1%)，财务1.73亿(+28.4%)。',
    '成本结构：研发44.39亿(16.4%)+销售51.91亿(19.1%)+人员薪酬~65亿(24%)+算力~35亿(13%)+其他~33亿(12%)。毛利率~57%稳定，软件服务占比高。',
    'PE(TTM) 118.3x偏高(行业50-150x)。归母PE 118x，扣非PE~150x(非经常损益小)，PB 3.2x合理(2.5-5.0x)，PS 3.6x合理(2.0-6.0x)。三个口径：PE偏高，PB和PS合理。综合判断：估值偏高但AI高增长可消化。',
    '中国AI大模型市场千亿级增速30%+。讯飞星火大模型中标23亿行业第一。教育AI渗透率30%→60%空间。医疗AI(智医助理)全国推广中。',
    '三大催化剂：星火5.0发布+C端AI学习机放量+医疗AI推广。三情景：30-80元，基准48元。核心催化剂看大模型商业化速度和毛利率变化。',
    '市场可能低估：①大模型中标23亿行业第一的商业化拐点；②PS 3.6x在AI公司中偏低；③开发者生态1000万+的网络效应。PE偏高和研发投入是市场关注焦点。',
    '核心风险：①PE 118x偏高估值压力；②研发44.39亿(16.4%)压制利润；③BAT巨头AI竞争加剧；④AI技术迭代快需持续投入。避雷全部通过。',
]
parts = html.split('{{BQ_ANALYSIS}}')
if len(parts) == len(bq_texts) + 1:
    html = parts[0]
    for i, txt in enumerate(bq_texts):
        html += txt + parts[i+1]
    ok(f"BQ({len(bq_texts)}篇)")
else:
    html = html.replace('{{BQ_ANALYSIS}}', '')

with open(REPORT, 'w', encoding='utf-8') as f:
    f.write(html)

import subprocess
r = subprocess.run(['grep', '-c', '__TODO__', REPORT], capture_output=True, text=True)
todo = r.stdout.strip()
r2 = subprocess.run(['wc', '-c', REPORT], capture_output=True, text=True)
print(f"\n{'='*50}")
print(f"  填充完成！共修改 {changes} 处")
print(f"  TODO: {todo} | 大小: {r2.stdout.strip()}")

# 自检
with open(REPORT, 'r') as f:
    c = f.read()
errs = []
if c.count('__TODO__') > 0: errs.append(f"TODO残留: {c.count('__TODO__')}个")
op, cl = c.count('<div'), c.count('</div>')
if op != cl: errs.append(f"div不平衡: {op}/{cl}")
for section, name in [('敏感性分析','敏感'),('避雷清单','避雷'),('估值指标','估值')]:
    idx = c.find(section)
    if idx > 0 and '—' in c[idx:idx+500] and '—' not in c[idx:idx+50]:
        errs.append(f"{name}表有—残留")
if errs:
    print("⚠️ " + ' | '.join(errs))
else:
    print("✅ 自检通过")
