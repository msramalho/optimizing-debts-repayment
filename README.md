# Optimizing Debts Repayment
Using Operations Research to minimize transactions in a debt network

[![codecov](https://codecov.io/gh/msramalho/optimizing-debts-repayment/branch/master/graph/badge.svg)](https://codecov.io/gh/msramalho/optimizing-debts-repayment)


## Problem
Given a set of people who owe money to each other (graph), how to simplify the repayments so that the number of transactions is minimal.


## Solution
### Step 1 (According to your problem)
* For each user (node) in the graph, sum the money they are owed (in-edges, positive value) and the money they owe (out-edges, negative value). This will mean you have a balance (positive/negative) for each person. 
* Separate those who owe/pay (`pay`) from those who are owed/ get money back (`get`). 
* Convert all negative debts to positive values in `pay`.
* Assert that `sum(pay) == sum(get)`.


### Step 2 (Minimize transactions)
Feed the `pay` and `get` variables into the `minimize_transactions(pay, get, decimal_places=2, verbose=False)` function. 

By default, it is assumed your values have two decimal places of precision, but that can be changed with the `decimal_places` parameter.

To see optimization execution statistics, set `verbose=True`.

The returned result is a list of `(payer_index, getter_index, amount)` for each transaction required to zero-out all debts.

#### Example
> 1st install ortools with `pip install ortools` or `pip install -r requirements`
```python
from src.minimize_transactions import minimize_transactions as mt

# Owers: 11, 9.5
# Getters: 9.5, 7, 4
mt([11, 9.5], [9.5, 7, 4], verbose=True)

>>> Solve status: OPTIMAL
>>> Optimal objective value: 3
>>> Statistics
  - conflicts : 0
  - branches  : 13
  - wall time : 0.004604 s
  
>>> [(0, 1, 7.0), (0, 2, 4.0), (1, 0, 9.5)]
```
## Disclaimer
This problem is actually an example of a large set of problems relating to network flow assignment, namely:
* [Uncapacitated Fixed-Charge Network Flow (Duhamel, 2001)](papers/duhamel2001.pdf) with null per-unit costs `cij=0` and unitary(constant) fixed costs `fij=1`. 
* [Fixed-charge Transportation Problem (Spielberg, 1964)](papers/spielberg1964.pdf)

Another good reference to understanding this kind of problems is [Settling Multiple Debts Efficiently: An Invitation to Computing Science](papers/settling-debts.pdf). 

So, the presented solution can be used for other problems too, you just need to be able to do that "conversion effort". This case was presented as an example on purpose, as I believe it is actually easier to learn the logic and port it with examples rather than abstractions.
