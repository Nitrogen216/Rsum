#!/usr/bin/env python3
"""
运行第一个递归摘要实验
"""
import os
import subprocess
import sys
import json
from pathlib import Path

def check_api_key():
    """检查API密钥是否已设置"""
    
    # 检查环境变量
    env_key = os.getenv('OPENAI_API_KEY')
    if env_key and env_key != 'your-actual-api-key-here':
        print("✅ 发现环境变量中的API密钥")
        return True
    
    # 检查代码文件中的密钥
    robot_file = Path("chatgpt/robot.py")
    if robot_file.exists():
        with open(robot_file, 'r') as f:
            content = f.read()
            if 'api_key = "xxxxxx"' not in content and 'api_key="xxxxxx"' not in content:
                print("✅ 发现代码文件中的API密钥")
                return True
    
    print("❌ 未找到有效的API密钥")
    print("请先运行: python setup_api.py --api-key 'your-openai-api-key'")
    return False

def check_dependencies():
    """检查依赖是否已安装"""
    
    required_packages = ['openai', 'transformers', 'torch', 'nltk', 'rouge']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {missing_packages}")
        print("请运行: pip install openai transformers torch nltk rouge")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def run_experiment(dataset="msc", session_id=5, mode="rsum", model_name="gpt-4o-2024-08-06"):
    """运行第一个实验"""
    
    print(f"\n🚀 开始运行实验:")
    print(f"   数据集: {dataset}")
    print(f"   Session: {session_id}")
    print(f"   模式: {mode}")
    print(f"   模型: {model_name}")
    print("=" * 50)
    
    # 构建命令
    cmd = [
        "python", "main_chatgpt.py",
        "--dataset", dataset,
        "--session_id", str(session_id), 
        "--mode", mode,
        "--model_name", model_name,
        "--test_num", "5",  # 先运行少量样本测试
        "--resp_temp", "0",
        "--summ_temp", "0"
    ]
    
    try:
        # 运行实验
        print("运行命令:", " ".join(cmd))
        print("\n📊 实验输出:")
        print("-" * 30)
        
        result = subprocess.run(cmd, capture_output=False, text=True, check=True)
        
        print("-" * 30)
        print("✅ 实验完成!")
        
        # 检查输出文件
        output_dir = f"save_{dataset}"
        expected_file = f"{output_dir}/{model_name}/infer_{mode}_sid{session_id}.json"
        
        if os.path.exists(expected_file):
            print(f"📄 结果已保存到: {expected_file}")
            
            # 显示部分结果
            with open(expected_file, 'r') as f:
                results = json.load(f)
            
            print(f"📈 生成了 {len(results)} 个预测结果")
            
            # 显示第一个例子
            if results:
                first_key = list(results.keys())[0]
                first_result = results[first_key]
                print(f"\n🔍 第一个例子 ({first_key}):")
                print(f"   预测: {first_result.get('prediction', 'N/A')[:100]}...")
                print(f"   真实: {first_result.get('label', 'N/A')[:100]}...")
        else:
            print(f"⚠️  预期的输出文件未找到: {expected_file}")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 实验运行失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 意外错误: {e}")
        return False

def main():
    """主函数"""
    
    print("🧪 递归摘要实验 - 首次运行")
    print("=" * 50)
    
    # 检查API密钥
    if not check_api_key():
        return False
    
    # 检查依赖
    if not check_dependencies():
        return False
        
    # 检查数据集
    if not os.path.exists("data/msc_dialogue/session_5/test.txt"):
        print("❌ 数据集未找到")
        print("请先运行数据集下载脚本")
        return False
    
    print("✅ 数据集已就绪")
    
    # 运行实验
    success = run_experiment()
    
    if success:
        print("\n🎉 首次实验成功完成!")
        print("\n📚 接下来可以:")
        print("1. 查看完整实验指南: EXPERIMENT_REPRODUCTION.md")
        print("2. 运行更多基线对比:")
        print("   python main_chatgpt.py --dataset msc --session_id 5 --mode full")
        print("   python main_chatgpt.py --dataset msc --session_id 5 --mode window")
        print("3. 使用更多测试样本:")
        print("   python main_chatgpt.py --dataset msc --session_id 5 --mode rsum --test_num 300")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)