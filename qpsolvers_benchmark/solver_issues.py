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
Some solvers fail on some problems. Make sure we handle and report those.
"""

from typing import Dict, Tuple

from .problem import Problem
from .spdlog import logging


def skip_solver_issue(problem: Problem, solver: str) -> bool:
    """
    Check whether a solver is known to fail at solving a given problem.

    Args:
        problem: Problem to solve.
        solver: QP solver.

    Returns:
        True if solver is known to fail at solving the problem.
    """
    if solver == "proxqp" and problem.name == "QGFRDXPN":
        # https://github.com/Simple-Robotics/proxsuite/issues/63
        return True
    if solver == "highs" and problem.name == "STADAT1":
        # https://github.com/ERGO-Code/HiGHS/issues/995
        return True
    return False


def skip_solver_timeout(
    time_limit: float, problem: Problem, solver: str, settings: str
) -> bool:
    """
    Skip known solver timeouts.

    Args:
        time_limit: Time limit in seconds.
        problem: Problem to solve.
        solver: QP solver.
        settings: QP solver settings.

    Note:
        This function only checks for timeouts that the solvers are not able to
        handle by themselves, e.g. for those who do not provide a time limit
        parameter.

    Returns:
        True if `solver` is known to take more than `time_limit` seconds on
        `problem` when using the solver parameters defined in `settings`.
    """
    minutes = 60.0
    known_timeout_settings: Dict[Tuple[str, str, str], float] = {
        ("AUG2D", "highs", "*"): 40 * minutes,
        ("AUG2DC", "highs", "*"): 40 * minutes,
        ("AUG2DQP", "proxqp", "*"): 30 * minutes,  # 0.3.0
        ("BOYD1", "proxqp", "*"): 30 * minutes,
        ("BOYD2", "proxqp", "*"): 20 * minutes,
        ("CONT-101", "proxqp", "*"): 30 * minutes,
        ("CONT-200", "proxqp", "*"): 20 * minutes,
        ("CONT-201", "proxqp", "*"): 30 * minutes,
        ("CONT-300", "cvxopt", "*"): 20 * minutes,
        ("CONT-300", "highs", "default"): 30 * minutes,
        ("CONT-300", "highs", "high_accuracy"): 30 * minutes,
        ("CONT-300", "proxqp", "*"): 60 * minutes,
        ("CVXQP1_L", "proxqp", "*"): 20 * minutes,
        ("CVXQP3_L", "cvxopt", "*"): 20 * minutes,
        ("CVXQP3_L", "proxqp", "*"): 30 * minutes,
        ("EXDATA", "proxqp", "*"): 30 * minutes,
        ("LISWET1", "proxqp", "*"): 20 * minutes,
        ("LISWET10", "proxqp", "*"): 50 * minutes,
        ("LISWET11", "proxqp", "high_accuracy"): 40 * minutes,
        ("LISWET12", "proxqp", "high_accuracy"): 20 * minutes,
        ("LISWET2", "proxqp", "high_accuracy"): 20 * minutes,
        ("LISWET3", "proxqp", "*"): 30 * minutes,  # 0.3.0
        ("LISWET4", "proxqp", "high_accuracy"): 20 * minutes,
        ("LISWET5", "proxqp", "high_accuracy"): 20 * minutes,
        ("LISWET6", "proxqp", "high_accuracy"): 20 * minutes,
        ("LISWET7", "proxqp", "high_accuracy"): 30 * minutes,
        ("LISWET8", "proxqp", "high_accuracy"): 30 * minutes,
        ("LISWET9", "proxqp", "high_accuracy"): 30 * minutes,
        ("POWELL20", "proxqp", "*"): 30 * minutes,
        ("QGFRDXPN", "proxqp", "*"): 20 * minutes,
        ("QSHIP08L", "proxqp", "*"): 20 * minutes,
        ("QSHIP12L", "proxqp", "*"): 20 * minutes,
        ("STADAT1", "proxqp", "*"): 20 * minutes,
        ("STADAT2", "proxqp", "*"): 20 * minutes,
        ("STADAT3", "proxqp", "*"): 20 * minutes,
        ("UBH1", "proxqp", "*"): 20 * minutes,
        ("YAO", "proxqp", "*"): 20 * minutes,
    }
    timeout = (
        known_timeout_settings[(problem.name, solver, settings)]
        if (problem.name, solver, settings) in known_timeout_settings
        else known_timeout_settings[(problem.name, solver, "*")]
        if (problem.name, solver, "*") in known_timeout_settings
        else 0.0
    )
    if timeout > time_limit:
        logging.warning(
            f"Skipping {problem.name} with {solver} at {settings} "
            f"as it is known to take {timeout} > {time_limit} seconds..."
        )
        return True
    return False
