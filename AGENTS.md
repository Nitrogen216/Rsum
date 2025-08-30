# Repository Guidelines

## Project Structure & Module Organization
- `chatgpt/`: API-based baselines (ChatGPT, direct generation, RAG helpers).
- `llama/`: Local model utilities (tokenizer, dataloaders, generation).
- `memorybank/`, `memo_chat/`: Memory-centric baseline implementations.
- `utils/`: Evaluation and retrieval helpers (e.g., `evaluation.py`, `rag.py`).
- `data/`: Input datasets (keep small; avoid committing large/raw assets).
- `save_msc/`: Experiment outputs grouped by model (logs, JSON, summaries).
- Top-level scripts: `main_chatgpt.py`, `main_llama.py`, `run_first_experiment.py`, `verify_datasets.py`, `run_rsum.sh`, `run_rag.sh`, `setup_api.py`.

## Build, Test, and Development Commands
- Environment: Python 3.8+ (recommend venv). Install core deps:
  ```bash
  pip install torch transformers openai tiktoken nltk bert-score rouge numpy pandas tqdm openpyxl
  ```
- Configure API (use .env):
  ```bash
  # Option A: create .env in project root
  echo "OPENAI_API_KEY=sk-..." > .env

  # Option B: helper script writes .env for you
  python setup_api.py --api-key "sk-..."

  # Optional: also export in your shell (persistent)
  # python setup_api.py --api-key "sk-..." --env-var
  ```
- Quick smoke test:
  ```bash
  python run_first_experiment.py
  ```
- Core ChatGPT run (small):
  ```bash
  python main_chatgpt.py --dataset msc --session_id 5 --mode rsum --test_num 5
  ```
- Local-model baseline / RAG:
  ```bash
  bash run_rsum.sh
  bash run_rag.sh
  ```
- Data sanity check:
  ```bash
  python verify_datasets.py
  ```

## Coding Style & Naming Conventions
- Python, 4-space indentation; follow PEP 8.
- Naming: snake_case for files/functions, PascalCase for classes.
- Prefer f-strings and type hints in new code.
- Expose CLI flags via `config.get_args()`; reuse existing option names.

## Testing Guidelines
- No formal unit-test suite; validate via script runs and metrics.
- Outputs live under `save_msc/<model>/` (e.g., `infer_rsum_sid5.json`).
- For PRs, include a small run (e.g., `--test_num 5`) and key metrics from `utils/evaluation.py`.

## Commit & Pull Request Guidelines
- Commits: short, imperative subject; optional scope (e.g., "llama: fix dataloader").
- PRs: description, motivation, commands used, sample logs/metrics, affected flags/files; link issues. Do not commit secrets, large data, or generated artifacts.

## Security & Configuration Tips
- Never hardcode API keys. Place them in `.env` (ignored by git) or export `OPENAI_API_KEY`.
- Keep `data/` minimal; add large/raw files to `.gitignore`.
- Note GPU/VRAM needs when adding models or increasing `--max_seq_length`.

## Notes
- The codebase loads `OPENAI_API_KEY` via `utils/env.py` (minimal `.env` loader). See `.env.example`.
- `.env` is ignored by git (see `.gitignore`).
