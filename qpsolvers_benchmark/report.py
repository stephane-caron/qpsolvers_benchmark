#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Report written from test set results.
"""

import datetime
import io
from importlib import metadata
from typing import Dict

import pandas

from .results import Results
from .solver_settings import SolverSettings
from .spdlog import logging
from .test_set import TestSet
from .utils import capitalize_settings, get_cpu_info, get_solver_versions
from .version import get_version


class Report:

    """
    Report generated from benchmark results.

    Attributes:
        author: GitHub username of the person who generated the report.
        results: Results from which the report should be generated.
        solver_settings: Dictionary of solver parameters for each settings.
        test_set: Test set from which results were generated.
    """

    # pylint: disable=R0902
    # Reports are big and linear, thus with many instance attributes.

    __correct_rate_df: pandas.DataFrame
    __cost_df: pandas.DataFrame
    __dual_df: pandas.DataFrame
    __gap_df: pandas.DataFrame
    __primal_df: pandas.DataFrame
    __runtime_df: pandas.DataFrame
    __success_rate_df: pandas.DataFrame
    author: str
    results: Results
    solver_settings: Dict[str, SolverSettings]
    test_set: TestSet

    def __init__(self, author: str, results: Results):
        """
        Initialize report.

        Args:
            author: GitHub username of the person who generated the report.
            results: Results from which the report should be generated.
        """
        self.__correct_rate_df = pandas.DataFrame()
        self.__cost_df = pandas.DataFrame()
        self.__dual_df = pandas.DataFrame()
        self.__gap_df = pandas.DataFrame()
        self.__primal_df = pandas.DataFrame()
        self.__runtime_df = pandas.DataFrame()
        self.__success_rate_df = pandas.DataFrame()
        self.author = author
        self.results = results
        self.solver_settings = results.test_set.solver_settings
        self.test_set = results.test_set

    def get_tolerances_table(self) -> str:
        """
        Get tolerances Markdown table.

        Returns:
            Tolerances Markdown table.
        """
        names = list(self.test_set.tolerances.keys())
        df = pandas.DataFrame(
            [],
            columns=["tolerance"] + names,
        )
        tolerances = ["cost", "primal", "dual", "gap", "runtime"]
        for tolerance in tolerances:
            row = {
                "tolerance": [f"``{tolerance}``"],
            }
            row.update(
                {
                    name: [self.test_set.tolerances[name].__dict__[tolerance]]
                    for name in names
                }
            )
            df = pandas.concat(
                [
                    df,
                    pandas.DataFrame(row),
                ],
                ignore_index=True,
            )
        df = df.sort_values(by="tolerance")
        return df.to_markdown(index=False)

    def get_solver_settings_table(self) -> str:
        """
        Get Markdown table for solver settings.

        Returns:
            Solver settings Markdown table.
        """
        solver_settings = self.test_set.solver_settings
        names = list(solver_settings.keys())
        df = pandas.DataFrame(
            [],
            columns=["solver", "parameter"] + names,
        )
        keys = set()
        for name, settings in solver_settings.items():
            for solver in settings.solvers:
                if solver not in self.test_set.solvers:
                    # Skip solvers that are configured but not in test set
                    continue
                for param in settings[solver]:
                    keys |= {(solver, param)}
        for solver, param in keys:
            row = {
                "solver": [solver],
                "parameter": [
                    f"``{str(param) if isinstance(param, bool) else param}``"
                ],
            }
            row.update(
                {
                    name: [solver_settings[name].get_param(solver, param, "-")]
                    for name in names
                }
            )
            df = pandas.concat(
                [
                    df,
                    pandas.DataFrame(row),
                ],
                ignore_index=True,
            )
        df = df.sort_values(by=["solver", "parameter"])
        return df.to_markdown(index=False)

    def get_solver_versions_table(self):
        """
        Get Markdown table for solver versions.

        Returns:
            Solver versions Markdown table.
        """
        versions = get_solver_versions(self.test_set.solvers)
        versions_df = pandas.DataFrame(
            {
                "solver": list(versions.keys()),
                "version": list(versions.values()),
            },
        )
        versions_df = versions_df.set_index("solver")
        versions_df = versions_df.sort_index()
        versions_table = versions_df.to_markdown(index=True)
        return versions_table

    def __compute_dataframes(self) -> None:
        """
        Compute dataframes used in the report.
        """
        primal_tolerances = {
            name: tolerance.primal
            for name, tolerance in self.test_set.tolerances.items()
        }
        dual_tolerances = {
            name: tolerance.dual
            for name, tolerance in self.test_set.tolerances.items()
        }
        gap_tolerances = {
            name: tolerance.gap
            for name, tolerance in self.test_set.tolerances.items()
        }
        cost_tolerances = {
            name: tolerance.cost
            for name, tolerance in self.test_set.tolerances.items()
        }
        runtime_tolerances = {
            name: tolerance.runtime
            for name, tolerance in self.test_set.tolerances.items()
        }
        self.__success_rate_df = self.results.build_success_rate_df(
            primal_tolerances,
            dual_tolerances,
            gap_tolerances,
            cost_tolerances,
        )
        self.__correct_rate_df = self.results.build_correct_rate_df(
            primal_tolerances,
            dual_tolerances,
            gap_tolerances,
            cost_tolerances,
        )
        self.__runtime_df = self.results.build_shifted_geometric_mean_df(
            column="runtime",
            shift=10.0,
            not_found_values=runtime_tolerances,
        )
        self.__primal_df = self.results.build_shifted_geometric_mean_df(
            column="primal_residual",
            shift=10.0,
            not_found_values=primal_tolerances,
        )
        self.__dual_df = self.results.build_shifted_geometric_mean_df(
            column="dual_residual",
            shift=10.0,
            not_found_values=dual_tolerances,
        )
        self.__gap_df = self.results.build_shifted_geometric_mean_df(
            column="duality_gap",
            shift=10.0,
            not_found_values=gap_tolerances,
        )
        self.__cost_df = self.results.build_shifted_geometric_mean_df(
            column="cost_error",
            shift=10.0,
            not_found_values=cost_tolerances,
        )

    def write(self, path: str) -> None:
        """
        Write report to a given path.

        Args:
            path: Path to the Markdown file to write the report to.

        Note:
            We make sure each table in the report is preceded by a single line
            title, for instance "Precentage of problems each solver is able to
            solve:". This comes in handy for ``@@`` anchorage when doing the
            ``diff`` of two reports.
        """
        assert path.endswith(".md")
        self.__compute_dataframes()
        with open(path, "w", encoding="UTF-8") as fh:
            self.__write_header(fh)
            self.__write_toc(fh)
            self.__write_description(fh)
            self.__write_solvers_section(fh)
            self.__write_settings_section(fh)
            self.__write_results_by_settings(fh)
            self.__write_results_by_metric(fh)
        logging.info(f"Wrote report to {path}")

    def __write_header(self, fh: io.TextIOWrapper) -> None:
        """
        Write report header.

        Args:
            fh: Output file handle.
        """
        benchmark_version = get_version()
        cpu_info = get_cpu_info()
        date = str(datetime.datetime.now(datetime.timezone.utc))
        fh.write(
            f"""# {self.test_set.title}

| Version | {benchmark_version} |
|:--------|:--------------------|
| Date    | {date} |
| CPU     | {cpu_info} |
| Run by  | [@{self.author}](https://github.com/{self.author}/) |

"""
        )

    def __write_toc(self, fh: io.TextIOWrapper) -> None:
        """
        Write table of contents.

        Args:
            fh: Output file handle.
        """
        fh.write("## Contents\n\n")
        if self.test_set.description is not None:
            fh.write("* [Description](#description)\n")
        fh.write(
            """* [Solvers](#solvers)
* [Settings](#settings)
* [Results by settings](#results-by-settings)\n"""
        )
        for name in self.solver_settings:
            link = name.replace("_", "-")
            fh.write(f"    * [{capitalize_settings(name)}](#{link})\n")
        fh.write(
            """* [Results by metric](#results-by-metric)
    * [Success rate](#success-rate)
    * [Computation time](#computation-time)
    * [Optimality conditions](#optimality-conditions)
        * [Primal residual](#primal-residual)
        * [Dual residual](#dual-residual)
        * [Duality gap](#duality-gap)
    * [Cost error](#cost-error)\n\n"""
        )

    def __write_description(self, fh: io.TextIOWrapper) -> None:
        """
        Write optional Description section.

        Args:
            fh: Output file handle.
        """
        if self.test_set.description is not None:
            fh.write(f"## Description\n\n{self.test_set.description}\n\n")

    def __write_solvers_section(self, fh: io.TextIOWrapper) -> None:
        """
        Write Solvers section.

        Args:
            fh: Output file handle.
        """
        qpsolvers_version = metadata.version("qpsolvers")
        fh.write(
            f"""## Solvers

{self.get_solver_versions_table()}

All solvers were called via
[qpsolvers](https://github.com/stephane-caron/qpsolvers)
v{qpsolvers_version}.\n\n"""
        )

    def __write_settings_section(self, fh: io.TextIOWrapper) -> None:
        """
        Write Settings section.

        Args:
            fh: Output file handle.
        """
        italics_settings = [f"*{x}*" for x in self.solver_settings]
        fh.write(
            f"""## Settings

There are {len(italics_settings)} settings: {", ".join(italics_settings[:-1])}
and {italics_settings[-1]}. They validate solutions using the following
tolerances:

{self.get_tolerances_table()}

Solvers for each settings are configured as follows:

{self.get_solver_settings_table()}\n\n"""
        )

    def __write_results_by_settings(self, fh: io.TextIOWrapper) -> None:
        """
        Write Results by settings.

        Args:
            fh: Output file handle.
        """
        fh.write("""## Results by settings\n\n""")
        for settings in self.solver_settings:
            cols = {
                "[Success rate](#success-rate) (%)": self.__success_rate_df[
                    settings
                ],
                "[Runtime](#computation-time) (shm)": self.__runtime_df[
                    settings
                ],
                "[Primal residual](#primal-residual) (shm)": self.__primal_df[
                    settings
                ],
                "[Dual residual](#dual-residual) (shm)": self.__dual_df[
                    settings
                ],
                "[Duality gap](#duality-gap) (shm)": self.__gap_df[settings],
                "[Cost error](#cost-error) (shm)": self.__cost_df[settings],
            }
            df = pandas.DataFrame([], index=self.__gap_df.index).assign(**cols)
            fh.write(
                f"""### {capitalize_settings(settings)}

Solvers are compared over the whole test set by [shifted geometric
mean](../README.md#shifted-geometric-mean) (shm). Lower is better.

{df.to_markdown(index=True, floatfmt=".1f")}\n\n"""
            )

    def __write_results_by_metric(self, fh: io.TextIOWrapper) -> None:
        """
        Write Results by metric.

        Args:
            fh: Output file handle.
        """
        fh.write(
            f"""## Results by metric

### Success rate

Precentage of problems each solver is able to solve:

{self.__success_rate_df.to_markdown(index=True, floatfmt=".0f")}

Rows are [solvers](#solvers) and columns are [settings](#settings). We consider
that a solver successfully solved a problem when (1) it returned with a success
status and (2) its solution satisfies optimality conditions within
[tolerance](#settings). The second table below summarizes the frequency at
which solvers return success (1) and the corresponding solution did indeed pass
tolerance checks.

Percentage of problems where "solved" return codes are correct:

{self.__correct_rate_df.to_markdown(index=True, floatfmt=".0f")}

### Computation time

We compare solver computation times over the whole test set using the shifted
geometric mean. Intuitively, a solver with a shifted-geometric-mean runtime of
Y is Y times slower than the best solver over the test set. See
[Metrics](../README.md#metrics) for details.

Shifted geometric mean of solver computation times (1.0 is the best):

{self.__runtime_df.to_markdown(index=True, floatfmt=".1f")}

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

{self.__primal_df.to_markdown(index=True, floatfmt=".1f")}

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

{self.__dual_df.to_markdown(index=True, floatfmt=".1f")}

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

{self.__gap_df.to_markdown(index=True, floatfmt=".1f")}

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

{self.__cost_df.to_markdown(index=True, floatfmt=".1f")}

Rows are solvers and columns are solver settings. The shift is $sh = 10$. A
solver that fails to find a solution receives a cost error equal to the [cost
tolerance](#settings).
"""
        )
