# Experimental Reproduction Guide

> 基于论文 **"Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models"** (Neurocomputing, 2025) 的完整实验复现指南

## 1. 实验环境准备

### 1.1 依赖安装
```bash
pip install torch transformers
pip install openai tiktoken
pip install nltk bert-score rouge
pip install numpy pandas tqdm
pip install openpyxl  # 用于结果分析
```

### 1.2 数据准备
确保以下数据文件存在：
- `data/msc_dialogue/session_4/test.txt` - MSC Session 4测试数据
- `data/msc_dialogue/session_5/test.txt` - MSC Session 5测试数据  
- `data/carecall/carecall-memory_en_auto_translated.json` - CareCall数据
- `prompt.json` - 主要提示模板文件
- `data/msc_dialogue/prompts.json` - MSC数据集特定提示

### 1.3 API配置
```bash
export OPENAI_API_KEY="your-api-key"
```

## 2. 主要实验复现

### 2.1 核心方法：递归摘要 (LLM-Rsum)

**MSC数据集 - Session 5 (重点评估)**
```bash
# GPT-4 递归摘要
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode rsum \
    --model_name gpt-4o-2024-05-13 \
    --resp_temp 0 \
    --summ_temp 0 \
    --test_num 300 \
    --saving_dir save_msc

# GPT-3.5 递归摘要
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode rsum \
    --model_name gpt-3.5-turbo-0301 \
    --resp_temp 0 \
    --summ_temp 0 \
    --test_num 300 \
    --saving_dir save_msc
```

**MSC数据集 - Session 4**
```bash
python main_chatgpt.py \
    --dataset msc \
    --session_id 4 \
    --mode rsum \
    --model_name gpt-4o-2024-05-13 \
    --resp_temp 0 \
    --summ_temp 0 \
    --saving_dir save_msc
```

**CareCall数据集**
```bash
python main_chatgpt.py \
    --dataset carecall \
    --session_id 5 \
    --mode rsum \
    --model_name gpt-4o-2024-05-13 \
    --resp_temp 0 \
    --summ_temp 0 \
    --saving_dir save_carecall
```

### 2.2 基线方法对比

**1. 上下文完整方法 (Context-only)**
```bash
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode full \
    --model_name gpt-4o-2024-05-13 \
    --resp_temp 0 \
    --saving_dir save_msc
```

**2. 滑动窗口方法 (Window)**
```bash
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode window \
    --model_name gpt-4o-2024-05-13 \
    --window_size 2000 \
    --resp_temp 0 \
    --saving_dir save_msc
```

**3. 检索增强生成 (RAG)**
```bash
# BM25检索
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode rag \
    --model_name gpt-4o-2024-05-13 \
    --do_rag \
    --retrieval b25 \
    --topk 5 \
    --resp_temp 0 \
    --saving_dir save_msc

# DPR检索
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode rag \
    --model_name gpt-4o-2024-05-13 \
    --do_rag \
    --retrieval dpr \
    --topk 3 \
    --resp_temp 0 \
    --saving_dir save_msc
```

**4. 记忆库基线方法**
```bash
# MemoryBank
python main_llama.py \
    --operation infer \
    --mode rsum \
    --model_name memorybank \
    --dataset msc \
    --session_id 5 \
    --saving_dir save_msc

# MemoChat  
python main_llama.py \
    --operation infer \
    --mode rsum \
    --model_name memochat \
    --dataset msc \
    --session_id 5 \
    --saving_dir save_msc
```

### 2.3 本地模型实验

**LLaMA-2模型**
```bash
# LLaMA-2-7B
python main_llama.py \
    --operation infer \
    --mode rsum \
    --model_name llama2-7b-hf \
    --dataset msc \
    --session_id 5 \
    --test_batch_size 2 \
    --saving_dir save_msc

# LLaMA-2-13B
python main_llama.py \
    --operation infer \
    --mode rsum \
    --model_name llama2-13b-hf \
    --dataset msc \
    --session_id 5 \
    --test_batch_size 2 \
    --saving_dir save_msc
```

**长上下文模型**
```bash
# LongLoRA-8K
python main_llama.py \
    --operation infer \
    --mode rsum \
    --model_name llama2-7b-longlora-8k-ft \
    --dataset msc \
    --session_id 5 \
    --max_seq_length 8000 \
    --saving_dir save_msc
```

## 3. 消融实验

### 3.1 Few-shot ICL实验
```bash
# 无示例 (Zero-shot)
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode rsum \
    --model_name gpt-4o-2024-05-13 \
    --saving_dir save_msc

# 1-shot ICL
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode rsum \
    --model_name gpt-4o-2024-05-13 \
    --do_ict \
    --n_shot 1 \
    --saving_dir save_msc

# 3-shot ICL
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode rsum \
    --model_name gpt-4o-2024-05-13 \
    --do_ict \
    --n_shot 3 \
    --saving_dir save_msc
```

### 3.2 记忆质量对比
```bash
# 使用预测记忆 (Generated Memory)
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode rsum \
    --summary_type pred \
    --saving_dir save_msc

# 使用真实记忆 (Gold Memory)
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode sumgold \
    --summary_type gt \
    --saving_dir save_msc
```

### 3.3 互补性实验
```bash
# RAG + Recursive Summary
python main_chatgpt.py \
    --dataset msc \
    --session_id 5 \
    --mode rag_mem \
    --model_name gpt-4o-2024-05-13 \
    --do_rag \
    --retrieval b25 \
    --topk 5 \
    --saving_dir save_msc
```

## 4. 评估实验

### 4.1 自动评估
所有上述实验运行后会自动计算并保存以下指标：
- BLEU-1, BLEU-2, BLEU-3
- F1-Score
- Distinct-1, Distinct-2
- BERTScore (如果配置)

### 4.2 LLM-as-Judge评估
```bash
# GPT-4单模型评分 (1-100分)
python main_llama.py \
    --operation judge \
    --dataset msc \
    --session_id 5 \
    --model_name gpt-4o-2024-05-13 \
    --eval_file "infer_rsum_sid5.json" \
    --saving_dir save_msc

# GPT-4成对比较
python main_llama.py \
    --operation win \
    --dataset msc \
    --session_id 5 \
    --model_name gpt-4o-2024-05-13 \
    --saving_dir save_msc
```

### 4.3 人工评估准备
```bash
# 生成人工评估样本
python main_llama.py \
    --operation eval \
    --dataset msc \
    --session_id 5 \
    --saving_dir save_msc
```

## 5. 结果分析与复现验证

### 5.1 主要结果检查
运行实验后，检查以下关键结果文件：
- `save_msc/gpt-4o-2024-05-13/infer_rsum_sid5.json` - 递归摘要预测结果
- `save_msc/gpt-4o-2024-05-13/infer_full_sid5.json` - 全上下文基线结果
- `save_msc/gpt-4o-2024-05-13/infer_window_sid5.json` - 窗口基线结果

### 5.2 期望结果指标
根据论文，期望复现的主要指标：

**MSC Session 5自动评估:**
- ChatGPT-Rsum F1: ~32.5
- ChatGPT-Full F1: ~29.8  
- ChatGPT-Window F1: ~30.1
- BLEU-1/2改善: 递归摘要 > 基线方法

**人工与LLM评估:**
- GPT-4评分: 递归摘要在连贯性和一致性上优于基线
- 成对比较: 递归摘要胜率 > 50%

**记忆质量:**
- 生成记忆F1 > 真实记忆F1
- 错误率 < 5% (虚构信息比例)

### 5.3 结果验证脚本
```bash
# 批量运行核心实验
bash run_rsum.sh

# 批量评估
python -c "
import json
import os
from utils.evaluation import evaluate_corpus

# 加载结果并计算指标
results_dir = 'save_msc/gpt-4o-2024-05-13'
for method in ['rsum', 'full', 'window']:
    file_path = f'{results_dir}/infer_{method}_sid5.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        preds = [v['prediction'] for v in data.values()]
        labels = [v['label'] for v in data.values()]
        metrics = evaluate_corpus(preds, labels)
        print(f'{method.upper()}: {metrics}')
"
```

## 6. 实验注意事项

### 6.1 重要参数设置
- **Temperature = 0**: 确保结果可复现
- **Session ID**: 重点测试Session 4和5 (最长上下文)
- **Test数量**: 论文使用300个测试样本进行评估
- **记忆长度**: 限制在200 tokens以内

### 6.2 计算资源需求
- **API模型**: GPT-4/3.5需要API配额
- **本地模型**: LLaMA-13B需要>16GB GPU内存
- **实验时间**: 完整实验套件需要数小时至数天

### 6.3 故障排除
- 如果缺少`prompt.json`，参考`dataset.py`第10行和第24行创建
- API限流时适当降低并发或添加重试机制
- 本地模型路径需要根据实际安装位置修改

## 7. 扩展实验

### 7.1 更多数据集
```bash
# 其他Session测试
for sid in 2 3 4; do
    python main_chatgpt.py --dataset msc --session_id $sid --mode rsum --model_name gpt-4o-2024-05-13
done
```

### 7.2 超参数敏感性
```bash
# 不同摘要长度
for size in 100 200 300; do
    python main_chatgpt.py --dataset msc --session_id 5 --mode rsum --summary_size $size
done

# 不同检索topk
for k in 3 5 10; do  
    python main_chatgpt.py --dataset msc --session_id 5 --mode rag --topk $k --do_rag
done
```

通过以上完整的实验流程，可以系统性地复现论文中的所有主要实验和结果。