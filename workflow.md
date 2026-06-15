# 企业研究报告生成标准流程

## 第零步：环境检查
1. 研报客：`node ~/.hermes/skills/yanbaoke/scripts/search.mjs "测试" -n 1`
2. fin-table API 可用
3. 空白模板就绪
4. 用户发的年报/季报PDF在工作目录

---

## 第一步：准备
复制 `blank-template.html` → `reports/股票代码.html`

---

## 第二步：数据采集（每项数据严格按此顺序）

### 第1层 — 年报PDF
年报的董事会报告/管理层讨论与分析章节已包含：
- 管理层名单与任职时间
- 分业务收入与占比
- 核心财务数据（主要会计数据表 + 三张报表）
- **行业概况与竞争格局**
- **市场地位与市占率**
- **可比公司财务对比**
- **政策影响分析**
- **风险提示与应对措施**
- 研发投入与研发管线
- 公司战略与下一年经营计划

所有能从年报获取的数据，必须先看年报。

### 第2层 — 季报PDF（如有）
- 最新季度营收/净利润/扣非/毛利率
- 最新经营数据更新

### 第3层 — fin-table API
- 历史多年度财务数据补充（营收、利润、毛利率、净利率、ROE、EPS、OCF等）
- 结构化跨年对比

### 第4层 — 研报客 search
- 仅补充年报和fin-table未覆盖的内容
- 不要跳过年报直接去研报客找行业数据和竞争格局
- 研报客没有企业自己的年报和季报，官方数据才是基准

### 第5层 — 问用户
对照模板所有 `{{...}}` 占位符检查三个来源是否覆盖
→ 仍缺失的：一次性汇总问用户

---

## 第三步：写填充脚本

```python
# 1. 读模板
# 2. 替换基础信息
html = html.replace('{{STOCK_CODE}}', '...')

# 3. 用 replace_table() 整块替换表格
#    从 <h3>表格标题</h3> 到 </table> 整段匹配+替换
def replace_table(html, title_text, new_html):
    import re
    pattern = rf'<h3[^>]*>{re.escape(title_text)}</h3>.*?</table>'
    return re.sub(pattern, new_html, html, flags=re.DOTALL)

# 4. 逐个替换 BQ
#    re.sub 找到每个 <div class="bq">...</div> 按M1-M10顺序填入唯一结论

# 5. 清理剩余 {{...}} 占位符
```

---

## 第四步：验证清单

```
[ ] 占位符 = 0                      → grep -oP '\{\{[^}]+\}\}' | wc -l
[ ] div平衡（opens==closes）         → re.findall('<div(?:\s|>)') vs '</div>'
[ ] BQ全部唯一                      → set对比12个bq内容
[ ] 无旧公司残留                     → grep 其他公司名
[ ] JS语法通过                      → node --check 提取的script块
[ ] 所有 <table> 含 class="tbl"     → grep '<table'
[ ] 无空单元格                       → 肉眼检查
[ ] 文件大小合理                     → ls -lh
```

---

## 第五步：本地预览（推前必须做）

```bash
python3 -m http.server 端口号
```
用户打开 `http://localhost:端口号/reports/xxx.html` 确认
→ 表格渲染正确，BQ内容在正确板块，无乱码

---

## 第六步：推 test 分支

```bash
git checkout test && git merge main
git add reports/xxx.html
git commit -m "feat(test): XXX报告初版"
git push origin test
git checkout main
```

---

## 第七步：用户确认后上线

```bash
bash scripts/deploy-to-main.sh "XXX报告"
```

---

---

## 第九步：执行审计（每次交付时附上）

报告完成后，逐条回答以下清单，标注 ✅ 已执行 / ❌ 未执行 / ⚠️ 部分执行：

```
第零步：环境检查
[ ] 研报客技能可用
[ ] fin-table API 可用
[ ] 空白模板就绪
[ ] 用户年报/季报PDF在工作目录

第一步：准备
[ ] 从blank-template.html复制，无旧公司残留

第二步：数据采集
[ ] 第1层：年报PDF已提取（含行业分析/竞争格局/市占率/风险等）
[ ] 第2层：季报PDF已提取
[ ] 第3层：fin-table API已调用
[ ] 第4层：研报客已搜索补充
[ ] 第5层：数据缺口已汇总问用户

第三步：填充
[ ] 基础信息占位符已替换
[ ] 表格用replace_table()整块替换
[ ] BQ按M1-M10顺序逐个填入唯一结论
[ ] 剩余{{...}}已清理

第四步：验证
[ ] 占位符 = 0
[ ] div平衡
[ ] BQ全部唯一
[ ] 无旧公司残留
[ ] JS语法通过
[ ] 所有<table>含class="tbl"

第五步：预览
[ ] 本地http.server已启动
[ ] 用户确认渲染正常

第六步：推送
[ ] 推test分支

第七步：上线
[ ] 用户确认后deploy-to-main.sh

第八步：来源清单
[ ] 每个指标标注了出处
```
