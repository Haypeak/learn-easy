import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class AdaptiveLearningModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(AdaptiveLearningModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return self.softmax(x)

# Initialize model
model = AdaptiveLearningModel(input_size=5, hidden_size=10, output_size=3)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

def predict_next_topic(student_data):
    """ Predicts the next best topic for the student """
    student_tensor = torch.tensor(student_data, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        output = model(student_tensor)
    predicted_topic = torch.argmax(output).item()
    return predicted_topic
