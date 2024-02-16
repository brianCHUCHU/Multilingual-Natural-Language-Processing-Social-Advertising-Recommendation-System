from gurobipy import *
import math
import pandas as pd
import numpy as np


num_subgraph = 4


def z_score_normalize(data):
    data = np.array(data)
    mean = np.mean(data)
    std = np.std(data)
    return (data - mean) / std


def load_data(folder):
    # load data
    items = []
    n_star = []
    n_nhelpful = []
    degree = []
    similarity = []

    for i in range(1, num_subgraph + 1):
        df = pd.read_csv(folder + str(i) + '.csv')
        items.append({})
        n_star.append({})
        n_nhelpful.append({})
        degree.append({})
        similarity.append({})

        df['stars'] = z_score_normalize(df['stars'].tolist())
        df['nhelpful'] = z_score_normalize(df['nhelpful'].tolist())
        df['trust'] = z_score_normalize(df['trust'].tolist())

        for j in range(len(df['work'].tolist())):
            if df['work'].tolist()[j] not in items[i - 1]:
                items[i - 1][df['work'].tolist()[j]] = []
                n_star[i - 1][df['work'].tolist()[j]] = []
                n_nhelpful[i - 1][df['work'].tolist()[j]] = []
                degree[i - 1][df['work'].tolist()[j]] = []
                similarity[i - 1][df['work'].tolist()[j]] = []
            items[i - 1][df['work'].tolist()[j]].append(df['work'].tolist()[j])
            n_star[i - 1][df['work'].tolist()[j]].append(df['stars'].tolist()[j])
            n_nhelpful[i - 1][df['work'].tolist()[j]
                              ].append(df['nhelpful'].tolist()[j])
            degree[i - 1][df['work'].tolist()[j]].append(df['depth'].tolist()[j])
            similarity[i - 1][df['work'].tolist()[j]
                              ].append(df['trust'].tolist()[j])

    return items, n_star, n_nhelpful, similarity, degree


def load_self_star(folder):
    self = []  # binary
    for i in range(1, num_subgraph + 1):
        df = pd.read_csv(folder + str(i) + '.csv')
        self.append({})
        for j in range(len(df['work'].tolist())):

            self[i - 1][df['work'].tolist()[j]] = df['stars'].tolist()[j]

    return self


items, n_star, n_nhelpful, similarity, degree = load_data('./subgroups/')
self = load_self_star('./subgroups_self/')


# Create a new model
m = Model("NMSL")  # 檸檬熟了

# Create variables
theta1 = m.addVar(vtype=GRB.CONTINUOUS, name="theta1")
theta2 = m.addVar(vtype=GRB.CONTINUOUS, name="theta2")
theta3 = m.addVar(vtype=GRB.CONTINUOUS, name="theta3")
theta4 = m.addVar(vtype=GRB.CONTINUOUS, name="theta4")


# Set objective
m.setObjective(
    quicksum(
        quicksum(
            quicksum(
                (1 - math.log(degree[k][j][i] + 1)/math.log(3)) * (theta1 * n_star[k][j][i] + theta2 * (n_nhelpful[k][j][i] + 1) + theta3 *
                                                                   similarity[k][j][i]) * self[k][j]
                for i in range(len(items[k][j]))
            )
            for j in items[k].keys()
        )
        for k in range(num_subgraph)
    ),

    GRB.MAXIMIZE)

# Add constraint:
m.addConstrs(
    quicksum(
        quicksum(
            (1 - math.log(degree[k][j][i] + 1)/math.log(3)) * (theta1 * n_star[k][j][i] + theta2 * (n_nhelpful[k][j][i] + 1) + theta3 *
                                                               similarity[k][j][i])

            for i in range(len(items[k][j]))
        )
        for j in items[k].keys()
    ) <= 5
    for k in range(num_subgraph)
)

for k in range(num_subgraph):
    m.addConstrs(
        quicksum(
            (1 - math.log(degree[k][j][i] + 1)/math.log(3)) * (theta1 * n_star[k][j][i] + theta2 * (n_nhelpful[k][j][i] + 1) + theta3 *
                                                               similarity[k][j][i])

            for i in range(len(items[k][j]))
        ) <= 1
        for j in items[k].keys()
    )

for k in range(num_subgraph):
    m.addConstrs(
        quicksum(
            (1 - math.log(degree[k][j][i] + 1)/math.log(3)) * (theta1 * n_star[k][j][i] + theta2 * (n_nhelpful[k][j][i] + 1) + theta3 *
                                                               similarity[k][j][i])

            for i in range(len(items[k][j]))
        ) >= 0
        for j in items[k].keys()
    )

# Optimize model
m.optimize()

for v in m.getVars():
    if v.x > 0 and v.varName[0] == 't':
        print('%s %g' % (v.varName, v.x))
