import matplotlib.pyplot as plt
import pandas as pd

products = ["potatoes", "cabbages", "sausages", "porridge", "tea"]
weights =[1000, 500,675, 100, 50]
weights1 =[10, 50,75, 10, 51]

plt.plot(products, weights, color="#FFFF0F", marker='^', linewidth= 5, linestyle= '--', label="Weights")

plt.plot(products, weights1, color="#2D00F7", marker='^', linewidth= 5, linestyle= '--', label="Weights1")
plt.xlabel("Products")
plt.ylabel("Weights")
plt.title("Product weights")
plt.legend()
plt.xticks()
plt.grid()
plt.show()

