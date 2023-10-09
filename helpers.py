"""Some helper functions for project 1."""
import csv
import numpy as np


def load_csv_data(data_path, sub_sample=False, test=False):
    """Loads data and returns y (class labels), tX (features) and ids (event ids)"""
    if test == False:
        y = np.genfromtxt(
            data_path + "y_train.csv",
            delimiter=",",
            skip_header=1,
            dtype=str,
        )
        x = np.genfromtxt(data_path + "x_train.csv", delimiter=",", skip_header=1)
        ids = x[:, 0].astype(np.int)
        input_data = x[:, 2:]
        yb = np.ones(len(y))
        yb[np.where(y == "0")] = 0

        if sub_sample:
            yb = yb[::50]
            input_data = input_data[::50]
            ids = ids[::50]

        return yb, input_data, ids

    else:
        x = np.genfromtxt(data_path + "x_test.csv", delimiter=",", skip_header=1)
        ids = x[:, 0].astype(np.int)
        input_data = x[:, 2:]

        if sub_sample:
            input_data = input_data[::50]
            ids = ids[::50]

        return input_data, ids


def create_csv_submission(ids, y_pred, name):
    """
    Creates an output file in .csv format for submission to Kaggle or AIcrowd
    Arguments: ids (event ids associated with each prediction)
               y_pred (predicted class labels)
               name (string name of .csv output file to be created)
    """
    with open(name, "w") as csvfile:
        fieldnames = ["Id", "Prediction"]
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        for r1, r2 in zip(ids, y_pred):
            writer.writerow({"Id": int(r1), "Prediction": int(r2)})


def batch_iter(y, tx, batch_size, num_batches=1, shuffle=True):
    """
    Generate a minibatch iterator for a dataset.
    Takes as input two iterables (here the output desired values 'y' and the input data 'tx')
    Outputs an iterator which gives mini-batches of `batch_size` matching elements from `y` and `tx`.
    Data can be randomly shuffled to avoid ordering in the original data messing with the randomness of the minibatches.
    Example of use :
    for minibatch_y, minibatch_tx in batch_iter(y, tx, 32):
        <DO-SOMETHING>
    """
    data_size = len(y)

    if shuffle:
        shuffle_indices = np.random.permutation(np.arange(data_size))
        shuffled_y = y[shuffle_indices]
        shuffled_tx = tx[shuffle_indices]
    else:
        shuffled_y = y
        shuffled_tx = tx
    for batch_num in range(num_batches):
        start_index = batch_num * batch_size
        end_index = min((batch_num + 1) * batch_size, data_size)
        if start_index != end_index:
            yield shuffled_y[start_index:end_index], shuffled_tx[start_index:end_index]
