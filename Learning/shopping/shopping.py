import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")



def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    #1. read csv file 
    #   ignore the first row

    with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # ignore the first row
            data = list(reader)

    #2. split data into evidence and labels
    evidence = [row[:-1] for row in data]

    labels = [row[-1] for row in data]

    # print(evidence[0:1])
    # print(labels[0:1])

    month_to_int = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "June": 6,
                    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    #3. In evidence  
    for row in evidence:
        # convert abbreviation of month to integer
        row[10] = month_to_int[row[10]] - 1
        # convert VisitorType to integer
        row[15] = 1 if row[15] == "Returning_Visitor" else 0
        # convert weekend to integer
        row[16] = 1 if row[16] == "TRUE" else 0
    
    #   convert all the item to float
    evidence = [[float(item) for item in row] for row in evidence]

    #4. In label , replace True with 1 and False with 0
    labels = [1 if label == "TRUE" else 0 for label in labels]

    
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # 1. count the number of 1 , 0 in labels
    count_1 = labels.count(1)
    count_0 = labels.count(0)
    true_negative =  0
    true_positive = 0
    # 2. iterate over each label and prediction
    for label, prediction in zip(labels, predictions):
        # 3. count the number of true positive, true negative
        if label == 1 and prediction == 1:
            true_positive += 1
        if label == 0 and prediction == 0:
            true_negative += 1

    return (true_positive / count_1, true_negative / count_0)
    


if __name__ == "__main__":
    main()
