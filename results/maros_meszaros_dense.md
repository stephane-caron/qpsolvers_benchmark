# Maros-Meszaros dense subset

| Version | 0.1.0rc4 |
|:--------|:--------------------|
| Date    | 2023-01-11 17:12:44.625267+00:00 |
| CPU     | Intel(R) Core(TM) i7-6500U CPU @ 2.50GHz |
| Run by  | [@stephane-caron](https://github.com/stephane-caron/) |

## Contents

* [Description](#description)
* [Solvers](#solvers)
* [Settings](#settings)
* [Results by settings](#results-by-settings)
    * [Default](#default)
    * [High accuracy](#high-accuracy)
    * [Low accuracy](#low-accuracy)
* [Results by metric](#results-by-metric)
    * [Success rate](#success-rate)
    * [Computation time](#computation-time)
    * [Optimality conditions](#optimality-conditions)
        * [Primal residual](#primal-residual)
        * [Dual residual](#dual-residual)
        * [Duality gap](#duality-gap)
    * [Cost error](#cost-error)

## Description

Subset of the Maros-Meszaros test setrestricted to smaller dense problems.

## Solvers

| solver   | version               |
|:---------|:----------------------|
| cvxopt   | 1.3.0                 |
| ecos     | 2.0.10                |
| gurobi   | 10.0.0 (size-limited) |
| highs    | 1.1.2.dev3            |
| osqp     | 0.6.2.post5           |
| proxqp   | 0.3.1                 |
| qpoases  | 3.2.1                 |
| qpswift  | 1.0.0                 |
| quadprog | 0.1.11                |
| scs      | 3.2.2                 |

All solvers were called via
[qpsolvers](https://github.com/stephane-caron/qpsolvers)
v2.7.2.

## Settings

There are 3 settings: *default*, *high_accuracy*
and *low_accuracy*. They validate solutions using the following
tolerances:

| tolerance   |   default |   low_accuracy |   high_accuracy |
|:------------|----------:|---------------:|----------------:|
| ``cost``    |      1000 |       1000     |        1000     |
| ``dual``    |         1 |          0.001 |           1e-09 |
| ``gap``     |         1 |          0.001 |           1e-09 |
| ``primal``  |         1 |          0.001 |           1e-09 |
| ``runtime`` |      1000 |       1000     |        1000     |

Solvers for each settings are configured as follows:

| solver   | parameter                        | default   | high_accuracy          | low_accuracy          |
|:---------|:---------------------------------|:----------|:-----------------------|:----------------------|
| cvxopt   | ``feastol``                      | -         | 1e-09                  | 0.001                 |
| ecos     | ``feastol``                      | -         | 1e-09                  | 0.001                 |
| gurobi   | ``FeasibilityTol``               | -         | 1e-09                  | 0.001                 |
| gurobi   | ``OptimalityTol``                | -         | 1e-09                  | 0.001                 |
| gurobi   | ``TimeLimit``                    | 1000.0    | 1000.0                 | 1000.0                |
| highs    | ``dual_feasibility_tolerance``   | -         | 1e-09                  | 0.001                 |
| highs    | ``primal_feasibility_tolerance`` | -         | 1e-09                  | 0.001                 |
| highs    | ``time_limit``                   | 1000.0    | 1000.0                 | 1000.0                |
| osqp     | ``eps_abs``                      | -         | 1e-09                  | 0.001                 |
| osqp     | ``eps_rel``                      | -         | 0.0                    | 0.0                   |
| osqp     | ``time_limit``                   | 1000.0    | 1000.0                 | 1000.0                |
| proxqp   | ``check_duality_gap``            | -         | True                   | True                  |
| proxqp   | ``eps_abs``                      | -         | 1e-09                  | 0.001                 |
| proxqp   | ``eps_rel``                      | -         | 0.0                    | 0.0                   |
| qpoases  | ``predefined_options``           | default   | reliable               | fast                  |
| qpoases  | ``time_limit``                   | 1000.0    | 1000.0                 | 1000.0                |
| qpswift  | ``RELTOL``                       | -         | 1.7320508075688772e-09 | 0.0017320508075688772 |
| scs      | ``eps_abs``                      | -         | 1e-09                  | 0.001                 |
| scs      | ``eps_rel``                      | -         | 0.0                    | 0.0                   |
| scs      | ``time_limit_secs``              | 1000.0    | 1000.0                 | 1000.0                |

## Results by settings

### Default

Solvers are compared over the whole test set by [shifted geometric
mean](../README.md#shifted-geometric-mean) (shm). Lower is better.

|          |   [Success rate](#success-rate) (%) |   [Runtime](#computation-time) (shm) |   [Primal residual](#primal-residual) (shm) |   [Dual residual](#dual-residual) (shm) |   [Duality gap](#duality-gap) (shm) |   [Cost error](#cost-error) (shm) |
|:---------|------------------------------------:|-------------------------------------:|--------------------------------------------:|----------------------------------------:|------------------------------------:|----------------------------------:|
| cvxopt   |                                25.8 |                                672.0 |                                    482749.9 |                                794862.9 |                                 2.5 |                             568.0 |
| ecos     |                                12.9 |                               1146.8 |                                    559250.8 |                                944595.4 |                                 2.8 |                             969.5 |
| gurobi   |                                37.1 |                                146.4 |                                    279207.1 |                              13678400.5 |                                71.5 |                             123.8 |
| highs    |                                64.5 |                                 42.1 |                                    143327.1 |                                236646.0 |                                 5.7 |                              35.4 |
| osqp     |                                51.6 |                                 15.5 |                                   3076625.0 |                               3656679.6 |                               348.3 |                             401.5 |
| proxqp   |                                95.2 |                                  1.0 |                                         1.0 |                                     1.0 |                                 1.0 |                               1.0 |
| qpoases  |                                24.2 |                                163.5 |                                   4502217.8 |                              23447138.1 |                                 1.5 |                             505.6 |
| qpswift  |                                25.8 |                                671.9 |                                    482749.9 |                                794860.4 |                                 2.5 |                             568.0 |
| quadprog |                                32.3 |                                493.0 |                                    439403.4 |                                723489.2 |                                 2.2 |                             416.8 |
| scs      |                                71.0 |                                  4.0 |                                   1879523.1 |                                371680.3 |                                47.8 |                             103.1 |

### High accuracy

Solvers are compared over the whole test set by [shifted geometric
mean](../README.md#shifted-geometric-mean) (shm). Lower is better.

|          |   [Success rate](#success-rate) (%) |   [Runtime](#computation-time) (shm) |   [Primal residual](#primal-residual) (shm) |   [Dual residual](#dual-residual) (shm) |   [Duality gap](#duality-gap) (shm) |   [Cost error](#cost-error) (shm) |
|:---------|------------------------------------:|-------------------------------------:|--------------------------------------------:|----------------------------------------:|------------------------------------:|----------------------------------:|
| cvxopt   |                                 0.0 |                                555.1 |                                         6.1 |                                 13679.2 |                            201610.2 |                             934.7 |
| ecos     |                                 0.0 |                                947.3 |                                         6.4 |                              32242383.1 |                           1008113.0 |                            1595.4 |
| gurobi   |                                11.3 |                                120.9 |                                         8.8 |                           74719645507.0 |                       44892532683.0 |                             203.6 |
| highs    |                                 0.0 |                                 34.8 |                                         2.9 |                               3772540.1 |                        3253828307.1 |                              58.2 |
| osqp     |                                41.9 |                                155.7 |                                         4.3 |                                     3.6 |                                 3.7 |                             262.2 |
| proxqp   |                                54.8 |                                  1.0 |                                         1.0 |                                     1.0 |                                89.9 |                               1.0 |
| qpoases  |                                19.4 |                                151.4 |                               45931216489.9 |                          128509042788.1 |                                 1.7 |                             831.9 |
| qpswift  |                                17.7 |                                555.0 |                                         5.6 |                                     4.9 |                             48079.4 |                             934.7 |
| quadprog |                                25.8 |                                407.2 |                                         9.6 |                                    17.4 |                                11.5 |                             685.9 |
| scs      |                                67.7 |                                 64.5 |                                         2.8 |                                     2.6 |                                 1.0 |                             108.0 |

### Low accuracy

Solvers are compared over the whole test set by [shifted geometric
mean](../README.md#shifted-geometric-mean) (shm). Lower is better.

|          |   [Success rate](#success-rate) (%) |   [Runtime](#computation-time) (shm) |   [Primal residual](#primal-residual) (shm) |   [Dual residual](#dual-residual) (shm) |   [Duality gap](#duality-gap) (shm) |   [Cost error](#cost-error) (shm) |
|:---------|------------------------------------:|-------------------------------------:|--------------------------------------------:|----------------------------------------:|------------------------------------:|----------------------------------:|
| cvxopt   |                                21.0 |                                661.5 |                                         7.1 |                                    69.2 |                                 2.3 |                             912.9 |
| ecos     |                                11.3 |                               1218.0 |                                         8.3 |                                    91.7 |                                 2.4 |                            1681.0 |
| gurobi   |                                37.1 |                                144.1 |                                         4.1 |                               1086837.1 |                             55063.1 |                             198.9 |
| highs    |                                54.8 |                                 41.5 |                                         2.1 |                                    75.9 |                              3991.4 |                              56.8 |
| osqp     |                                38.7 |                                110.7 |                                         4.4 |                                    49.5 |                               373.4 |                             155.4 |
| proxqp   |                                48.4 |                                  1.0 |                                         1.0 |                                     1.0 |                                34.6 |                               1.0 |
| qpoases  |                                19.4 |                                186.3 |                                     38002.7 |                               1265314.8 |                                 1.3 |                             729.7 |
| qpswift  |                                24.2 |                                661.4 |                                         7.1 |                                    70.2 |                                 7.2 |                             913.1 |
| quadprog |                                32.3 |                                485.3 |                                         6.4 |                                    63.0 |                                 1.9 |                             669.9 |
| scs      |                                79.0 |                                 36.9 |                                         2.9 |                                    27.2 |                                 1.0 |                              50.4 |

## Results by metric

### Success rate

Precentage of problems each solver is able to solve:

|          |   default |   high_accuracy |   low_accuracy |
|:---------|----------:|----------------:|---------------:|
| cvxopt   |        26 |               0 |             21 |
| ecos     |        13 |               0 |             11 |
| gurobi   |        37 |              11 |             37 |
| highs    |        65 |               0 |             55 |
| osqp     |        52 |              42 |             39 |
| proxqp   |        95 |              55 |             48 |
| qpoases  |        24 |              19 |             19 |
| qpswift  |        26 |              18 |             24 |
| quadprog |        32 |              26 |             32 |
| scs      |        71 |              68 |             79 |

Rows are [solvers](#solvers) and columns are [settings](#settings). We consider
that a solver successfully solved a problem when (1) it returned with a success
status and (2) its solution satisfies optimality conditions within
[tolerance](#settings). The second table below summarizes the frequency at
which solvers return success (1) and the corresponding solution did indeed pass
tolerance checks.

Percentage of problems where "solved" return codes are correct:

|          |   default |   high_accuracy |   low_accuracy |
|:---------|----------:|----------------:|---------------:|
| cvxopt   |       100 |              74 |             95 |
| ecos     |        98 |              85 |             98 |
| gurobi   |        81 |              55 |             81 |
| highs    |        87 |              23 |             77 |
| osqp     |        63 |              90 |             77 |
| proxqp   |        95 |              55 |             48 |
| qpoases  |        69 |              65 |             68 |
| qpswift  |       100 |              92 |             98 |
| quadprog |       100 |              94 |            100 |
| scs      |        74 |             100 |            100 |

### Computation time

We compare solver computation times over the whole test set using the shifted
geometric mean. Intuitively, a solver with a shifted-geometric-mean runtime of
Y is Y times slower than the best solver over the test set. See
[Metrics](../README.md#metrics) for details.

Shifted geometric mean of solver computation times (1.0 is the best):

|          |   default |   high_accuracy |   low_accuracy |
|:---------|----------:|----------------:|---------------:|
| cvxopt   |     672.0 |           555.1 |          661.5 |
| ecos     |    1146.8 |           947.3 |         1218.0 |
| gurobi   |     146.4 |           120.9 |          144.1 |
| highs    |      42.1 |            34.8 |           41.5 |
| osqp     |      15.5 |           155.7 |          110.7 |
| proxqp   |       1.0 |             1.0 |            1.0 |
| qpoases  |     163.5 |           151.4 |          186.3 |
| qpswift  |     671.9 |           555.0 |          661.4 |
| quadprog |     493.0 |           407.2 |          485.3 |
| scs      |       4.0 |            64.5 |           36.9 |

Rows are solvers and columns are solver settings. The shift is $sh = 10$. As in
the OSQP and ProxQP benchmarks, we assume a solver's run time is at the [time
limit](#settings) when it fails to solve a problem.

### Optimality conditions

#### Primal residual

The primal residual measures the maximum (equality and inequality) constraint
violation in the solution returned by a solver. We use the shifted geometric
mean to compare solver primal residuals over the whole test set. Intuitively, a
solver with a shifted-geometric-mean primal residual of Y is Y times less
precise on constraints than the best solver over the test set. See
[Metrics](../README.md#metrics) for details.

Shifted geometric means of primal residuals (1.0 is the best):

|          |   default |   high_accuracy |   low_accuracy |
|:---------|----------:|----------------:|---------------:|
| cvxopt   |  482749.9 |             6.1 |            7.1 |
| ecos     |  559250.8 |             6.4 |            8.3 |
| gurobi   |  279207.1 |             8.8 |            4.1 |
| highs    |  143327.1 |             2.9 |            2.1 |
| osqp     | 3076625.0 |             4.3 |            4.4 |
| proxqp   |       1.0 |             1.0 |            1.0 |
| qpoases  | 4502217.8 |   45931216489.9 |        38002.7 |
| qpswift  |  482749.9 |             5.6 |            7.1 |
| quadprog |  439403.4 |             9.6 |            6.4 |
| scs      | 1879523.1 |             2.8 |            2.9 |

Rows are solvers and columns are solver settings. The shift is $sh = 10$. A
solver that fails to find a solution receives a primal residual equal to the
full [primal tolerance](#settings).

#### Dual residual

The dual residual measures the maximum violation of the dual feasibility
condition in the solution returned by a solver. We use the shifted geometric
mean to compare solver dual residuals over the whole test set. Intuitively, a
solver with a shifted-geometric-mean dual residual of Y is Y times less precise
on the dual feasibility condition than the best solver over the test set. See
[Metrics](../README.md#metrics) for details.

Shifted geometric means of dual residuals (1.0 is the best):

|          |    default |   high_accuracy |   low_accuracy |
|:---------|-----------:|----------------:|---------------:|
| cvxopt   |   794862.9 |         13679.2 |           69.2 |
| ecos     |   944595.4 |      32242383.1 |           91.7 |
| gurobi   | 13678400.5 |   74719645507.0 |      1086837.1 |
| highs    |   236646.0 |       3772540.1 |           75.9 |
| osqp     |  3656679.6 |             3.6 |           49.5 |
| proxqp   |        1.0 |             1.0 |            1.0 |
| qpoases  | 23447138.1 |  128509042788.1 |      1265314.8 |
| qpswift  |   794860.4 |             4.9 |           70.2 |
| quadprog |   723489.2 |            17.4 |           63.0 |
| scs      |   371680.3 |             2.6 |           27.2 |

Rows are solvers and columns are solver settings. The shift is $sh = 10$. A
solver that fails to find a solution receives a dual residual equal to the full
[dual tolerance](#settings).

#### Duality gap

The duality gap measures the consistency of the primal and dual solutions
returned by a solver. A duality gap close to zero ensures that the
complementarity slackness optimality condition is satisfied. We use the shifted
geometric mean to compare solver duality gaps over the whole test set.
Intuitively, a solver with a shifted-geometric-mean duality gap of Y is Y times
less precise on the complementarity slackness condition than the best solver
over the test set. See [Metrics](../README.md#metrics) for details.

Shifted geometric means of duality gaps (1.0 is the best):

|          |   default |   high_accuracy |   low_accuracy |
|:---------|----------:|----------------:|---------------:|
| cvxopt   |       2.5 |        201610.2 |            2.3 |
| ecos     |       2.8 |       1008113.0 |            2.4 |
| gurobi   |      71.5 |   44892532683.0 |        55063.1 |
| highs    |       5.7 |    3253828307.1 |         3991.4 |
| osqp     |     348.3 |             3.7 |          373.4 |
| proxqp   |       1.0 |            89.9 |           34.6 |
| qpoases  |       1.5 |             1.7 |            1.3 |
| qpswift  |       2.5 |         48079.4 |            7.2 |
| quadprog |       2.2 |            11.5 |            1.9 |
| scs      |      47.8 |             1.0 |            1.0 |

Rows are solvers and columns are solver settings. The shift is $sh = 10$. A
solver that fails to find a solution receives a duality gap equal to the full
[gap tolerance](#settings).

### Cost error

The cost error measures the difference between the known optimal objective and
the objective at the solution returned by a solver. We use the shifted
geometric mean to compare solver cost errors over the whole test set.
Intuitively, a solver with a shifted-geometric-mean cost error of Y is Y times
less precise on the optimal cost than the best solver over the test set. See
[Metrics](../README.md#metrics) for details.

Shifted geometric means of solver cost errors (1.0 is the best):

|          |   default |   high_accuracy |   low_accuracy |
|:---------|----------:|----------------:|---------------:|
| cvxopt   |     568.0 |           934.7 |          912.9 |
| ecos     |     969.5 |          1595.4 |         1681.0 |
| gurobi   |     123.8 |           203.6 |          198.9 |
| highs    |      35.4 |            58.2 |           56.8 |
| osqp     |     401.5 |           262.2 |          155.4 |
| proxqp   |       1.0 |             1.0 |            1.0 |
| qpoases  |     505.6 |           831.9 |          729.7 |
| qpswift  |     568.0 |           934.7 |          913.1 |
| quadprog |     416.8 |           685.9 |          669.9 |
| scs      |     103.1 |           108.0 |           50.4 |

Rows are solvers and columns are solver settings. The shift is $sh = 10$. A
solver that fails to find a solution receives a cost error equal to the [cost
tolerance](#settings).
