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
Utility functions.
"""

import platform
from importlib import import_module, metadata
from time import perf_counter
from typing import Set, Tuple

import qpsolvers

from .problem import Problem
from .spdlog import logging

try:
    import cpuinfo
except ImportError:
    cpuinfo = None
    logging.warning(
        "Run ``pip install py-cpuinfo`` for more accurate CPU info"
    )


def capitalize_settings(name: str) -> str:
    """
    Capitalize settings name.

    Args:
        name: Settings name, e.g. "low_accuracy".

    Returns:
        Capitalized settings name to use as column title, e.g. "Low accuracy".
    """
    return name.replace("_", " ").capitalize()


def get_cpu_info() -> str:
    """
    Get CPU information.

    Returns:
        CPU information.
    """
    return (
        platform.processor()
        if cpuinfo is None
        else cpuinfo.get_cpu_info()["brand_raw"]
    )


def get_solver_versions(solvers: Set[str]):
    """
    Get version numbers for a given set of solvers.

    Args:
        solvers: Names of solvers to get the version of.

    Returns:
        Dictionary mapping solver names to their versions.
    """
    package_name = {solver: solver for solver in solvers}
    package_name.update(
        {
            "gurobi": "gurobipy",
            "highs": "highspy",
            "proxqp": "proxsuite",
        }
    )
    versions = {}
    for solver, package in package_name.items():
        try:
            versions[solver] = metadata.version(package)
        except metadata.PackageNotFoundError:
            pass
        if solver in versions:
            continue
        try:
            module = import_module(package)
            versions[solver] = module.__version__
        except AttributeError:
            pass
        except ModuleNotFoundError:
            pass
    if "qpoases" in solvers and "qpoases" not in versions:
        # See https://github.com/coin-or/qpOASES/issues/140
        versions["qpoases"] = "3.2.1"
    if "gurobi" in versions:
        versions["gurobi"] += " (size-limited)"
    return versions


def time_solve_problem(
    problem: Problem, solver: str, **kwargs
) -> Tuple[qpsolvers.Solution, float]:
    """
    Solve quadratic program.

    Args:
        problem: Quadratic program to solve.
        solver: Name of the backend QP solver to call.

    Returns:
        Solution to the quadratic program, along with the time the solver took
        to compute it.
    """
    # Don't time matrix conversions for solvers that require sparse inputs
    if solver in ["highs", "osqp", "scs"]:
        problem = problem.to_sparse()
    start_time = perf_counter()
    try:
        solution = qpsolvers.solve_problem(problem, solver=solver, **kwargs)
    except Exception as e:  # pylint: disable=W0703
        # TODO(scaron): wait for qpsolvers update regarding exceptions
        # See https://github.com/stephane-caron/qpsolvers/pull/139
        logging.warning(f"Caught solver {type(e).__name__} exception: {e}")
        solution = qpsolvers.Solution(problem)
    runtime = perf_counter() - start_time
    return solution, runtime
