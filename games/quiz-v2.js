// ===== 投资人格解密 · 二级市场四维度模型 =====
// 4维度 × 2极性 = 16种交易人格
// 每题五级评分: 非常像我(+2) / 像我(+1) / 一般(0) / 不像我(-1) / 完全不像我(-2)

// ===== 人格类型数据 =====
const PERSONALITY_TYPES = {
  // ── TJ组: 理性计划派 ──
  'ISTJ': {
    dims: 'I S T J', icon: '🏛️', name: '稳健价投者', sub: '数据理性计划 · 巴菲特型',
    motto: '「慢慢变富，才是最快的路。」',
    desc: '你是典型的价值投资践行者。你依赖数据做决策，严格遵守交易纪律，不追热点、不情绪化。你的持仓可能看起来很\"无聊\"——但正是这种无聊带来了长期稳定的回报。你像一座灯塔，在市场的惊涛骇浪中始终坚定。',
    good: '熊市中你活最久，复利效应最明显，长期胜率极高',
    bad: '可能错过成长股的大行情，对行业变革反应偏慢',
    advice: '偶尔审视组合中是否有被时代淘汰的\"价值陷阱\"，保持适度开放',
    who: '沃伦·巴菲特、本杰明·格雷厄姆、约翰·涅夫'
  },
  'INTJ': {
    dims: 'I N T J', icon: '🎯', name: '策略布局者', sub: '逻辑理性计划 · 机构策略型',
    motto: '「胜兵先胜而后求战。」',
    desc: '你是全局思考型的投资者。你喜欢提前研究行业大趋势，做自上而下的布局。你不在乎短期的市场噪音，因为你有自己的逻辑框架和判断标准。你的交易计划像作战地图一样清晰——什么时候进、什么时候出、为什么，全都提前想好了。',
    good: '擅长抓住大级别行情，布局前瞻性强，回撤控制好',
    bad: '过于自信逻辑框架，可能忽视数据层面的警示信号',
    advice: '逻辑再好也要用数据验证，定期检查你的假设是否还成立',
    who: '查理·芒格、霍华德·马克斯、乔治·索罗斯'
  },
  'ESTJ': {
    dims: 'E S T J', icon: '📊', name: '量化执行者', sub: '数据理性执行 · 量化/波段型',
    motto: '「系统不撒谎，情绪才撒谎。」',
    desc: '你是一个系统化交易者。你相信数据信号胜过主观判断——当条件触发就执行，不犹豫、不纠结。你擅长波段操作和量化策略，你的交易记录像实验室记录一样干净。你可能不是市场上最聪明的，但你一定是最守纪律的。',
    good: '执行力极强，胜率稳定，适合程序化/半程序化交易',
    bad: '系统失效时缺乏应变能力，可能在大行情转折处反复被收割',
    advice: '定期复盘优化你的交易系统，极端行情下允许人工干预',
    who: '詹姆斯·西蒙斯、汤姆·巴索'
  },
  'ENTJ': {
    dims: 'E N T J', icon: '🐉', name: '龙头猎手', sub: '逻辑理性执行 · 龙头战法型',
    motto: '「不做龙头的交易都是浪费行情。」',
    desc: '你是天生的趋势交易者。你擅长识别市场主线、抓住龙头股，并且在主升浪中敢于重仓。你杀伐果断——发现机会时不犹豫，发现错误时不留恋。你的反应速度和执行力让大多数人望尘莫及。你的问题不是赚不到钱，而是赚够了之后能不能守住。',
    good: '牛市中收益爆炸，抓主线能力一流，止损果断',
    bad: '震荡市中反复打脸，大赚之后容易自负导致回撤',
    advice: '牛市赚到的钱要用熊市策略来保护——学会空仓也是能力',
    who: '杰西·利弗莫尔、徐翔'
  },
  // ── FP组: 情绪灵活派 ──
  'ISFP': {
    dims: 'I S F P', icon: '🎪', name: '直觉交易者', sub: '数据情绪灵活 · 短线散户型',
    motto: '「我感觉它要涨。」',
    desc: '你依赖盘感和直觉做交易。你看K线、看成交量、凭\"感觉\"做买卖决定。你爱做T、爱短线、小赚就跑、套了就扛。你不是没有赚钱的时候——但你赚的是小钱，亏的是大钱。你的问题不在智商，在纪律。',
    good: '盘感敏锐，小行情中也能找到交易机会',
    bad: '没有系统，情绪化交易，赚小亏大是常态',
    advice: '建立简单的交易规则（比如：-8%必须止损），用规则代替感觉',
    who: '林园'
  },
  'INFP': {
    dims: 'I N F P', icon: '🌈', name: '信仰持仓者', sub: '逻辑情绪灵活 · 情怀价投型',
    motto: '「我相信这家公司会改变世界。」',
    desc: '你买股票是因为\"相信\"——你相信这家公司的故事、相信它的创始人、相信它终将伟大。你在公司困难时不会卖出，反而可能加仓。你的信仰有时会带来超额回报——但有时也会让你在泡沫破裂时粉身碎骨。',
    good: '拿得住十倍股，信仰坚定的人往往能吃到最肥美的段落',
    bad: '容易陷入\"价值陷阱\"，为信仰支付过高代价',
    advice: '信仰也需要锚点——设定逻辑证伪条件，破了就走',
    who: '凯茜·伍德、彼得·林奇'
  },
  'ESFP': {
    dims: 'E S F P', icon: '🌿', name: '情绪跟风者', sub: '数据情绪社交 · 新手散户型',
    motto: '「这次不一样！」',
    desc: '你刚入市不久，或者虽然入市很久但一直被情绪牵着走。你喜欢热闹——群里推荐什么你就买什么，看到涨了就追，看到跌了就慌。你经常在高位接盘、在低位割肉。好消息是——每个人都是从这里开始的，这不是终点。',
    good: '市场好时也能赚钱，社交能力强，信息获取快',
    bad: '追涨杀跌、没有独立判断、容易被收割',
    advice: '先停止交易，读三本书：《聪明的投资者》《彼得·林奇的成功投资》《股票大作手回忆录》',
    who: '追涨杀跌的新股民'
  },
  'ENFP': {
    dims: 'E N F P', icon: '🔥', name: '题材猎妖者', sub: '逻辑情绪社交 · 题材炒作型',
    motto: '「风口来了，猪都会飞。」',
    desc: '你是题材炒作的活跃分子。你对新概念、新热点有着敏锐的嗅觉——从元宇宙到AI，从低空经济到固态电池，你总是第一时间冲进去。你喜欢研究\"故事\"，也擅长把故事讲给别人听。你偶尔能大赚一笔，但长期看回撤惊人。',
    good: '抓题材能力一流，市场情绪感知力极强',
    bad: '换票太频繁、手续费高、长期收益率不稳定',
    advice: '用10%的资金做题材练手，90%做有逻辑的配置',
    who: '赵老哥'
  },
  // ── TP组: 理性灵活派 ──
  'INTP': {
    dims: 'I N T P', icon: '🔬', name: '量化研究者', sub: '逻辑理性灵活 · 量化/研究型',
    motto: '「回测过了，胜率63%。」',
    desc: '你是一个研究型投资者。你享受搭建模型、回测策略、分析数据的乐趣。你不太关注短期交易——你更在乎策略本身是否有效。你的交易频率不高，但每笔都有据可查。你的弱点可能是过度优化——在历史数据上完美，在未来市场上失效。',
    good: '策略思维强，不情绪化，长期可复制',
    bad: '容易过度拟合，实盘和回测差距大，执行时犹豫',
    advice: '简单策略往往比复杂策略更鲁棒——减少参数，增加容错',
    who: '詹姆斯·西蒙斯、肯·格里芬'
  },
  'ISTP': {
    dims: 'I S T P', icon: '⚡', name: '短线狙击手', sub: '数据理性灵活 · 短线高手型',
    motto: '「进场、交易、离场——不带走一片云彩。」',
    desc: '你是纯粹的交易者。你看盘快、反应更快。你关注的是量价关系和盘口资金——不关心公司叫什么名字，只关心它今天能不能涨。你止损之快让大多数人瞠目结舌，也正因为如此你才能在这个残酷的游戏中活下来。',
    good: '风险控制极好，回撤小，适应各种市场环境',
    bad: '格局不够大，容易卖飞牛股，大牛市跑不赢持有者',
    advice: '适当放大交易周期——有的利润用\"持有\"来赚比\"交易\"更轻松',
    who: '瑞鹤仙、方新侠'
  },
  'ENTP': {
    dims: 'E N T P', icon: '🔄', name: '轮动套利者', sub: '逻辑理性灵活 · 套利/轮动型',
    motto: '「永远满仓，永远热泪盈眶——不过换了个票。」',
    desc: '你是市场中的多面手。你不执着于某一个行业或某一只股票——你的能力在于发现不同板块之间的性价比差异，及时切换。你像一只灵活的猫，总能在市场变化中找到新的落脚点。你的问题不是找不到机会——而是每个机会你都不想错过。',
    good: '适应性强，牛熊都能赚钱，资金使用效率高',
    bad: '过度交易，容易因精力分散而错过重仓大机会',
    advice: '学会\"舍\"——放弃80%的机会，只做最确定的20%',
    who: '大卫·泰珀、章盟主'
  },
  'ESTP': {
    dims: 'E S T P', icon: '📈', name: '事件驱动者', sub: '数据理性灵活 · 波段/事件型',
    motto: '「有事件就有波动，有波动就有机会。」',
    desc: '你善于利用消息面和事件驱动做交易。财报季、政策发布、行业会议——这些时间节点就是你的战场。你技术面功底扎实，纪律尚可，反应速度一流。你最大的敌人是自己的冲动——一个好的机会出现时，你往往等不及确认就冲了进去。',
    good: '事件交易胜率高，信息处理速度快，交易节奏好',
    bad: '容易在假突破中受伤，耐心不够，左侧交易容易止损',
    advice: '等右侧确认再入场虽然少赚几个点，但胜率大幅提升',
    who: '卡尔·伊坎、冯柳'
  },
  // ── FJ组: 情绪计划派 ──
  'INFJ': {
    dims: 'I N F J', icon: '🎭', name: '纠结价投者', sub: '逻辑情绪计划 · 理想与现实',
    motto: '「计划得很好，执行起来...下次一定。」',
    desc: '你有着优秀的投资理念和逻辑框架——你知道什么是对的。问题是，你很难把计划执行到底。看好一只股票却不敢重仓，计划持有三年却三个月就卖了，止损线设了却不执行。你不是不懂——你是做不到。',
    good: '投资认知水平高，学习能力强，方向感好',
    bad: '知行不合一，计划与执行严重脱节',
    advice: '减少决策频率——一年只做3-5次交易，每次严格执行书面计划',
    who: '但斌'
  },
  'ISFJ': {
    dims: 'I S F J', icon: '🛡️', name: '稳健纠结者', sub: '数据情绪计划 · 保守与焦虑',
    motto: '「稳稳的幸福...吗？」',
    desc: '你追求稳健——你买蓝筹、买高股息、买大家都说好的公司。但你有一个致命的问题：你设了止损却不执行，赚了小钱就跑，亏了却死扛。你本质上厌恶风险，但你的行为却在不断制造风险——因为你不肯认错。',
    good: '选股偏稳健，整体组合风险不高',
    bad: '止损执行差，一次大亏可能吃掉多年收益',
    advice: '止损单不要手动执行——用条件单自动触发，别给自己犹豫的机会',
    who: '追求稳健却舍不得止损的价值投资者'
  },
  'ENFJ': {
    dims: 'E N F J', icon: '📢', name: '市场布道者', sub: '逻辑情绪社交 · 群主/大V型',
    motto: '我觉得这个方向大家可以关注一下。',
    desc: '你是一个乐于分享的人。你可能经营着一个投资群、一个有影响力的社交账号，或者身边总有人找你聊股票。你对市场方向有自己独到的见解，但你最大的挑战是你的观点会影响别人，而别人的反馈又会影响你。',
    good: '信息渠道广，学习动力强，能影响他人',
    bad: '被粉丝或群友情绪反噬，为维持人设而做出错误交易',
    advice: '公开分享和私人交易要分开——你的交易不需要对任何人负责',
    who: '段永平（大道无形我有型）'
  },
  'ESFJ': {
    dims: 'E S F J', icon: '🐢', name: '跟风稳健派', sub: '数据情绪社交 · 大V跟随者',
    motto: '「跟着大V走，准没错...吧？」',
    desc: '你是一个谨慎的跟随者。你不敢自己选股——你觉得专业的事应该交给专业的人。你跟着大V买、跟着机构买、跟着朋友买。你赚过钱，但不明白为什么赚；你亏过钱，也不知道为什么亏。你不是没有判断力——你只是不相信自己的判断力。',
    good: '跟随优质信息来源，长期看能跟上市场平均收益',
    bad: '没有独立判断能力，被带偏时毫无防范',
    advice: '从\"抄作业\"到\"独立分析\"——每跟一笔，写清楚买入理由和卖出条件',
    who: '跟投大V配置的基金投资者'
  }
};

// ===== 超简短版定义（给结果页顶部用） =====
const TYPE_SHORT = {
  'ISTJ': { dims:'I S T J', icon:'🏛️', name:'稳健价投者', sub:'巴菲特型 · 重仓蓝筹长期持有' },
  'INTJ': { dims:'I N T J', icon:'🎯', name:'策略布局者', sub:'机构策略型 · 自上而下提前布局' },
  'ESTJ': { dims:'E S T J', icon:'📊', name:'量化执行者', sub:'量化波段型 · 数据信号驱动交易' },
  'ENTJ': { dims:'E N T J', icon:'🐉', name:'龙头猎手', sub:'龙头战法型 · 敢重仓果断止损' },
  'ISFP': { dims:'I S F P', icon:'🎪', name:'直觉交易者', sub:'短线散户型 · 凭感觉做T' },
  'INFP': { dims:'I N F P', icon:'🌈', name:'信仰持仓者', sub:'情怀价投型 · 信仰长期持有' },
  'ESFP': { dims:'E S F P', icon:'🌿', name:'情绪跟风者', sub:'新手散户型 · 追涨杀跌' },
  'ENFP': { dims:'E N F P', icon:'🔥', name:'题材猎妖者', sub:'题材炒作型 · 追新概念换票' },
  'INTP': { dims:'I N T P', icon:'🔬', name:'量化研究者', sub:'量化研究型 · 回测搭系统' },
  'ISTP': { dims:'I S T P', icon:'⚡', name:'短线狙击手', sub:'短线高手型 · 快进快出' },
  'ENTP': { dims:'E N T P', icon:'🔄', name:'轮动套利者', sub:'套利轮动型 · 多品种切换' },
  'ESTP': { dims:'E S T P', icon:'📈', name:'事件驱动者', sub:'事件驱动型 · 量价突破' },
  'INFJ': { dims:'I N F J', icon:'🎭', name:'纠结价投者', sub:'知行不合一 · 计划好执行难' },
  'ISFJ': { dims:'I S F J', icon:'🛡️', name:'稳健纠结者', sub:'保守焦虑型 · 止损不执行' },
  'ENFJ': { dims:'E N F J', icon:'📢', name:'市场布道者', sub:'大V群主型 · 爱分享易被反噬' },
  'INFJ': { dims:'I N F J', icon:'🎭', name:'纠结价投者', sub:'知行不合一 · 计划好执行难' },
  'ENFJ': { dims:'E N F J', icon:'📢', name:'市场布道者', sub:'大V群主型 · 爱分享易被反噬' },
  'ESFJ': { dims:'E S F J', icon:'🐢', name:'跟风稳健派', sub:'大V跟随者 · 抄作业无主见' }
};

// ===== 题库 =====
// d: 维度 (EI/SN/TF/JP), p: +1正向该维度, q: 题目
// 评分: 非常像我+2 / 像我+1 / 一般0 / 不像我-1 / 完全不像我-2
// score加给对应维度: d值+'Score'
const QUIZ_NEW = [
  // ── E/I 维度：信息来源 ──
  { d:'EI', p:+1, q:'我经常从微信群、论坛、社交媒体获取股票信息' },
  { d:'EI', p:-1, q:'我更喜欢独自研究财报和公告，很少和别人讨论持仓' },
  { d:'EI', p:+1, q:'市场情绪高涨时我交易更频繁，冷清时我也没兴趣' },
  { d:'EI', p:-1, q:'别人的观点很难影响我的买卖决策' },
  { d:'EI', p:+1, q:'我喜欢在投资社区分享我的分析和看法' },
  { d:'EI', p:-1, q:'独处复盘和阅读研报让我觉得最充实' },

  // ── S/N 维度：分析视角 ──
  { d:'SN', p:+1, q:'我买股票首先看PE、PB、股息率、ROE这些财务指标' },
  { d:'SN', p:-1, q:'我更看重公司未来5-10年的成长空间，哪怕现在盈利一般' },
  { d:'SN', p:+1, q:'财报数据和历史业绩比行业故事更能说服我' },
  { d:'SN', p:-1, q:'我经常思考行业变革趋势和政策方向带来的投资机会' },
  { d:'SN', p:+1, q:'我偏爱成熟稳定、盈利确定性强的公司' },
  { d:'SN', p:-1, q:'我容易被颠覆性的新技术和新商业模式吸引' },

  // ── T/F 维度：决策方式 ──
  { d:'TF', p:+1, q:'我严格按止损纪律执行，亏损到线就卖，不犹豫' },
  { d:'TF', p:-1, q:'持仓亏损时我很难卖出，总想着"迟早会涨回来的" ' },
  { d:'TF', p:+1, q:'市场涨跌不影响我的睡眠和日常生活' },
  { d:'TF', p:-1, q:'看到朋友圈或群里别人赚钱了，我会感到焦虑并想跟风' },
  { d:'TF', p:+1, q:'我做投资决策主要依靠逻辑分析，而不是"感觉"' },
  { d:'TF', p:-1, q:'我会因为"心里不踏实"而卖出一只基本面没问题的股票' },

  // ── J/P 维度：交易节奏 ──
  { d:'JP', p:+1, q:'每次交易前我都会提前写好买入和卖出的计划' },
  { d:'JP', p:-1, q:'我经常在盘中临时决定买卖，计划赶不上变化' },
  { d:'JP', p:+1, q:'我喜欢长期持有，不频繁换票' },
  { d:'JP', p:-1, q:'我享受盘中随时应变、灵活交易的快感' },
  { d:'JP', p:+1, q:'我会设定明确的持仓周期和交易条件' },
  { d:'JP', p:-1, q:'我的操作计划经常被临时的想法打乱' }
];

// ===== 固定维度定义 =====
const DIM_LABELS = {
  EI: { name:'信息来源', left:'I 内研型', right:'E 外信型',
    descL:'独研财报，不信消息，安静专注',
    descR:'混群看帖，听大V，越聊越来劲' },
  SN: { name:'分析视角', left:'S 数据派', right:'N 逻辑派',
    descL:'盯PE/PB/股息，求确定性',
    descR:'看趋势/模式/未来，敢为故事买单' },
  TF: { name:'决策方式', left:'T 理性脑', right:'F 情绪脑',
    descL:'按系统交易，止损强，涨跌不影响',
    descR:'容易焦虑，重仓睡不着，死扛跟风' },
  JP: { name:'交易节奏', left:'J 计划型', right:'P 灵活型',
    descL:'提前计划、严格执行、不临时起意',
    descR:'盘中决策、爱做T、享受随机应变' }
};

// ===== 测验逻辑 =====
var quizState = null;

function startQuiz() {
  document.getElementById('quizIntro').style.display = 'none';
  document.getElementById('quizScreen').style.display = 'block';
  document.getElementById('quizResult').style.display = 'none';

  quizState = {
    idx: 0,
    answers: [],    // 每项: {qIdx, score}  score: -2,-1,0,1,2
    scores: { EI:0, SN:0, TF:0, JP:0 }
  };

  document.getElementById('quizTotal').textContent = QUIZ_NEW.length;
  showQuestion(0);
}

function showQuestion(idx) {
  var total = QUIZ_NEW.length;
  var item = QUIZ_NEW[idx];
  var dimKey = item.d;
  var dimInfo = DIM_LABELS[dimKey];

  // Update progress
  document.getElementById('quizNum').textContent = idx + 1;
  document.getElementById('quizProgressBar').style.width = ((idx / total) * 100) + '%';

  // Build question HTML
  var dimLabel = item.p > 0 ? dimInfo.right : dimInfo.left;
  var dimSide = item.p > 0 ? 'E/SN/TF/JP'.indexOf(dimKey[dimKey.length-1]) : 'I/SN/TF/JP'.indexOf(dimKey[0]);
  var dimColor = dimKey === 'EI' ? '#4fc3f7' : dimKey === 'SN' ? '#f0c040' : dimKey === 'TF' ? '#e04040' : '#8bc34a';

  var html = '<div style="display:flex;align-items:center;gap:6px;margin-bottom:10px">';
  html += '<span class="tg" style="background:'+dimColor+'20;color:'+dimColor+';border:1px solid '+dimColor+'40">'+dimInfo.name+' · '+dimLabel+'</span>';
  html += '</div>';
  html += '<div class="quiz-q">' + item.q + '</div>';

  // Options (5-level Likert)
  var opts = [
    { label: '非常像我', val: 2 },
    { label: '像我', val: 1 },
    { label: '一般', val: 0 },
    { label: '不像我', val: -1 },
    { label: '完全不像我', val: -2 }
  ];
  html += '<div class="quiz-opts">';
  for (var i = 0; i < opts.length; i++) {
    var sel = (quizState.answers[idx] && quizState.answers[idx].score === opts[i].val) ? ' selected' : '';
    html += '<button class="quiz-opt' + sel + '" onclick="selectOpt(' + idx + ',' + opts[i].val + ',this)">' + opts[i].label + '</button>';
  }
  html += '</div>';

  document.getElementById('quizQ').innerHTML = html;

  // Show/hide next button
  var hasAnswer = quizState.answers[idx] !== undefined;
  document.getElementById('quizNextBtn').style.display = hasAnswer ? 'block' : 'none';
  document.getElementById('quizExplain').style.display = 'none';
}

function selectOpt(qIdx, score, btn) {
  // Guard: prevent double-click / re-selection
  if (quizState.answers[qIdx] !== undefined) return;

  // Save answer
  quizState.answers[qIdx] = { qIdx: qIdx, score: score };

  // Update visual
  var parent = btn.parentElement;
  var btns = parent.querySelectorAll('.quiz-opt');
  btns.forEach(function(b) { b.classList.remove('selected'); });
  btn.classList.add('selected');

  // Disable buttons briefly to prevent rapid re-clicks during transition
  btns.forEach(function(b) { b.disabled = true; });

  // Auto advance to next question after a brief pause (user sees their selection)
  setTimeout(function() {
    // Re-enable (though DOM will be replaced by showQuestion)
    btns.forEach(function(b) { b.disabled = false; });
    nextQuestion();
  }, 350);
}

function nextQuestion() {
  var idx = quizState.idx;
  var total = QUIZ_NEW.length;

  // Save score to dimension totals
  var ans = quizState.answers[idx];
  if (ans) {
    var item = QUIZ_NEW[idx];
    quizState.scores[item.d] = (quizState.scores[item.d] || 0) + (ans.score * item.p);
  }

  quizState.idx++;
  if (quizState.idx >= total) {
    // Calculate and show result
    showResult();
    return;
  }
  showQuestion(quizState.idx);
}

// ===== 结果计算 =====
function showResult() {
  document.getElementById('quizScreen').style.display = 'none';
  document.getElementById('quizResult').style.display = 'block';

  var s = quizState.scores;
  // 每个维度: score > 0 → 右边的极性, score < 0 → 左边的极性
  var typeCode = '';
  typeCode += s.EI > 0 ? 'E' : 'I';
  typeCode += s.SN > 0 ? 'S' : 'N';
  typeCode += s.TF > 0 ? 'T' : 'F';
  typeCode += s.JP > 0 ? 'J' : 'P';

  // 强度 (0-100)
  var intensity = {};
  intensity.EI = Math.min(100, Math.round(Math.abs(s.EI) / 12 * 100));
  intensity.SN = Math.min(100, Math.round(Math.abs(s.SN) / 12 * 100));
  intensity.TF = Math.min(100, Math.round(Math.abs(s.TF) / 12 * 100));
  intensity.JP = Math.min(100, Math.round(Math.abs(s.JP) / 12 * 100));

  var type = PERSONALITY_TYPES[typeCode];
  if (!type) type = PERSONALITY_TYPES['INFP']; // fallback

  var short = TYPE_SHORT[typeCode] || { icon:'🧬', name:typeCode, sub:'' };

  // Fill result
  document.getElementById('resultTypeIcon').textContent = short.icon;
  document.getElementById('resultTypeName').textContent = short.name;
  document.getElementById('resultTypeSub').textContent = short.sub + ' · ' + typeCode;
  document.getElementById('resultMotto').textContent = type.motto;

  var descHtml = '<div style="font-size:13px;color:var(--t5);line-height:1.8">' + type.desc + '</div>';
  descHtml += '<div style="margin-top:12px">';
  descHtml += '<div style="font-size:12px;color:var(--accent);font-weight:600;margin-bottom:6px">✅ 优势</div>';
  descHtml += '<div style="font-size:12px;color:var(--t5);margin-bottom:10px">' + type.good + '</div>';
  descHtml += '<div style="font-size:12px;color:#f44336;font-weight:600;margin-bottom:6px">⚠️ 劣势</div>';
  descHtml += '<div style="font-size:12px;color:var(--t5);margin-bottom:10px">' + type.bad + '</div>';
  descHtml += '</div>';
  document.getElementById('resultTypeDesc').innerHTML = descHtml;

  // Four dimensions display
  var dimKeys = ['EI','SN','TF','JP'];
  var dimColors = {'EI':'#4fc3f7','SN':'#f0c040','TF':'#e04040','JP':'#8bc34a'};
  var dimHtml = '';
  for (var i = 0; i < dimKeys.length; i++) {
    var k = dimKeys[i];
    var info = DIM_LABELS[k];
    var score = s[k] || 0;
    var pct = Math.min(100, Math.round(Math.abs(score) / 12 * 100));
    var leftLabel = info.left;
    var rightLabel = info.right;
    var leftPct = score <= 0 ? pct : 0;
    var rightPct = score > 0 ? pct : 0;
    var active = score > 0 ? 'R' : 'L';
    var c = dimColors[k];
    dimHtml += '<div style="margin:8px 0">';
    dimHtml += '<div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:4px">';
    dimHtml += '<span style="color:' + (active==='L'?c:'var(--m5)') + ';font-weight:' + (active==='L'?'600':'400') + '">' + leftLabel + '</span>';
    dimHtml += '<span style="color:var(--m5);font-size:10px">' + info.name + '</span>';
    dimHtml += '<span style="color:' + (active==='R'?c:'var(--m5)') + ';font-weight:' + (active==='R'?'600':'400') + '">' + rightLabel + '</span>';
    dimHtml += '</div>';
    dimHtml += '<div style="display:flex;height:6px;background:var(--b1);border-radius:3px;overflow:hidden">';
    dimHtml += '<div style="width:' + leftPct + '%;background:' + c + ';border-radius:3px 0 0 3px;transition:width .5s"></div>';
    dimHtml += '<div style="width:' + (100-leftPct-rightPct) + '%;background:transparent"></div>';
    dimHtml += '<div style="width:' + rightPct + '%;background:' + c + ';border-radius:0 3px 3px 0;transition:width .5s"></div>';
    dimHtml += '</div>';
    dimHtml += '<div style="font-size:10px;color:var(--m5);margin-top:2px">' + info.descL + ' · ' + info.descR + '</div>';
    dimHtml += '</div>';
  }
  document.getElementById('resultDims').innerHTML = dimHtml;

  document.getElementById('resultAdvice').innerHTML = type.advice;
  document.getElementById('resultWho').textContent = type.who;

  // Update progress to 100%
  document.getElementById('quizProgressBar').style.width = '100%';
}

function resetQuiz() {
  document.getElementById('quizResult').style.display = 'none';
  startQuiz();
}
