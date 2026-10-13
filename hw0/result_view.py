import numpy as np
data = np.load("outputs/task2/task2_results.npz")

print(data.files)

print("P =")
print(data["projection"])

print("K =")
print(data["K"])
R = data["R"]
print("R =")
print(R)

t = data["t"]
print("t =")
print(t)

print("C =")
print(data["C"])

print("result")
print(-R.T@t)