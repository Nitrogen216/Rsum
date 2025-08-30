# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository implements "Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models" (Neurocomputing, 2025). It provides a complete framework for reproducing the paper's recursive summarization method for long-term dialogue memory.

## Core Architecture

### Entry Points
- `main_chatgpt.py`: Main implementation for GPT models (GPT-3.5, GPT-4)
- `main_llama.py`: Main implementation for LLaMA and other local models
- `config.py`: Central configuration with all experimental parameters

### Algorithm Implementation
The recursive summarization pipeline is implemented in `main_chatgpt.py`:
- `update_summary()` (lines 12-26): Memory iteration component - recursively generates M_i from session S_i and prior memory M_{i-1}
- `update_response()` (lines 28-44): Memory-based response component - generates response r_t from current context C_t using latest memory M_N
- `summary_all()` (lines 79-140): End-to-end Algorithm 1 implementation

### Data Flow
1. **Preprocessing**: `dataloader.py` handles MSC and CareCall dataset loading with session splitting
2. **Dataset Classes**: `dataset.py` provides specialized datasets (RSumDataset, MSCDataset, RAGDataset, SumDataset)
3. **Evaluation**: `utils/evaluation.py` implements F1, BLEU, BERTScore, and distinct-N metrics

### Baseline Methods
- **Memory-based**: `memorybank/` (MemoryBank), `memo_chat/` (MemoChat)
- **Retrieval-based**: `utils/rag.py` with BM25/DPR support
- **LLM Judge**: `utils/llm_judge.py` for GPT-4 evaluation

## Common Commands

### Running Experiments

**Core Method (Recursive Summarization):**
```bash
# MSC Session 5 with GPT-4
python main_chatgpt.py --dataset msc --session_id 5 --mode rsum --model_name gpt-4o-2024-05-13

# LLaMA models
python main_llama.py --operation infer --mode rsum --model_name llama2-7b-hf --session_id 5
```

**Baseline Comparisons:**
```bash
# Context-only baseline
python main_chatgpt.py --dataset msc --session_id 5 --mode full --model_name gpt-4o-2024-05-13

# Window baseline
python main_chatgpt.py --dataset msc --session_id 5 --mode window --model_name gpt-4o-2024-05-13

# RAG baseline
python main_chatgpt.py --dataset msc --session_id 5 --mode rag --do_rag
```

**Evaluation:**
```bash
# LLM-as-Judge evaluation
python main_llama.py --operation judge --session_id 5

# Pairwise comparison
python main_llama.py --operation win --session_id 5
```

**Ablation Studies:**
```bash
# Few-shot ICL
python main_chatgpt.py --mode rsum --do_ict --n_shot 3

# RAG + Memory combination
python main_chatgpt.py --mode rag_mem --do_rag
```

### Using Shell Scripts
```bash
# Run recursive summarization experiments
bash run_rsum.sh

# Generate summaries
bash summarize.sh
```

## Key Configuration Parameters

### Core Settings (config.py)
- `--mode`: Experimental mode (`rsum`, `full`, `window`, `rag`, `rag_mem`)
- `--dataset`: Dataset choice (`msc`, `carecall`)
- `--session_id`: Session number (focus on 4-5 for longest context)
- `--model_name`: LLM backbone (`gpt-4o-2024-05-13`, `llama2-7b-hf`, etc.)

### Memory Parameters
- `--summary_size 200`: Maximum memory summary length
- `--window_size 2000`: Context window size
- `--resp_temp 0`: Response generation temperature (0 for reproducibility)
- `--summ_temp 0`: Summary generation temperature

### Evaluation Settings
- `--test_num 300`: Number of test dialogues
- `--topk`: Retrieval top-k (3 or 5)
- `--operation`: Task type (`infer`, `judge`, `win`, `eval`)

## Data Requirements

### Expected Data Structure
- MSC data: `data/msc_dialogue/session_{session_id}/test.txt`
- CareCall data: `data/carecall/carecall-memory_en_auto_translated.json`
- Prompts: `prompt.json` (main), `data/msc_dialogue/prompts.json`

### Missing Files Setup
If `prompt.json` is missing, create it with memory update and response generation prompts. See `dataset.py` lines 10, 24 for expected format.

## Model Path Configuration

### LLaMA Models (main_llama.py lines 47-91)
Update model paths in `build_model()` function:
- LLaMA-2-7B: Update path in line 52
- LLaMA-2-13B: Update path in line 49
- Long context models: Update paths in lines 57-58

### API Models
Configure API keys for GPT models in environment or `chatgpt/robot.py`.

## Output and Results

### Result Files
- Predictions: `save_{dataset}/{model_name}/{operation}_{mode}_sid{session_id}.json`
- Summaries: `save_{dataset}/{model_name}/{operation}_sum_sid{session_id}.json`
- Logs: `save_{dataset}/{model_name}/{operation}_{mode}_sid{session_id}_log.txt`

### Evaluation Metrics
Results include F1, BLEU-1/2/3, BERTScore, Distinct-1/2. Use `utils/evaluation.py:evaluate_corpus()` for comprehensive evaluation.

## Implementation Notes

### Recursive Memory Algorithm
The core algorithm follows this pattern:
1. Initialize M_0 = "Empty"
2. For each session S_i: M_i = update_summary(M_{i-1}, S_i)  
3. At response time: r_t = update_response(M_N, C_t)

### Prompt Engineering
Memory update prompts should:
- Analyze previous memory for existing information
- Extract new personality traits from current session
- Merge information while avoiding redundancy
- Limit output to ≤20 sentences

Response prompts should:
- Extract relevant traits from memory
- Generate contextually appropriate responses
- Fall back to natural conversation if no relevant traits

### Temperature Settings
All experiments use temperature=0 for both memory generation and response generation to ensure reproducibility across runs.