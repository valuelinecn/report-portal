# 报告生成流程 v39

## 一、准备阶段
```
1. 复制 blank-template-v39.ckpt → reports/{股票代码}.html
2. 拉取财务数据：
   python3 scripts/fetch_financial_data.py reports/{股票代码}.html {股票代码}
3. 拉取K线数据：
   python3 scripts/gen_kline.py sh{股票代码}  (上交所)
   python3 scripts/gen_kline.py sz{股票代码}  (深交所)
4. 移动K线文件到 kline/ 目录
```

## 二、填充阶段
```
5. 填充基础信息：公司名、代码、评分、标签（从API+你提供）
6. 填充财务表（API已自动拉取）
7. 填充K线图（JSON已就位，JS自动加载）
8. 填写各区块分析内容：
   - 从API已知的数据直接填
   - 我能搜到的先搜索再填
   - 搜不到的标记出来问用户
```

## 三、检查阶段
```
9. 必查项目：
   □ 占位符残留 = 0
   □ div平衡（<div>数量 = </div>数量）
   □ JS语法通过（node --check）
   □ 股票代码一致性
   □ 空单元格 = 0
   □ 财务表三色着色（pos/neg/warn）
   □ 各区块完整性（s0-s13 + s-mcap + s-financial）
10. 跑审计脚本：bash scripts/auto-audit.sh reports/{文件}
```

## 四、确认与推送
```
11. 输出来源清单（数据出处）
12. 用户确认内容准确性
13. 用户确认后推送：
    git add reports/{文件} kline/{文件} index.html
    git commit -m "feat: 公司名报告(股票代码)"
    git push
```
