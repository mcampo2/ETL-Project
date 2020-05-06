# Part 2: Iris Flower Database (API to SQL)
# see Jupyter Notebook for verbose version

from sklearn import datasets
import numpy as np

# Source scikit-learn
iris = datasets.load_iris()

# Aggregate the data
header = np.append(iris.feature_names, "target")
table = np.append(iris.data, [[iris.target_names[target]] for target in iris.target], axis=1)

# Destination SQL Script
f = open("iris.sql", "w")

# Create table
f.write("DROP TABLE IF EXISTS IRIS;\n")
f.write("CREATE TABLE IRIS (\n")
f.write("  SEPAL_LENGTH FLOAT,\n")
f.write("  SEPAL_WIDTH FLOAT,\n")
f.write("  PETAL_LENGTH FLOAT,\n")
f.write("  PETAL_WIDTH FLOAT,\n")
f.write("  TARGET ENUM(" + str(list(iris.target_names))[1:-1] + ")\n")
f.write(");\n")
f.write("\n")

# Insert data
for row in table:
    f.write("INSERT INTO IRIS (SEPAL_LENGTH, SEPAL_WIDTH, PETAL_LENGTH, PETAL_WIDTH, TARGET)\n")
    f.write("  VALUES ('" + "', '".join(row) + "');\n")

# Close SQL Script
f.close()