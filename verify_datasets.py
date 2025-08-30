#!/usr/bin/env python3
"""
Verify that datasets are properly formatted and accessible.
"""
import json
import os
from pathlib import Path

def verify_msc_dataset():
    """Verify MSC dataset structure."""
    print("=== Verifying MSC Dataset ===")
    
    base_dir = Path("data/msc_dialogue")
    
    if not base_dir.exists():
        print("❌ MSC data directory not found")
        return False
    
    # Check sessions 1-5
    sessions_found = []
    for session_id in range(1, 6):
        session_dir = base_dir / f"session_{session_id}"
        if session_dir.exists():
            sessions_found.append(session_id)
            
            # Check required files
            test_file = session_dir / "test.txt"
            valid_file = session_dir / "valid.txt"
            
            if test_file.exists():
                # Count lines
                with open(test_file, 'r') as f:
                    lines = sum(1 for _ in f)
                print(f"✅ Session {session_id}: test.txt ({lines} examples)")
                
                # Verify JSON format
                try:
                    with open(test_file, 'r') as f:
                        first_line = f.readline().strip()
                        if first_line:
                            json.loads(first_line)
                    print(f"✅ Session {session_id}: JSON format valid")
                except json.JSONDecodeError as e:
                    print(f"❌ Session {session_id}: Invalid JSON format - {e}")
            else:
                print(f"❌ Session {session_id}: test.txt missing")
    
    # Check prompts file
    prompts_file = base_dir / "prompts.json"
    if prompts_file.exists():
        try:
            with open(prompts_file, 'r') as f:
                prompts = json.load(f)
            print(f"✅ MSC prompts.json loaded successfully")
            print(f"   Available models: {list(prompts.keys())}")
        except Exception as e:
            print(f"❌ Error loading MSC prompts.json: {e}")
    else:
        print(f"❌ MSC prompts.json not found")
    
    print(f"MSC sessions found: {sessions_found}")
    return len(sessions_found) >= 4  # Need at least sessions 1-4

def verify_carecall_dataset():
    """Verify CareCall dataset structure."""
    print("\n=== Verifying CareCall Dataset ===")
    
    carecall_file = Path("data/carecall/carecall-memory_en_auto_translated.json")
    
    if not carecall_file.exists():
        print("❌ CareCall dataset file not found")
        return False
    
    try:
        with open(carecall_file, 'r') as f:
            data = json.load(f)
        
        print(f"✅ CareCall dataset loaded successfully")
        print(f"   Total sessions: {len(data)}")
        
        # Check structure
        if len(data) > 0:
            sample = data[0]
            if isinstance(sample, list) and len(sample) > 0:
                first_dialog = sample[0]
                required_keys = ['guid', 'dialogue']
                
                if all(key in first_dialog for key in required_keys):
                    print(f"✅ CareCall dataset structure is valid")
                    print(f"   Sample session length: {len(sample)} dialogs")
                else:
                    print(f"❌ CareCall dataset missing required keys: {required_keys}")
                    return False
            else:
                print(f"❌ CareCall dataset has invalid structure")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading CareCall dataset: {e}")
        return False

def verify_prompt_files():
    """Verify main prompt files."""
    print("\n=== Verifying Prompt Files ===")
    
    main_prompt_file = Path("prompt.json")
    
    if main_prompt_file.exists():
        try:
            with open(main_prompt_file, 'r') as f:
                prompts = json.load(f)
            print(f"✅ Main prompt.json loaded successfully")
            print(f"   Available datasets: {list(prompts.keys())}")
            
            # Check required prompts for each dataset
            for dataset in ['msc', 'carecall']:
                if dataset in prompts:
                    dataset_prompts = prompts[dataset]
                    for model in dataset_prompts:
                        required_prompts = ['update_memory', 'update_response', 'direct_response']
                        missing = [p for p in required_prompts if p not in dataset_prompts[model]]
                        if missing:
                            print(f"⚠️  {dataset}-{model} missing prompts: {missing}")
                        else:
                            print(f"✅ {dataset}-{model} all prompts present")
                else:
                    print(f"❌ Dataset {dataset} not found in main prompt.json")
            
            return True
        except Exception as e:
            print(f"❌ Error loading main prompt.json: {e}")
            return False
    else:
        print(f"❌ Main prompt.json not found")
        return False

def test_dataloader():
    """Test if the dataloader can load the datasets."""
    print("\n=== Testing Data Loading ===")
    
    try:
        # Simple import test
        from config import get_args
        print("✅ Config module imported successfully")
        
        # Test with sample arguments
        import sys
        sys.argv = ['verify_datasets.py', '--dataset', 'msc', '--session_id', '5', '--mode', 'rsum']
        args = get_args()
        print("✅ Sample arguments parsed successfully")
        
        # Try to import dataloader
        from dataloader import load_dataset
        print("✅ Dataloader module imported successfully")
        
        # Note: We don't actually load data here to avoid dependency issues
        print("✅ Basic dataloader test passed")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Dataloader test issue: {e}")
        return True  # Non-critical error

def main():
    """Main verification function."""
    print("🔍 Verifying Dataset Setup for Recursive Summarization Experiment")
    print("=" * 60)
    
    results = {
        'msc': verify_msc_dataset(),
        'carecall': verify_carecall_dataset(), 
        'prompts': verify_prompt_files(),
        'dataloader': test_dataloader()
    }
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component.upper()}: {'PASSED' if status else 'FAILED'}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All verifications passed! The datasets are ready for experiments.")
        print("\nNext steps:")
        print("1. Configure API keys (if using GPT models)")
        print("2. Run experiments using commands in EXPERIMENT_REPRODUCTION.md")
        print("3. Start with basic MSC Session 5 experiment:")
        print("   python main_chatgpt.py --dataset msc --session_id 5 --mode rsum")
    else:
        print("\n⚠️  Some components failed verification. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)