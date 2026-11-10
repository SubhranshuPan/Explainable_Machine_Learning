import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# FIX: read from the shared data/ folder (run from the Final_Submission folder)
alldata = pd.read_csv('data/all_data.csv', header=None).to_numpy()
print('Data shape:', alldata.shape)
print('First five rows:')
print(alldata[:5])

fig, ax = plt.subplots(3, 3, figsize=(18, 7))
categories = ['N', 'L', 'R', 'V', 'A', 'F', 'f', '/']
#"N": Normal beat
#"L": Left bundle branch block beat
#"R": Right bundle branch block beat
#"V": Premature ventricular contraction
#"A": Atrial premature beat
#"F": Fusion of ventricular and normal beat
#"f": Fusion of paced and normal beat
#"/": Paced beat

for i in range(len(categories)):
    indices_category = np.argwhere(alldata[:, -2] == i + 1)
    if len(indices_category) > 0:
        # FIX: plot a beat from the middle of the class; the first beat of a class sits at the
        # start of a recording and is partly zero-padded (flat line at the start)
        ax[i // 3, i % 3].plot(np.arange(275), alldata[indices_category[len(indices_category) // 2], :-2][0])
    ax[i // 3, i % 3].set_title('Class: ' + categories[i] + ', Number: ' + str(i + 1))

ax[2, 2].axis('off')
plt.tight_layout()
fig.savefig('figures/task1_ecg_beats.jpg', dpi=400)  # FIX: save into figures/
plt.show()

# 3. Count and plot the distribution of the eight classes.
counts = []
for i in range(len(categories)):
    count = np.sum(alldata[:, -2] == i + 1)
    counts.append(count)
    print('Class', categories[i], ':', count)

fig = plt.figure(figsize=(12, 6))
barplt = plt.bar(categories, counts, width=0.6)
plt.title('Distribution of ECG Beat Classes')
plt.xlabel('Annotations')
plt.ylabel('Counts')

for bar in barplt:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + max(counts) * 0.01, str(int(yval)))

plt.tight_layout()
fig.savefig('figures/task1_class_distribution.jpg', dpi=400)  # FIX: save into figures/
plt.show()