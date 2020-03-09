from ml.models import NN, Dummy

model = NN()
pred = model.predict([4,5,6,7,8])

print(pred)