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
Base class for test sets.
"""

import abc
from typing import Dict, Iterator, Optional

import qpsolvers

from .exceptions import ProblemNotFound
from .problem import Problem
from .solver_settings import SolverSettings
from .spdlog import logging
from .tolerance import Tolerance


class TestSet(abc.ABC):

    """
    Abstract base class for a test test, i.e. a collection of problems with
    solver settings.

    Attributes:
        solver_settings: Dictionary of solver parameters for each settings.
        tolerances: Validation tolerances.
    """

    solver_settings: Dict[str, SolverSettings]
    tolerances: Dict[str, Tolerance]

    @abc.abstractmethod
    def __iter__(self) -> Iterator[Problem]:
        """
        Yield test problems one by one.
        """

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """
        Test set description.
        """

    @abc.abstractmethod
    def define_tolerances(self) -> None:
        """
        Define validation tolerances.
        """

    def define_solver_settings(self) -> None:
        """
        Define solver settings.
        """
        default = SolverSettings()
        default.set_param("qpoases", "predefined_options", "default")
        default.set_time_limit(self.tolerances["default"].runtime)

        high_accuracy = SolverSettings()
        high_accuracy.set_eps_abs(1e-9)
        high_accuracy.set_eps_rel(0.0)
        high_accuracy.set_param("proxqp", "check_duality_gap", True)
        high_accuracy.set_param("qpoases", "predefined_options", "reliable")
        high_accuracy.set_time_limit(self.tolerances["high_accuracy"].runtime)

        low_accuracy = SolverSettings()
        low_accuracy.set_eps_abs(1e-3)
        low_accuracy.set_eps_rel(0.0)
        low_accuracy.set_param("proxqp", "check_duality_gap", True)
        low_accuracy.set_param("qpoases", "predefined_options", "fast")
        low_accuracy.set_time_limit(self.tolerances["low_accuracy"].runtime)

        self.solver_settings = {
            "default": default,
            "high_accuracy": high_accuracy,
            "low_accuracy": low_accuracy,
        }

    @property
    @abc.abstractmethod
    def sparse_only(self) -> bool:
        """
        If True, test set is restricted to solvers with a sparse matrix API.
        """

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """
        Report title.
        """

    def __init__(self):
        """
        Initialize test set.
        """
        candidate_solvers = set(
            qpsolvers.sparse_solvers
            if self.sparse_only
            else qpsolvers.available_solvers
        )
        solvers = set(
            solver
            for solver in candidate_solvers
            if SolverSettings.is_implemented(solver)
        )
        for solver in candidate_solvers - solvers:
            logging.warning(
                f"Solver '{solver}' is available but skipped "
                "as its settings are unknown"
            )
        self.solver_settings = {}
        self.solvers = solvers
        self.tolerances = {}
        #
        self.define_tolerances()
        self.define_solver_settings()
        self.check_definitions()

    def check_definitions(self):
        """
        Check that settings and tolerance definitions are consistent.

        Raises:
            ValueError: in case of inconsistency.
        """
        tolerances = set(self.tolerances.keys())
        settings = set(self.solver_settings.keys())
        if tolerances != settings:
            logging.error("Settings are not consistent with tolerances")
            logging.info(f"Settings: {settings}")
            logging.info(f"Tolerances: {tolerances}")
            raise ValueError("Settings are not consistent with tolerances")

    def get_problem(self, name: str) -> Optional[Problem]:
        """
        Get a specific test set problem.

        Args:
            name: Problem name.

        Returns:
            Problem if found, None otherwise.
        """
        for problem in self:
            if problem.name == name:
                return problem
        set_name = str(self.__class__.__name__)
        problem_names = "\n- ".join(problem.name for problem in self)
        logging.info(
            "Problems in the %s test set:\n- %s\n"
            "Requested problem is not one of them",
            set_name,
            problem_names,
        )
        raise ProblemNotFound(
            f"problem '{name}' not found "
            f"in the {self.__class__.__name__} test set"
        )
