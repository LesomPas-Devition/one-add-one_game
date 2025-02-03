
# BotBattle - 基于遗传算法的双手对战AI

*该README文件由[DeepSeek](https://github.com/deepseek-ai/DeepSeek-R1)撰写并结构化*

---

## 📜 项目简介
这是一个结合遗传算法与策略优化的双人对战AI项目。两个Bot通过模10加法攻击对方双手，目标是将对方双手数值同时变为0。项目包含**AI训练系统**、**对战逻辑核心**和**用户交互界面**，展现了强化学习在游戏策略中的实践。

---

## 🎮 功能特性

### 🧠 AI核心
- **动态策略矩阵**：9x9概率矩阵驱动攻击选择
- **遗传进化**：种群竞争、两点交叉、概率变异
- **自适应决策**：ε-greedy策略平衡探索与利用

### 🕹️ 游戏系统
- 模10加法战斗机制 `(a+b)%10`
- 双人对战模式（Bot vs Bot / Human vs Bot）
- 实时战斗日志与操作可视化
- 先手顺序调整（随机/Bot优先/玩家优先）

### 🛠️ 训练体系
- 种群规模与迭代次数可配置
- 适应度函数 `fitness = 12 - log2(step)`
- 变异保护机制（保留最优个体）

---

## ⚙️ 快速开始

### 环境要求
- Python 3.10+
- 无额外依赖

### 安装步骤
暂时不提供安装


### 🏃 运行指南
| 模式                | 命令                  | 说明                     |
|---------------------|-----------------------|--------------------------|
| 玩家对战模式        | `python main.py`      | 启动交互式命令行界面     |
| 训练模式            | `python training.py`  | 生成data_collection.json |
| 自定义Bot对战       | 参考`bot.py`示例代码  | 支持策略矩阵注入         |

---

## 📂 文件结构
```text
src/
├── data/                  # 训练数据存储
│   └── data_collection.json
├── bot/
│    ├── bot.py                 # 核心Bot逻辑
│    ├── training.py            # 遗传算法训练
│    ├── utils.py               # 数据工具类
│    └── errors.py              # 自定义异常
└── user/
      └── main.py                # 用户交互入口

```

---

## 🧪 训练配置
在`training.py`中调整训练参数：
```python
population_num = 512    # 种群规模
times = 1024            # 迭代次数
variant_probability = 0.1  # 变异概率
```

---

## 🤝 贡献指南
1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 发起Pull Request

---

## 📄 许可协议
本项目采用 [GPL-3.0 license](https://www.gnu.org/licenses/gpl-3.0.txt)，欢迎用于学习与研究。商业使用请联系作者授权。

---

## ✨ 项目优势
- **模块化设计**：各组件低耦合高内聚
- **高效训练**：两点交叉法加速收敛
- **可解释性**：策略矩阵可视化分析
- **鲁棒性**：200步强制终止机制

---

*本README由AI助手通过深度分析项目代码架构后生成，完整呈现项目核心价值与使用场景。建议配合代码注释获得最佳理解体验。*
