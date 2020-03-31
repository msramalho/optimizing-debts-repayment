# -*- coding: utf-8 -*-
from ortools.sat.python import cp_model


def times_power_of_10(l, decimal_places):
    # must multiply by 10**decimal_places due to integer only restrictions
    return list(map(lambda x: int(x * (10**decimal_places)), l))


def minimize_transactions(pay, get, decimal_places=2, verbose=False):
    # pay is the list of values owed (from people that need to pay)
    # get is the list of values to receive (from people that get it back)
    # approach the problem as a bipartite graph flow
    # with custom optimization methods but similar to min cost flow problems
    # ----
    pay, get = times_power_of_10(pay, decimal_places), times_power_of_10(get, decimal_places)
    N, M = len(pay), len(get)

    # Instantiate Constraint Programming Model
    model = cp_model.CpModel()

    #------------------------------------ Variables
    activated, weight = [], []  # activated state and flow through edges
    for i in range(N):
        ai, wi = [], []
        for j in range(M):
            ai.append(model.NewBoolVar("a_%d_%d" % (i, j)))
            wi.append(model.NewIntVar(0, pay[i], "w_%d_%d" % (i, j)))
        activated.append(ai)
        weight.append(wi)

    #------------------------------------ Constraints
    # each payer must pay all they owe
    for i in range(N):
        model.Add(sum(weight[i]) == pay[i])

    # each receiver must get all they are owed
    for j in range(M):
        model.Add(sum(weight[i][j] for i in range(N)) == get[j])

    # activate edges when weights are non-null
    for i in range(N):
        for j in range(M):
            # if not activated => weight == 0 (NECESSARY)
            model.Add(weight[i][j] == 0).OnlyEnforceIf(activated[i][j].Not())
            # if activated => weight >=1 (OPTIONAL IMPROVES PERFORMANCE)
            model.Add(weight[i][j] >= 1).OnlyEnforceIf(activated[i][j])

    #------------------------------------ Objective
    # minimize transactions
    model.Minimize(sum(activated[i][j] for i in range(N) for j in range(M)))

    #------------------------------------Call solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status == cp_model.OPTIMAL, ("Something went wrong [%s]" % solver.StatusName(status))

    if verbose:  # pragma: no cover
        print('Solve status: %s' % solver.StatusName(status))
        print('Optimal objective value: %i' % solver.ObjectiveValue())
        print('Statistics')
        print('  - conflicts : %i' % solver.NumConflicts())
        print('  - branches  : %i' % solver.NumBranches())
        print('  - wall time : %f s' % solver.WallTime())

    #------------------------------------ Retrieve results
    result = []  # (A, B, X) A owes B X
    for i in range(N):
        for j in range(M):
            if solver.Value(activated[i][j]):
                how_much = solver.Value(weight[i][j])
                result.append((i, j, how_much / (10**decimal_places)))

    return result
