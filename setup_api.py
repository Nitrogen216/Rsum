#!/usr/bin/env python3
"""
自动设置 OpenAI API 密钥的工具脚本

现在默认把密钥写入项目根目录的 .env 文件：
  OPENAI_API_KEY=sk-...

代码会从 .env 或环境变量中读取密钥，不再在源码中硬编码。
"""
import argparse
import os
import re
from pathlib import Path


def write_dotenv(api_key: str, dotenv_path: str = ".env") -> Path:
    """Write OPENAI_API_KEY to a .env file in the project root."""
    path = Path(dotenv_path)
    try:
        if path.exists():
            # Update or append OPENAI_API_KEY
            lines = path.read_text(encoding="utf-8").splitlines()
            found = False
            new_lines = []
            for line in lines:
                if line.strip().startswith("OPENAI_API_KEY="):
                    new_lines.append(f"OPENAI_API_KEY={api_key}")
                    found = True
                else:
                    new_lines.append(line)
            if not found:
                new_lines.append(f"OPENAI_API_KEY={api_key}")
            path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        else:
            path.write_text(f"OPENAI_API_KEY={api_key}\n", encoding="utf-8")
        print(f"✅ 已写入 {dotenv_path} (OPENAI_API_KEY)")
    except Exception as e:
        print(f"❌ 无法写入 {dotenv_path}: {e}")
    return path

def setup_environment_variable(api_key):
    """设置环境变量"""
    
    shell_config_files = [
        os.path.expanduser("~/.bashrc"),
        os.path.expanduser("~/.zshrc"), 
        os.path.expanduser("~/.bash_profile")
    ]
    
    export_line = f'export OPENAI_API_KEY="{api_key}"\n'
    
    for config_file in shell_config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                
                if 'OPENAI_API_KEY' not in content:
                    with open(config_file, 'a') as f:
                        f.write(f'\n# OpenAI API Key for Rsum project\n{export_line}')
                    print(f"✅ 添加环境变量到: {config_file}")
                else:
                    print(f"🔍 {config_file} 已包含 OPENAI_API_KEY")
                    
            except Exception as e:
                print(f"❌ 无法更新 {config_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="设置 OpenAI API 密钥")
    parser.add_argument("--api-key", required=True, help="你的 OpenAI API 密钥")
    parser.add_argument("--env-var", action="store_true", help="同时设置 shell 环境变量 (~/.zshrc 等)")
    
    args = parser.parse_args()
    
    print("🔧 开始设置 OpenAI API 密钥...")
    print("=" * 50)

    # 写入 .env
    write_dotenv(args.api_key)
    
    if args.env_var:
        print("\n🌍 设置 shell 环境变量...")
        setup_environment_variable(args.api_key)
    
    print("\n🎉 API 密钥设置完成!")
    print("\n📝 接下来的步骤:")
    print("1. 将 .env 加入版本控制忽略 (已在 .gitignore 配置)")
    print("2. 运行第一个实验: python run_first_experiment.py")
    print("3. 或手动运行: python main_chatgpt.py --dataset msc --session_id 5 --mode rsum")

if __name__ == "__main__":
    main()
