from tqdm import tqdm
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from .datasets import CodeDataset
from .models import CodeLanguageModel, HybridModel

def train_model(json_file, tokenizer, classical_model, num_qubits=None, epochs=10, batch_size=32, lr=0.001):
    """
    Train a model, either classical or hybrid.

    Parameters:
    - json_file: Path to the JSON dataset.
    - tokenizer: Tokenizer instance.
    - classical_model: Predefined PyTorch model (classical).
    - num_qubits: Number of qubits for hybrid quantum-classical model. If None, trains classical-only model.
    - epochs: Number of training epochs.
    - batch_size: Batch size for training.
    - lr: Learning rate.
    """
    dataset = CodeDataset(json_file, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Use Hybrid Model if num_qubits is specified
    if num_qubits:
        model = HybridModel(classical_model, num_qubits)
    else:
        model = classical_model

    criterion = torch.nn.NLLLoss()  # Change based on task
    optimizer = optim.Adam(model.parameters(), lr=lr)

    model.train()
    from tqdm import tqdm
    

    for epoch in range(epochs):
        total_loss = 0
        model.train()
        with tqdm(dataloader, desc=f"\033[92mEpoch {epoch+1}/{epochs}\033[0m", unit="batch") as tepoch:
            for inputs, targets in tepoch:
                optimizer.zero_grad()

                # Forward pass
                outputs = model(inputs)  # Outputs: (batch_size, seq_len, vocab_size)
                outputs = outputs.view(-1, outputs.size(-1))  # Flatten outputs
                targets = targets.view(-1)  # Flatten targets

                # Validate output range and targets
                print(f"\033[93mOutputs min/max:\033[0m {outputs.min().item()} / {outputs.max().item()}")
                print(f"\033[93mTargets min/max:\033[0m {targets.min().item()} / {targets.max().item()}")

                # Calculate loss
                loss = criterion(outputs, targets)
                print(f"Loss: {loss.item()}")

                # Debug loss
                print(f"\033[94mLoss before backward:\033[0m {loss.item()}")

                # Backward pass and optimization
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()

                total_loss += loss.item()

                # Update progress bar with colored loss
                tepoch.set_postfix(loss=f"\033[91m{loss.item():.4f}\033[0m")

        # Log average loss for the epoch
        print(f"\033[96mEpoch {epoch+1}/{epochs}, Average Loss:\033[0m {total_loss / len(dataloader):.4f}")


    # Save the model
    model_path = 'hybrid_model.pth' if num_qubits else 'classical_model.pth'
    torch.save(model.state_dict(), model_path)
    print(f"Model saved at {model_path}.")


