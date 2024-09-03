import torch
import pytorch_lightning as pl
from torch.utils.data import DataLoader, TensorDataset


class TransformerClassifier(pl.LightningModule):
    def __init__(self, model, learning_rate=2e-5):
        super(TransformerClassifier, self).__init__()
        self.model = model
        self.learning_rate = learning_rate
        self.validation_step_outputs = []

        # Freeze the embedding layer
        self.freeze_embedding_layer()

    def freeze_embedding_layer(self):
        # Assuming the model is a BERT-based model, you can freeze the embedding layer like this:
        for param in self.model.bert.embeddings.parameters():
            param.requires_grad = False

    def forward(self, input_ids, attention_mask, labels=None):
        return self.model(input_ids, attention_mask=attention_mask, labels=labels)

    def training_step(self, batch, batch_idx):
        input_ids, attention_mask, labels = batch
        outputs = self(input_ids, attention_mask, labels)
        loss = outputs.loss
        logits = outputs.logits
        preds = torch.argmax(logits, dim=1)
        acc = (preds == labels).float().mean()
        # Log loss and metric
        self.log("train_loss", loss, on_step=False, on_epoch=True, prog_bar=False, logger=True)
        self.log("train_acc", acc, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return {'loss': loss, 'train_acc': acc}

    def validation_step(self, batch, batch_idx):
        input_ids, attention_mask, labels = batch
        outputs = self(input_ids, attention_mask)
        logits = outputs.logits
        loss = torch.nn.functional.cross_entropy(logits, labels)
        preds = torch.argmax(logits, dim=1)
        acc = (preds == labels).float().mean()
        self.validation_step_outputs.append(acc)
        self.log("val_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        self.log("val_acc", acc, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return {'val_loss': loss, 'val_acc': acc, 'preds': preds, 'labels': labels}

    def predict_step(self, batch, batch_idx):
        input_ids, attention_mask, labels = batch
        # Forward pass
        outputs = self(input_ids, attention_mask)
        # Get predictions
        logits = outputs.logits
        preds = torch.argmax(logits, dim=1)
        # Return both predictions and labels if you want to compare them later
        return {'preds': preds, 'labels': labels}

    def on_validation_epoch_end(self):
        epoch_average_acc = torch.stack(self.validation_step_outputs).mean()
        self.log("validation_epoch_average", epoch_average_acc)
        self.validation_step_outputs.clear()  # free memory

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.learning_rate, eps=1e-8)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.9)
        return [optimizer], [scheduler]


def tokenize_data(tokenizer, texts, labels, max_length=256):
    labels = torch.tensor(labels)
    tokenizer_clf = tokenizer(
        texts,
        max_length=max_length,
        truncation=True,
        padding=True,
        return_attention_mask=True,
        return_tensors='pt',
    )
    return tokenizer_clf, labels


def create_dataloaders(tokenizer, labels, batch_size, is_training_set):
    dataset = TensorDataset(tokenizer['input_ids'], tokenizer['attention_mask'], labels)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=is_training_set, num_workers=11, persistent_workers=True)
    return loader
