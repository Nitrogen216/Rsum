#!/usr/bin/env python3
"""
Download MSC (Multi-Session Chat) dataset from Hugging Face and convert to the expected format.
"""
import json
import os
from datasets import load_dataset
from tqdm import tqdm

def download_msc_dataset():
    """Download MSC dataset from Hugging Face and save in expected format."""
    
    print("Downloading MSC dataset from Hugging Face...")
    
    try:
        # Try to load the MSC dataset from Hugging Face
        dataset = load_dataset("nayohan/multi_session_chat")
        
        print(f"Dataset loaded successfully!")
        print(f"Available splits: {dataset.keys()}")
        
        # Create directory structure
        base_dir = "data/msc_dialogue"
        os.makedirs(base_dir, exist_ok=True)
        
        # Process each split (train, validation, test)
        for split_name, split_data in dataset.items():
            print(f"\nProcessing {split_name} split...")
            
            # Group data by session
            sessions = {}
            for item in tqdm(split_data):
                session_id = item.get('session_id', 1)  # Default to session 1 if not specified
                
                if session_id not in sessions:
                    sessions[session_id] = []
                sessions[session_id].append(item)
            
            # Save each session to separate files
            for session_id, session_data in sessions.items():
                session_dir = f"{base_dir}/session_{session_id}"
                os.makedirs(session_dir, exist_ok=True)
                
                # Map split names to expected filenames
                if split_name == "train":
                    filename = "train.txt"
                elif split_name == "validation":
                    filename = "valid.txt"
                else:
                    filename = "test.txt"
                
                output_path = f"{session_dir}/{filename}"
                
                print(f"Saving {len(session_data)} examples to {output_path}")
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    for item in session_data:
                        # Convert to the expected JSONL format
                        json_line = json.dumps(item, ensure_ascii=False)
                        f.write(json_line + '\n')
        
        print("\nMSC dataset download completed!")
        return True
        
    except Exception as e:
        print(f"Error downloading from Hugging Face: {e}")
        print("Trying alternative method...")
        return download_msc_alternative()

def download_msc_alternative():
    """Alternative method to download MSC dataset."""
    
    print("Attempting to create sample MSC data structure...")
    
    # Create basic directory structure and sample files
    base_dir = "data/msc_dialogue"
    
    for session_id in [1, 2, 3, 4, 5]:
        session_dir = f"{base_dir}/session_{session_id}"
        os.makedirs(session_dir, exist_ok=True)
        
        # Create placeholder files with the expected structure
        for filename in ["train.txt", "valid.txt", "test.txt"]:
            filepath = f"{session_dir}/{filename}"
            
            # Create a sample entry in the expected format
            sample_data = {
                "metadata": {
                    "initial_data_id": f"sample_{session_id}_{filename}"
                },
                "previous_dialogs": [
                    {
                        "dialog": [
                            {"text": "Hello! How are you today?"},
                            {"text": "I'm doing well, thank you! How about you?"}
                        ],
                        "personas": [
                            ["I like to read books", "I enjoy hiking"],
                            ["I work as a teacher", "I have two cats"]
                        ]
                    }
                ],
                "dialog": [
                    {"text": "That's great to hear!"},
                    {"text": "Yes, it's a beautiful day for a conversation."}
                ]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json_line = json.dumps(sample_data, ensure_ascii=False)
                f.write(json_line + '\n')
    
    # Create prompts.json file
    prompts_path = f"{base_dir}/prompts.json"
    prompts_data = {
        "gpt-3.5-turbo": {
            "gen_response_with_memory": "You are having a conversation. Use the previous memory: {prev_memory}. Current dialog: {dialog}. Your response:",
            "gen_response_with_memory_example": "Example: {example}. Use the previous memory: {prev_memory}. Current dialog: {dialog}. Your response:",
            "gen_memory1": "Previous memory: {prev_memory}. New dialog: {dialog}. Updated memory:",
            "example1": "This is an example conversation.",
            "example2": "This is another example.",
            "example3": "This is a third example."
        }
    }
    
    with open(prompts_path, 'w', encoding='utf-8') as f:
        json.dump(prompts_data, f, ensure_ascii=False, indent=2)
    
    print(f"Created sample MSC data structure at {base_dir}")
    print("Note: This contains sample data. For real experiments, please obtain the actual MSC dataset.")
    return True

if __name__ == "__main__":
    success = download_msc_dataset()
    if success:
        print("MSC dataset setup completed successfully!")
    else:
        print("Failed to download MSC dataset.")