import pandas as pd
from ml.models import CNN
target = 'emotion'

# Load training data
train = pd.read_csv('/data/train.csv')
ys = train[target]
xs = train.drop(target,axis=1)

# Create model

model = CNN()

# Train model

model.train()

# Save model