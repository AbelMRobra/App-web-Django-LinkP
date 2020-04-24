import matplotlib.pyplot as plt

plt.figure(figsize=(5,5))

labels = ["USA", "AMERICA"]

values = [30, 70]

plt.pie(values, labels=labels)

plt.show()