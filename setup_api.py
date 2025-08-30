#!/usr/bin/env python3
"""
自动设置 OpenAI API 密钥的工具脚本
"""
import argparse
import os
import re
from pathlib import Path

def setup_api_key(api_key):
    """在所有需要的文件中设置API密钥"""
    
    files_to_update = [
        "chatgpt/robot.py",
        "chatgpt/direct_generation.py",
        "utils/robot.py", 
        "utils/llm_judge.py",
        "memo_chat/gpt_memochat.py",
        "memorybank/gpt_memorybank.py",
        "memorybank/question_memorybank.py", 
        "memorybank/retrieval_memorybank.py",
        "memoryrecu/gpt_recu.py"
    ]
    
    updated_files = []
    
    for file_path in files_to_update:
        full_path = Path(file_path)
        
        if not full_path.exists():
            print(f"⚠️  文件不存在: {file_path}")
            continue
            
        try:
            # 读取文件内容
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换API密钥
            patterns = [
                r'api_key\s*=\s*["\']x+["\']',  # api_key = "xxxxxx"
                r'api_key\s*=\s*["\'][^"\']*["\']',  # api_key = "any-key"
                r'OpenAI\(api_key\s*=\s*["\']x+["\']\)',  # OpenAI(api_key="xxxxxx")
                r'OpenAI\(api_key\s*=\s*["\'][^"\']*["\']\)'  # OpenAI(api_key="any-key")
            ]
            
            replacements = [
                f'api_key = "{api_key}"',
                f'api_key = "{api_key}"', 
                f'OpenAI(api_key="{api_key}")',
                f'OpenAI(api_key="{api_key}")'
            ]
            
            original_content = content
            
            for pattern, replacement in zip(patterns, replacements):
                content = re.sub(pattern, replacement, content)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(file_path)
                print(f"✅ 更新: {file_path}")
            else:
                print(f"🔍 检查: {file_path} (无需更新)")
                
        except Exception as e:
            print(f"❌ 错误处理 {file_path}: {e}")
    
    return updated_files

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
    parser.add_argument("--env-var", action="store_true", help="同时设置环境变量")
    
    args = parser.parse_args()
    
    print("🔧 开始设置 OpenAI API 密钥...")
    print("=" * 50)
    
    # 更新代码文件中的API密钥
    updated_files = setup_api_key(args.api_key)
    
    print("\n" + "=" * 50)
    print(f"📊 总结:")
    print(f"✅ 成功更新 {len(updated_files)} 个文件")
    
    if args.env_var:
        print("\n🌍 设置环境变量...")
        setup_environment_variable(args.api_key)
    
    print("\n🎉 API 密钥设置完成!")
    print("\n📝 接下来的步骤:")
    print("1. 如果设置了环境变量，请重启终端或运行: source ~/.bashrc")
    print("2. 运行第一个实验: python run_first_experiment.py")
    print("3. 或手动运行: python main_chatgpt.py --dataset msc --session_id 5 --mode rsum")

if __name__ == "__main__":
    main()