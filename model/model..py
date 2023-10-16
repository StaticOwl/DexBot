import torch
from torch.utils.data import Dataset, DataLoader
from transformers import RobertaModel, RobertaTokenizer

# Tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base') 

# Dataset handles tokenization
class RedditDataset(Dataset):
  def __init__(self, from_file, to_file):
    self.from_texts = load_texts(from_file) 
    self.to_texts = load_texts(to_file)

  def __len__(self):
    return len(self.from_texts)

  def __getitem__(self, idx):
    from_text = self.from_texts[idx]
    to_text = self.to_texts[idx]

    from_tokens = tokenizer(from_text)
    to_tokens = tokenizer(to_text)

    return from_tokens, to_tokens

# Model 
class Seq2Seq(nn.Module):   
  def __init__(self, encoder, decoder):
    super().__init__()
    self.encoder = encoder
    self.decoder = decoder
  
  def forward(self, x, y):
    x_embed = self.encoder(x)
    y_pred = self.decoder(x_embed) 
    return y_pred

encoder = RobertaModel.from_pretrained('roberta-base')
decoder = LSTMDecoder() # Implements RNN decoder 
model = Seq2Seq(encoder, decoder)

# Training loop
for epoch in num_epochs:
  
  for x, y in DataLoader(RedditDataset(), batch_size=32):
  
    pred = model(x, y[:-1])
    loss = calc_loss(pred, y)

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

# Save model
torch.save(model.state_dict(), 'chatbot.pt')