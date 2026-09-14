# ghgStorylinesRAG 使用引导

## 1. 当前目标

第一阶段围绕CAP 2023–2027建立可追溯数据库，区分EU法律文件、27国的28份
战略计划、具体interventions、计划预算与实际支出、实施产出与最终结果。
LLM只解释非结构化文本；国家数、金额合计和指标计算优先由Pandas完成。

## 2. 环境准备

PyCharm解释器选择：

`E:\TUM-PhD\Proposal_new idea\LLM+RAG\ghgStorylinesRAG\.venv\Scripts\python.exe`

项目终端运行：

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python scripts\smoke_test_ollama.py
```

预期结果是包含政策工具、日期、行业和减排目标的JSON。

## 3. 检查现有CAP工作簿

两份已下载工作簿位于`data/cap/raw/xlsx/`：

```powershell
python scripts\inspect_cap_workbooks.py
```

先记录sheet、行数、列名和代码表，再编写确定性的字段映射。

## 4. 登记与下载来源

所有来源先加入`data/cap/source_registry.csv`。至少记录来源ID、标题、URL、
文件类型、辖区、发布日期、本地路径和状态。优先级为：官方XLSX、官方PDF、
官方HTML、二手材料。`documents.py`提供基础下载和解析函数。

## 5. 使用Qwen提取一份文档

在PyCharm将`src`标记为Sources Root，或在终端运行：

```powershell
$env:PYTHONPATH="$PWD\src"
```

然后在Python脚本中调用：

```python
from pathlib import Path
from ghg_storylines_rag.pipeline import extract_file

output = extract_file(
    source_id="EU-2021-2115",
    path=Path("data/cap/raw/pdf/regulation-2021-2115.pdf"),
    source_url="https://eur-lex.europa.eu/eli/reg/2021/2115/oj/eng",
)
print(output)
```

输出写入`data/cap/extracted/<source_id>.jsonl`，保留URL、页码、模型名、
提示词版本和证据原文。

## 6. 质量控制

第一轮只处理EU概览以及德国、法国、荷兰、爱尔兰、西班牙五个案例，人工
核验至少100条记录。重点检查计划金额与实际支出、目标与实现结果、金额
单位、政策版本，以及evidence能否支持字段值。

## 7. 后续实现顺序

查看代码中的实施提示：

```powershell
rg -n "TODO\(CAP-RAG\)" .
```

建议依次完成：

1. 两份XLSX的列映射与规范化；
2. 官方来源批量下载和版本记录；
3. PDF章节/表格感知分块与OCR；
4. Qwen JSON失败重试、缓存和证据校验；
5. 生成legal acts、plans、interventions、budgets、outputs五张表；
6. 建立人工标注集并评估字段准确率；
7. 加入BGE-M3、BM25和向量数据库；
8. 与排放、生产、价格和天气面板匹配。

## 8. Git同步

```powershell
git pull --ff-only
git status
git add .
git commit -m "Build initial EU CAP extraction structure"
git push
```

不要提交`.env`、`.venv`、下载原文件或任何包含凭据的JSON。

## 9. 旧项目

原JRC/EMM灾害项目位于`legacy/`，不会被新管线导入。它仅用于参考旧有
storyline、知识图谱和验证逻辑；确认新管线稳定前不建议永久删除。
