
import os
import torch
import torchvision
from torch.utils.data import random_split
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import cv2
import pickle
import copy
from PIL import Image
import numpy as np

dataset = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))

class ImageClassificationBase(nn.Module):
    
    def training_step(self, batch):
        images, labels = batch 
        out = self(images)                  # Generate predictions
        loss = F.cross_entropy(out, labels) # Calculate loss
        return loss
    
    def validation_step(self, batch):
        images, labels = batch 
        out = self(images)                    # Generate predictions
        loss = F.cross_entropy(out, labels)   # Calculate loss
        acc = accuracy(out, labels)           # Calculate accuracy
        return {'val_loss': loss.detach(), 'val_acc': acc}
        
    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()      # Combine accuracies
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}
    
    def epoch_end(self, epoch, result):
        print("Epoch {}: train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch+1, result['train_loss'], result['val_loss'], result['val_acc']))


class ResNet(ImageClassificationBase):
    def __init__(self):
        super().__init__()
        
        # Use a pretrained model
        self.network = models.resnet50(pretrained=True)
    
        # Replace last layer
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, len(dataset))
    
    def forward(self, xb):
        return torch.sigmoid(self.network(xb))


def get_default_device():
    
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')


device = get_default_device()


def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)



transformations = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])


model = ResNet()
model = torch.load("Model.pkl",map_location=torch.device('cpu'))

model = to_device(ResNet(), device)



def predict_image(img, model):
    # Convert to a batch of 1
    xb = to_device(img.unsqueeze(0), device)
    # Get predictions from model
    yb = model(xb)
    # Pick index with highest probability
    prob, preds  = torch.max(yb, dim=1)
    # Retrieve the class label
    return dataset[preds[0].item()],prob


# cap = cv2.VideoCapture(0)


# while True:
#     ret, frame = cap.read() 
#     cv2.imshow("h",frame)          # read from camera
#     if not ret:
#         break
#     # framen = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))    # frame = cv2.imread(frame)
#     framen = Image.fromarray(np.uint8(frame)).convert('RGB')
#     framen = transformations(framen)
#     pred, prob = predict_image(framen,model)
#     if prob.item() < 0.6:
#         print("No Trash")
#     else:
#         print("Trash")       # show image
#     if cv2.waitKey(10) == ord('q'):  # wait a bit, and see keyboard press
#         break                        # if q pressed, quit

# # release things before quiting
# cap.release()
# cv2.destroyAllWindows()


img = Image.open("card.jpeg")
img = transformations(img)
pred,prob = predict_image(img,model)
if prob.item() < 0.5:
    print("No Trash")
else:
    print("Trash") 
