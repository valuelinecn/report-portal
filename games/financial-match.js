// ===== 财报指标连连看 · 题库 =====
// 三级难度，每级4对（8张卡片），左→右匹配

const MATCH_DATA = {
  初级: {
    desc: '基础财务指标 · 看懂公司赚钱能力',
    pairs: [
      { term: 'ROE<br><small>净资产收益率</small>', def: '净利润 ÷ 净资产<br>衡量股东每一块钱能赚回多少利润<br><span class="mhint">合理区间：15%以上为优秀</span>' },
      { term: '毛利率<br><small>Gross Margin</small>', def: '(营收 − 营业成本) ÷ 营收<br>衡量产品的溢价能力和行业地位<br><span class="mhint">茅台91%+ vs 制造业20-30%</span>' },
      { term: '净利率<br><small>Net Margin</small>', def: '净利润 ÷ 营收<br>衡量公司最终的盈利水平<br><span class="mhint">中际旭创22.7%，越稳定越好</span>' },
      { term: '资产负债率<br><small>Debt Ratio</small>', def: '总负债 ÷ 总资产<br>衡量公司的财务杠杆和偿债风险<br><span class="mhint">通常40-60%较健康，过高有风险</span>' },
    ]
  },
  中级: {
    desc: '估值与效率指标 · 判断贵还是便宜',
    pairs: [
      { term: 'PE<br><small>市盈率</small>', def: '股价 ÷ 每股收益 (EPS)<br>衡量市场愿意为每一块钱利润支付的价格<br><span class="mhint">茅台20.7x，中际旭创21.5x</span>' },
      { term: 'PB<br><small>市净率</small>', def: '股价 ÷ 每股净资产<br>衡量市场对公司资产的溢价程度<br><span class="mhint">大于1说明有溢价，小于1可能被低估</span>' },
      { term: '股息率<br><small>Dividend Yield</small>', def: '每股股息 ÷ 股价<br>衡量持有股票的现金回报率<br><span class="mhint">茅台3.2%，长期稳定分红是好事</span>' },
      { term: '营业利润率<br><small>Operating Margin</small>', def: '营业利润 ÷ 营收<br>衡量主营业务的真实盈利能力<br><span class="mhint">排除了非经常性损益的影响</span>' },
    ]
  },
  高级: {
    desc: '进阶拆解指标 · 深入分析公司质量',
    pairs: [
      { term: '资产周转率<br><small>Asset Turnover</small>', def: '营收 ÷ 总资产<br>衡量每一块钱资产能产生多少营收<br><span class="mhint">越高说明运营效率越好</span>' },
      { term: '权益乘数<br><small>Equity Multiplier</small>', def: '总资产 ÷ 净资产<br>衡量公司使用了多少财务杠杆<br><span class="mhint">也就是1 ÷ (1 − 资产负债率)</span>' },
      { term: 'EPS<br><small>每股收益</small>', def: '净利润 ÷ 总股本<br>衡量每一股能分到多少利润<br><span class="mhint">持续增长是好信号，警惕稀释</span>' },
      { term: '自由现金流<br><small>FCF</small>', def: '经营现金流 − 资本支出<br>巴菲特最看重的指标——公司真正可自由支配的钱<br><span class="mhint">有利润没现金=假繁荣</span>' },
    ]
  }
}
