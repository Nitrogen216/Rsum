# Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models

This repository contains the official implementation of the paper:

[**Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models**](https://arxiv.org/pdf/2308.15022)  
*Qingyue Wang, Yanhe Fu, Yanan Cao, Shuai Wang, Zhiliang Tian, Liang Ding*  
*Neurocomputing, 2025*

---

## 🚀 Quickstart

### 1) Environment
- Python 3.8+
- Install core deps:
  ```bash
  pip install torch transformers openai tiktoken nltk bert-score rouge numpy pandas tqdm openpyxl
  ```

### 2) API Setup (OpenAI)
- Create a `.env` file in the project root (recommended):
  ```bash
  echo "OPENAI_API_KEY=sk-..." > .env
  ```
- Or use the helper to write `.env` for you:
  ```bash
  python setup_api.py --api-key "sk-..."        # writes .env
  # optional: also persist to your shell
  # python setup_api.py --api-key "sk-..." --env-var
  ```
- See `.env.example` for the expected format. Do not commit real keys.

### 3) Run a Smoke Test
```bash
python run_first_experiment.py
```

### 4) Minimal ChatGPT Run
```bash
python main_chatgpt.py --dataset msc --session_id 5 --mode rsum --test_num 5
```

### 5) Local Baselines / RAG
```bash
bash run_rsum.sh
bash run_rag.sh
```

### 6) Data Sanity Check
```bash
python verify_datasets.py
```

## 📄 Citation
If you find this work useful, please cite our paper:

```bibtex
@article{wang2025recursive,
  title={Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models},
  author={Wang, Qingyue and Fu, Yanhe and Cao, Yanan and Wang, Shuai and Tian, Zhiliang and Ding, Liang},
  year={2025},
  journal={Neurocomputing}
}
