import json
import torch
from torch.utils.data import Dataset

class CodeDataset(Dataset):
    def __init__(self, json_file, tokenizer, max_length=256):
        with open(json_file, 'r') as file:
            self.data = json.load(file)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        topic_data = self.data[idx]
        code = ''
        for subtopic in topic_data.get("subtopics", []):
            code += f"# {subtopic['name']}\n{subtopic['code']}\n"

        tokens = self.tokenizer(code)

        # Pad tokens to max_length
        tokens = tokens[:self.max_length] + [0] * max(0, self.max_length - len(tokens))

        # Inputs and targets
        input_tensor = torch.tensor(tokens[:-1], dtype=torch.long)  # Input (shifted left)
        target_tensor = torch.tensor(tokens[1:], dtype=torch.long)  # Target (shifted right)

        return input_tensor, target_tensor
