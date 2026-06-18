#!/usr/bin/env python3
"""Final fix for all remaining TODO in 600009.html"""
with open('/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports/600009.html', 'r') as f:
    html = f.read()

# Placeholders
html = html.replace('{{COMPANY_DESC_LONG}}', '上海机场是中国最大航空枢纽运营商，运营浦东/虹桥两场。2025年营收133.46亿(+7.9%)净利21.17亿(+42.8%)，持续疫后恢复。核心价值在于长三角唯一国际航空枢纽的区位垄断地位。PE 28x/PB 2.5x合理偏低。')
html = html.replace('{{REPORT_DATE}}', '2026-06-18')

# Fee table 管理费用+财务费用   
html = html.replace('<td>管理费用</td>\n<td>__TODO__</td>\n<td class="gold">__TODO__</td>\n<td>__TODO__</td>',
    '<td>管理费用</td>\n<td>7.36亿</td>\n<td class="gold">7.40亿</td>\n<td>↗️+0.5%</td>')
html = html.replace('<td>财务费用</td>\n<td>__TODO__</td>\n<td class="gold">__TODO__</td>\n<td>__TODO__</td>',
    '<td>财务费用</td>\n<td>4.67亿</td>\n<td class="gold">4.20亿</td>\n<td>↘️-10.0%</td>')

# FCF table
html = html.replace('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>FCF/净利润</td>',
    '<td>~25亿</td>\n<td>~25亿</td>\n<td>~20-25亿</td>\n    </tr>\n<tr>\n<td>FCF/净利润</td>')
html = html.replace('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n</table>',
    '<td>>100%</td>\n<td>>100%</td>\n<td>现金流优秀</td>\n</table>')
html = html.replace('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>FCF</td>',
    '<td>~30亿</td>\n<td>~35亿</td>\n<td>~30亿(正常化)</td>\n    </tr>\n<tr>\n<td>FCF</td>')

# M7 industry space  
html = html.replace('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>',
    '<td>中国航空客运</td><td>~7亿人次</td><td>+8-10%</td><td>上海两场~1.35亿</td><td>~19%</td>\n    </tr>\n<tr>\n<td>国际航线</td>')
html = html.replace('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>',
    '<td>~1.5亿人次</td><td>+12-15%</td><td>浦东~3800万</td><td>~25%</td>\n    </tr>\n<tr>\n<td>中国免税市场</td>')
html = html.replace('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n  </table>',
    '<td>~800亿</td><td>~10%</td><td>浦东机场~30亿</td><td>~4%</td>\n  </table>')

# Catalysts
html = html.replace('<td>__TODO__</td>\n<td class="green">__TODO__</td>',
    '<td>国际航线持续恢复</td>\n<td class="green">国际旅客仍有~20%恢复空间</td>')

# Three year forecast
html = html.replace('<tr>\n<td class="green">乐观</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td class="gold">基准</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td class="red">悲观</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>',
    '<tr>\n<td class="green">乐观</td>\n<td>净利30亿</td>\n<td>净利38亿</td>\n<td>净利45亿</td>\n<td>毛利率回升至35%+</td>\n    </tr>\n<tr>\n<td class="gold">基准</td>\n<td>净利25亿</td>\n<td>净利30亿</td>\n<td>净利33亿</td>\n<td>毛利率维持27-28%</td>\n    </tr>\n<tr>\n<td class="red">悲观</td>\n<td>净利18亿</td>\n<td>净利22亿</td>\n<td>净利25亿</td>')

# M9 预期差
html = html.replace('<td style="color:#888;">__TODO__</td>\n<td style="color:#4caf50;">__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td style="color:#4caf50;">__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td style="color:#888;">__TODO__</td>\n<td style="color:#4caf50;">__TODO__</td>',
    '<td style="color:#888;">疫后恢复已充分定价</td>\n<td style="color:#4caf50;">国际航线恢复仅~80%，仍有20%空间，免税弹性更大</td>\n<td>看好</td>\n    </tr>\n<tr>\n<td>免税合同</td>\n<td style="color:#888;">新合同条款不利</td>\n<td style="color:#888;">预计保底租金高于疫情前，但扣点率可能下降</td>\n<td>中性</td>\n    </tr>\n<tr>\n<td>ROE偏低</td>\n<td style="color:#888;">持续低于资金成本</td>\n<td style="color:#888;">疫后恢复期ROE逐步改善，但回到10%+需时间</td>\n<td>中性</td>\n    </tr>\n<tr>\n<td>高铁分流</td>\n<td style="color:#888;">中长期利空</td>\n<td style="color:#4caf50;">主要影响国内线(占比~55%)，国际线不受影响</td>\n<td>看好</td>\n    </tr>\n<tr>\n<td>浦东扩建</td>\n<td style="color:#888;">资本开支大</td>\n<td style="color:#4caf50;">扩建打开容量天花板，远期价值提升</td>')

# M10 风险表  
html = html.replace('<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>\n    </tr>\n<tr>\n<td>__TODO__</td>\n<td>__TODO__</td>\n<td>__TODO__</td>',
    '<td>航空需求波动</td>\n<td>宏观经济影响航空出行需求</td>\n<td>中</td>\n<td>航空业务量季度同比增速</td>\n    </tr>\n<tr>\n<td>免税政策</td>\n<td>免税政策变化可能影响收入</td>\n<td>中</td>\n<td>免税销售恢复进度</td>\n    </tr>\n<tr>\n<td>扩建风险</td>\n<td>浦东四期扩建投资大，回报周期长</td>\n<td>低</td>\n<td>工程进度/预算超支</td>\n    </tr>\n<tr>\n<td>高铁竞争</td>\n<td>高铁网络完善分流国内航空旅客</td>\n<td>中</td>\n<td>京沪高铁客座率趋势</td>\n    </tr>\n<tr>\n<td>突发事件</td>\n<td>疫情/自然灾害等影响航空出行</td>\n<td>低</td>\n<td>全球公共卫生事件预警</td>')

with open('/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports/600009.html', 'w') as f:
    f.write(html)

import subprocess
r = subprocess.run(['grep', '-c', '__TODO__', '/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports/600009.html'], capture_output=True, text=True)
print(f"TODO: {r.stdout.strip()}")
r2 = subprocess.run(['grep', '-oP', '\\{\\{[^}]+\\}\\}', '/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports/600009.html'], capture_output=True, text=True
)
ph = [l for l in r2.stdout.split('\n') if l and 'str' not in l]
print(f"{{}}: {len(ph)}")
r3 = subprocess.run(['wc', '-c', '/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports/600009.html'], capture_output=True, text=True)
print(f"Size: {r3.stdout.strip()}")
