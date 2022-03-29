from time import perf_counter

import numpy as np
import pandas as pd
from hurry.filesize import size

from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier as RFC

import cudf
from cuml.ensemble import RandomForestClassifier as cuRFC

train_size = int(6e5) * 256
test_size = int(1e5) * 256
npoints = train_size + test_size
nfeatures = 16
random_state = 42

accuracies_gpu = []

total_times_gpu = []

init_times_gpu = []
transfer_times_gpu = []

def np2cudf(df):
    # convert numpy array to cuDF dataframe
    df = pd.DataFrame({"fea%d" % i: df[:, i] for i in range(df.shape[1])})
    pdf = cudf.DataFrame()
    for c, column in enumerate(df):
        pdf[str(c)] = df[column]
    return pdf

# load empty data to the GPU to pay the initialization cost
tic = perf_counter()
gpu_data = np2cudf(np.zeros((2, 2)))
toc = perf_counter()
init_time_gpu = toc - tic
del gpu_data

print(f"number of points : {train_size}")
data_size = train_size * (nfeatures + 1) * 4
print(f"data size = {size(data_size)}")

##################################################
#                   DATA GEN                     #
##################################################

X, y = make_classification(n_samples=npoints, n_features=nfeatures, n_informative=4, n_redundant=4,
                            random_state=random_state)
X = X.astype(np.float32)
y = y.astype(np.float32)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, shuffle=False)

##################################################
#                   GPU PERF                     #
##################################################

# load the data to the GPU
tic = perf_counter()
X_train_gpu = np2cudf(X_train)
y_train_gpu = cudf.DataFrame(y_train)
toc = perf_counter()
transfer_time_gpu = toc - tic

clf = cuRFC(n_estimators=1, random_state=random_state, split_criterion='gini', max_depth=10, bootstrap=False, max_features=1.0, n_streams=1)

tic = perf_counter()
clf.fit(X_train_gpu, y_train_gpu)
toc = perf_counter()
# export_graphviz(clf, out_file="tree_dpu.dot")
y_pred = clf.predict(X_test)
gpu_accuracy = accuracy_score(y_test, y_pred)

# read GPU times
accuracies_gpu.append(gpu_accuracy)
total_times_gpu.append(toc - tic)
init_times_gpu.append(init_time_gpu)
transfer_times_gpu.append(transfer_time_gpu)
print(f"Accuracy for GPUs: {gpu_accuracy}")
print(f"total time for GPUs: {toc - tic} s")

df = pd.DataFrame(
    {
        "GPU_times": total_times_gpu,
        "GPU_init_time": init_times_gpu,
        "GPU_transfer_times": transfer_times_gpu,
        "GPU_scores": accuracies_gpu,
    },
)

df.to_csv("strong_scaling_gpu.csv")