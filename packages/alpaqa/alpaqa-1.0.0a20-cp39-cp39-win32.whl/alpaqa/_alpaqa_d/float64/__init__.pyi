"""
Double precision
"""
from __future__ import annotations
import alpaqa._alpaqa_d
import datetime
import numpy
import typing
from . import functions
__all__ = ['ALMParams', 'ALMSolver', 'AndersonAccel', 'AndersonDirection', 'Box', 'BoxConstrProblem', 'CasADiControlProblem', 'CasADiProblem', 'ControlProblem', 'ControlProblemWithCounters', 'ConvexNewtonDirection', 'DLProblem', 'FISTAParams', 'FISTAProgressInfo', 'FISTASolver', 'InnerOCPSolver', 'InnerSolveOptions', 'InnerSolver', 'KKTError', 'LBFGS', 'LBFGSDirection', 'LipschitzEstimateParams', 'NewtonTRDirection', 'NewtonTRDirectionParams', 'NoopDirection', 'OCPEvaluator', 'PANOCDirection', 'PANOCOCPParams', 'PANOCOCPProgressInfo', 'PANOCOCPSolver', 'PANOCParams', 'PANOCProgressInfo', 'PANOCSolver', 'PANTRDirection', 'PANTRParams', 'PANTRProgressInfo', 'PANTRSolver', 'Problem', 'ProblemWithCounters', 'SteihaugCGParams', 'StructuredLBFGSDirection', 'StructuredNewtonDirection', 'UnconstrProblem', 'ZeroFPRParams', 'ZeroFPRProgressInfo', 'ZeroFPRSolver', 'control_problem_with_counters', 'deserialize_casadi_problem', 'functions', 'kkt_error', 'load_casadi_control_problem', 'load_casadi_problem', 'problem_with_counters', 'provided_functions', 'prox', 'prox_step']
M = typing.TypeVar("M", bound=int)
N = typing.TypeVar("N", bound=int)
class ALMParams:
    """
    C++ documentation: :cpp:class:`alpaqa::ALMParams`
    """
    dual_tolerance: float
    initial_penalty: float
    initial_penalty_factor: float
    initial_tolerance: float
    max_iter: int
    max_multiplier: float
    max_penalty: float
    max_time: datetime.timedelta
    min_penalty: float
    penalty_update_factor: float
    print_interval: int
    print_precision: int
    rel_penalty_increase_threshold: float
    single_penalty_factor: bool
    tolerance: float
    tolerance_update_factor: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class ALMSolver:
    """
    Main augmented Lagrangian solver.
    
    C++ documentation: :cpp:class:`alpaqa::ALMSolver`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __call__(self, problem: Problem | ControlProblem, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple:
        """
        Solve.
        
        :param problem: Problem to solve.
        :param x: Initial guess for decision variables :math:`x`
        
        :param y: Initial guess for Lagrange multipliers :math:`y`
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`x`
                 * Lagrange multipliers :math:`y` at the solution
                 * Statistics
        """
    def __copy__(self) -> ALMSolver:
        ...
    def __deepcopy__(self, memo: dict) -> ALMSolver:
        ...
    @typing.overload
    def __init__(self, other: ALMSolver) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Build an ALM solver using Structured PANOC as inner solver.
        """
    @typing.overload
    def __init__(self, inner_solver: InnerSolver) -> None:
        """
        Build an ALM solver using the given inner solver.
        """
    @typing.overload
    def __init__(self, inner_solver: InnerOCPSolver) -> None:
        """
        Build an ALM solver using the given inner solver.
        """
    @typing.overload
    def __init__(self, alm_params: ALMParams | dict, inner_solver: InnerSolver) -> None:
        """
        Build an ALM solver using the given inner solver.
        """
    @typing.overload
    def __init__(self, alm_params: ALMParams | dict, inner_solver: InnerOCPSolver) -> None:
        """
        Build an ALM solver using the given inner solver.
        """
    def __str__(self) -> str:
        ...
    def stop(self) -> None:
        ...
    @property
    def inner_solver(self) -> typing.Any:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def params(self) -> typing.Any:
        ...
class AndersonAccel:
    """
    C++ documentation :cpp:class:`alpaqa::AndersonAccel`
    """
    class Params:
        """
        C++ documentation :cpp:class:`alpaqa::AndersonAccelParams`
        """
        memory: int
        min_div_fac: float
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        @typing.overload
        def __init__(self, params: dict) -> None:
            ...
        @typing.overload
        def __init__(self, **kwargs) -> None:
            ...
        def to_dict(self) -> dict:
            ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: AndersonAccel.Params | dict) -> None:
        ...
    @typing.overload
    def __init__(self, params: AndersonAccel.Params | dict, n: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @typing.overload
    def compute(self, g_k: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], r_k: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], x_k_aa: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def compute(self, g_k: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], r_k: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def initialize(self, g_0: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], r_0: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def reset(self) -> None:
        ...
    def resize(self, n: int) -> None:
        ...
    @property
    def Q(self) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]:
        ...
    @property
    def R(self) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]:
        ...
    @property
    def current_history(self) -> int:
        ...
    @property
    def history(self) -> int:
        ...
    @property
    def n(self) -> int:
        ...
    @property
    def params(self) -> AndersonAccel.Params:
        ...
class AndersonDirection:
    """
    C++ documentation: :cpp:class:`alpaqa::AndersonDirection`
    """
    class DirectionParams:
        """
        C++ documentation: :cpp:class:`alpaqa::AndersonDirection::DirectionParams`
        """
        rescale_on_step_size_changes: bool
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        @typing.overload
        def __init__(self, params: dict) -> None:
            ...
        @typing.overload
        def __init__(self, **kwargs) -> None:
            ...
        def to_dict(self) -> dict:
            ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, anderson_params: AndersonAccel.Params | dict = {}, direction_params: AndersonDirection.DirectionParams | dict = {}) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def params(self) -> tuple[AndersonAccel.Params, AndersonDirection.DirectionParams]:
        ...
class Box:
    """
    C++ documentation: :cpp:class:`alpaqa::Box`
    """
    lowerbound: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]
    upperbound: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> Box:
        ...
    def __deepcopy__(self, memo: dict) -> Box:
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, other: Box) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, n: int) -> None:
        """
        Create an :math:`n`-dimensional box at with bounds at :math:`\\pm\\infty` (no constraints).
        """
    @typing.overload
    def __init__(self, *, lower: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], upper: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        """
        Create a box with the given bounds.
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
class BoxConstrProblem:
    """
    C++ documentation: :cpp:class:`alpaqa::BoxConstrProblem`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> BoxConstrProblem:
        ...
    def __deepcopy__(self, memo: dict) -> BoxConstrProblem:
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, other: BoxConstrProblem) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, n: int, m: int) -> None:
        """
        :param n: Number of unknowns
        :param m: Number of constraints
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], J: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]) -> int:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]:
        ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], e: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_proj_multipliers(self, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], M: float) -> None:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], x_hat: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], p: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], float]:
        ...
    def get_box_C(self) -> Box:
        ...
    def get_box_D(self) -> Box:
        ...
    def resize(self, n: int, m: int) -> None:
        ...
    @property
    def C(self) -> Box:
        """
        Box constraints on :math:`x`
        """
    @C.setter
    def C(self, arg0: Box) -> None:
        ...
    @property
    def D(self) -> Box:
        """
        Box constraints on :math:`g(x)`
        """
    @D.setter
    def D(self, arg0: Box) -> None:
        ...
    @property
    def l1_reg(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        :math:`\\ell_1` regularization on :math:`x`
        """
    @l1_reg.setter
    def l1_reg(self, arg0: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @property
    def m(self) -> int:
        """
        Number of general constraints, dimension of :math:`g(x)`
        """
    @property
    def n(self) -> int:
        """
        Number of decision variables, dimension of :math:`x`
        """
    @property
    def penalty_alm_split(self) -> int:
        """
        Index between quadratic penalty and augmented Lagrangian constraints
        """
    @penalty_alm_split.setter
    def penalty_alm_split(self, arg0: int) -> None:
        ...
class CasADiControlProblem:
    """
    C++ documentation: :cpp:class:`alpaqa::CasADiControlProblem`
    
    See :py:class:`alpaqa.ControlProblem` for the full documentation.
    """
    D: Box
    D_N: Box
    U: Box
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> CasADiControlProblem:
        ...
    def __deepcopy__(self, memo: dict) -> CasADiControlProblem:
        ...
    def __init__(self, other: CasADiControlProblem) -> None:
        """
        Create a copy
        """
    @property
    def N(self) -> int:
        ...
    @property
    def nc(self) -> int:
        ...
    @property
    def nc_N(self) -> int:
        ...
    @property
    def nh(self) -> int:
        ...
    @property
    def nh_N(self) -> int:
        ...
    @property
    def nu(self) -> int:
        ...
    @property
    def nx(self) -> int:
        ...
    @property
    def param(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Parameter vector :math:`p` of the problem
        """
    @param.setter
    def param(self, arg1: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @property
    def x_init(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Initial state vector :math:`x^0` of the problem
        """
    @x_init.setter
    def x_init(self, arg1: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
class CasADiProblem(BoxConstrProblem):
    """
    C++ documentation: :cpp:class:`alpaqa::CasADiProblem`
    
    See :py:class:`alpaqa.Problem` for the full documentation.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> CasADiProblem:
        ...
    def __deepcopy__(self, memo: dict) -> CasADiProblem:
        ...
    def __init__(self, other: CasADiProblem) -> None:
        """
        Create a copy
        """
    def __str__(self) -> str:
        ...
    def check(self) -> None:
        ...
    def eval_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_f_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_fx: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_f_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple:
        ...
    @typing.overload
    def eval_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], gx: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_grad_L(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_L: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_n: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_fx: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    @typing.overload
    def eval_grad_g_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_gxy: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_g_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_grad_gi(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], i: int, grad_gi: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_n: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_m: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_hess_L(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float = 1.0) -> tuple[typing.Any, alpaqa._alpaqa_d.Symmetry]:
        """
        Returns the Hessian of the Lagrangian and its symmetry.
        """
    def eval_hess_L_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float, v: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Hv: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def eval_hess_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float = 1.0) -> tuple[typing.Any, alpaqa._alpaqa_d.Symmetry]:
        """
        Returns the Hessian of the augmented Lagrangian and its symmetry.
        """
    def eval_hess_ψ_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float, v: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Hv: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], J: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]) -> int:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]:
        ...
    def eval_jac_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[typing.Any, alpaqa._alpaqa_d.Symmetry]:
        """
        Returns the Jacobian of the constraints and its symmetry.
        """
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], e: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_proj_multipliers(self, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], M: float) -> None:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], x_hat: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], p: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], float]:
        ...
    @typing.overload
    def eval_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], ŷ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[float, numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]]:
        ...
    @typing.overload
    def eval_ψ_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_n: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_m: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_ψ_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[float, numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]]:
        ...
    def get_box_C(self) -> Box:
        ...
    def get_box_D(self) -> Box:
        ...
    def provides_eval_grad_L(self) -> bool:
        ...
    def provides_eval_grad_gi(self) -> bool:
        ...
    def provides_eval_grad_ψ(self) -> bool:
        ...
    def provides_eval_hess_L(self) -> bool:
        ...
    def provides_eval_hess_L_prod(self) -> bool:
        ...
    def provides_eval_hess_ψ(self) -> bool:
        ...
    def provides_eval_hess_ψ_prod(self) -> bool:
        ...
    def provides_eval_jac_g(self) -> bool:
        ...
    def provides_eval_ψ(self) -> bool:
        ...
    def provides_eval_ψ_grad_ψ(self) -> bool:
        ...
    def provides_get_box_C(self) -> bool:
        ...
    @property
    def m(self) -> int:
        """
        Number of general constraints, dimension of :math:`g(x)`
        """
    @property
    def n(self) -> int:
        """
        Number of decision variables, dimension of :math:`x`
        """
    @property
    def param(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Parameter vector :math:`p` of the problem
        """
    @param.setter
    def param(self, arg1: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
class ControlProblem:
    """
    C++ documentation: :cpp:class:`alpaqa::TypeErasedControlProblem`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> ControlProblem:
        ...
    def __deepcopy__(self, memo: dict) -> ControlProblem:
        ...
    @typing.overload
    def __init__(self, other: ControlProblem) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, problem: CasADiControlProblem) -> None:
        """
        Explicit conversion
        """
class ControlProblemWithCounters:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def evaluations(self) -> alpaqa._alpaqa_d.OCPEvalCounter:
        ...
    @property
    def problem(self) -> ControlProblem:
        ...
class ConvexNewtonDirection:
    """
    C++ documentation: :cpp:class:`alpaqa::ConvexNewtonDirection`
    """
    class AcceleratorParams:
        """
        C++ documentation: :cpp:class:`alpaqa::ConvexNewtonDirection::AcceleratorParams`
        """
        ldlt: bool
        ζ: float
        ν: float
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        @typing.overload
        def __init__(self, params: dict) -> None:
            ...
        @typing.overload
        def __init__(self, **kwargs) -> None:
            ...
        def to_dict(self) -> dict:
            ...
    class DirectionParams:
        """
        C++ documentation: :cpp:class:`alpaqa::ConvexNewtonDirection::DirectionParams`
        """
        hessian_vec_factor: float
        quadratic: bool
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        @typing.overload
        def __init__(self, params: dict) -> None:
            ...
        @typing.overload
        def __init__(self, **kwargs) -> None:
            ...
        def to_dict(self) -> dict:
            ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, newton_params: ConvexNewtonDirection.AcceleratorParams | dict = {}, direction_params: ConvexNewtonDirection.DirectionParams | dict = {}) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def params(self) -> ConvexNewtonDirection.DirectionParams:
        ...
class DLProblem(BoxConstrProblem):
    """
    C++ documentation: :cpp:class:`alpaqa::dl::DLProblem`
    
    See :py:class:`alpaqa.Problem` for the full documentation.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> DLProblem:
        ...
    def __deepcopy__(self, memo: dict) -> DLProblem:
        ...
    @typing.overload
    def __init__(self, so_filename: str, *args, function_name: str = 'register_alpaqa_problem', user_param_str: bool = False, **kwargs) -> None:
        """
        Load a problem from the given shared library file.
        By default, extra arguments are passed to the problem as a void pointer to a ``std::tuple<pybind11::args, pybind11::kwargs>``.
        If the keyword argument ``user_param_str=True`` is used, the ``args`` is converted to a list of strings, and passed as a void pointer to a ``std::span<std::string_view>``.
        """
    @typing.overload
    def __init__(self, other: DLProblem) -> None:
        """
        Create a copy
        """
    def __str__(self) -> str:
        ...
    def call_extra_func(self, name: str, *args, **kwargs) -> typing.Any:
        """
        Call the given extra member function registered by the problem, with the signature ``pybind11::object(pybind11::args, pybind11::kwargs)``.
        """
    def check(self) -> None:
        ...
    def eval_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    def eval_f_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], g: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_f_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_fx: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_f_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple:
        ...
    @typing.overload
    def eval_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], gx: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_grad_L(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_L: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_n: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_fx: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_grad_f_grad_g_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_f: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_gxy: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_g_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_gxy: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_g_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_grad_gi(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], i: int, grad_gi: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_n: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_m: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_hess_L(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float = 1.0) -> tuple[typing.Any, alpaqa._alpaqa_d.Symmetry]:
        """
        Returns the Hessian of the Lagrangian and its symmetry.
        """
    def eval_hess_L_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float, v: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Hv: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def eval_hess_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float = 1.0) -> tuple[typing.Any, alpaqa._alpaqa_d.Symmetry]:
        """
        Returns the Hessian of the augmented Lagrangian and its symmetry.
        """
    def eval_hess_ψ_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float, v: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Hv: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], J: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]) -> int:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]:
        ...
    def eval_jac_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[typing.Any, alpaqa._alpaqa_d.Symmetry]:
        """
        Returns the Jacobian of the constraints and its symmetry.
        """
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], e: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_proj_multipliers(self, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], M: float) -> None:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], x_hat: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], p: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], float]:
        ...
    @typing.overload
    def eval_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], ŷ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[float, numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]]:
        ...
    @typing.overload
    def eval_ψ_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_n: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_m: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_ψ_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[float, numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]]:
        ...
    def get_box_C(self) -> Box:
        ...
    def get_box_D(self) -> Box:
        ...
    def provides_eval_f_g(self) -> bool:
        ...
    def provides_eval_f_grad_f(self) -> bool:
        ...
    def provides_eval_grad_L(self) -> bool:
        ...
    def provides_eval_grad_f_grad_g_prod(self) -> bool:
        ...
    def provides_eval_grad_gi(self) -> bool:
        ...
    def provides_eval_grad_ψ(self) -> bool:
        ...
    def provides_eval_hess_L(self) -> bool:
        ...
    def provides_eval_hess_L_prod(self) -> bool:
        ...
    def provides_eval_hess_ψ(self) -> bool:
        ...
    def provides_eval_hess_ψ_prod(self) -> bool:
        ...
    def provides_eval_inactive_indices_res_lna(self) -> bool:
        ...
    def provides_eval_jac_g(self) -> bool:
        ...
    def provides_eval_ψ(self) -> bool:
        ...
    def provides_eval_ψ_grad_ψ(self) -> bool:
        ...
    def provides_get_box_C(self) -> bool:
        ...
    def provides_get_box_D(self) -> bool:
        ...
    def provides_get_hess_L_sparsity(self) -> bool:
        ...
    def provides_get_hess_ψ_sparsity(self) -> bool:
        ...
    def provides_get_jac_g_sparsity(self) -> bool:
        ...
    @property
    def m(self) -> int:
        """
        Number of general constraints, dimension of :math:`g(x)`
        """
    @property
    def n(self) -> int:
        """
        Number of decision variables, dimension of :math:`x`
        """
class FISTAParams:
    """
    C++ documentation: :cpp:class:`alpaqa::FISTAParams`
    """
    L_max: float
    L_min: float
    Lipschitz: LipschitzEstimateParams
    disable_acceleration: bool
    max_iter: int
    max_no_progress: int
    max_time: datetime.timedelta
    print_interval: int
    print_precision: int
    quadratic_upperbound_tolerance_factor: float
    stop_crit: alpaqa._alpaqa_d.PANOCStopCrit
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class FISTAProgressInfo:
    """
    Data passed to the FISTA progress callback.
    
    C++ documentation: :cpp:class:`alpaqa::FISTAProgressInfo`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def L(self) -> float:
        """
        Estimate of Lipschitz constant of objective :math:`L`
        """
    @property
    def fpr(self) -> float:
        """
        Fixed-point residual :math:`\\left\\|p\\right\\| / \\gamma`
        """
    @property
    def grad_ψ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Gradient of objective :math:`\\nabla\\psi(x)`
        """
    @property
    def grad_ψ_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Gradient of objective at x̂ :math:`\\nabla\\psi(\\hat x)`
        """
    @property
    def k(self) -> int:
        """
        Iteration
        """
    @property
    def norm_sq_p(self) -> float:
        """
        :math:`\\left\\|p\\right\\|^2`
        """
    @property
    def p(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Projected gradient step :math:`p`
        """
    @property
    def params(self) -> FISTAParams:
        """
        Solver parameters
        """
    @property
    def problem(self) -> Problem:
        """
        Problem being solved
        """
    @property
    def status(self) -> alpaqa._alpaqa_d.SolverStatus:
        """
        Current solver status
        """
    @property
    def t(self) -> float:
        """
        Acceleration parameter :math:`t`
        """
    @property
    def x(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Decision variable :math:`x`
        """
    @property
    def x_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Decision variable after projected gradient step :math:`\\hat x`
        """
    @property
    def y(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Lagrange multipliers :math:`y`
        """
    @property
    def y_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Candidate updated multipliers at x̂ :math:`\\hat y(\\hat x)`
        """
    @property
    def Σ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Penalty factor :math:`\\Sigma`
        """
    @property
    def γ(self) -> float:
        """
        Step size :math:`\\gamma`
        """
    @property
    def ε(self) -> float:
        """
        Tolerance reached :math:`\\varepsilon_k`
        """
    @property
    def φγ(self) -> float:
        """
        Forward-backward envelope :math:`\\varphi_\\gamma(x)`
        """
    @property
    def ψ(self) -> float:
        """
        Objective value :math:`\\psi(x)`
        """
    @property
    def ψ_hat(self) -> float:
        """
        Objective at x̂ :math:`\\psi(\\hat x)`
        """
class FISTASolver:
    """
    C++ documentation: :cpp:class:`alpaqa::FISTASolver`
    """
    Params = FISTAParams
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __call__(self, problem: Problem, opts: InnerSolveOptions = {}, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple:
        """
        Solve the given problem.
        
        :param problem: Problem to solve
        :param opts: Options (such as desired tolerance)
        :param x: Optional initial guess for the decision variables
        :param y: Lagrange multipliers (when used as ALM inner solver)
        :param Σ: Penalty factors (when used as ALM inner solver)
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`x`
                 * Updated Lagrange multipliers (only if parameter ``y`` was not ``None``)
                 * Constraint violation (only if parameter ``y`` was not ``None``)
                 * Statistics
        """
    def __copy__(self) -> FISTASolver:
        ...
    def __deepcopy__(self, memo: dict) -> FISTASolver:
        ...
    @typing.overload
    def __init__(self, other: FISTASolver) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, fista_params: FISTAParams | dict = {}) -> None:
        """
        Create a FISTA solver using structured L-BFGS directions.
        """
    def __str__(self) -> str:
        ...
    def set_progress_callback(self, callback: typing.Callable[[FISTAProgressInfo], None]) -> FISTASolver:
        """
        Specify a callable that is invoked with some intermediate results on each iteration of the algorithm.
        """
    def stop(self) -> None:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def params(self) -> FISTAParams:
        ...
class InnerOCPSolver:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> InnerOCPSolver:
        ...
    def __deepcopy__(self, memo: dict) -> InnerOCPSolver:
        ...
    @typing.overload
    def __init__(self, other: InnerOCPSolver) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, inner_solver: PANOCOCPSolver) -> None:
        """
        Explicit conversion.
        """
    def __str__(self) -> str:
        ...
    def stop(self) -> None:
        ...
    @property
    def name(self) -> str:
        ...
class InnerSolveOptions:
    always_overwrite_results: bool
    max_time: datetime.timedelta | None
    tolerance: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class InnerSolver:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> InnerSolver:
        ...
    def __deepcopy__(self, memo: dict) -> InnerSolver:
        ...
    @typing.overload
    def __init__(self, other: InnerSolver) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, inner_solver: PANOCSolver) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, inner_solver: FISTASolver) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, inner_solver: ZeroFPRSolver) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, inner_solver: PANTRSolver) -> None:
        """
        Explicit conversion.
        """
    def __str__(self) -> str:
        ...
    def stop(self) -> None:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def params(self) -> typing.Any:
        ...
class KKTError:
    """
    C++ documentation: :cpp:class:`alpaqa::KKTError`
    """
    bounds_violation: float
    complementarity: float
    constr_violation: float
    stationarity: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class LBFGS:
    """
    C++ documentation :cpp:class:`alpaqa::LBFGS`
    """
    class Params:
        """
        C++ documentation :cpp:class:`alpaqa::LBFGSParams`
        """
        class CBFGS:
            """
            C++ documentation :cpp:class:`alpaqa::CBFGSParams`
            """
            α: float
            ϵ: float
            @staticmethod
            def _pybind11_conduit_v1_(*args, **kwargs):
                ...
            @typing.overload
            def __init__(self, params: dict) -> None:
                ...
            @typing.overload
            def __init__(self, **kwargs) -> None:
                ...
            def to_dict(self) -> dict:
                ...
        cbfgs: LBFGS.Params.CBFGS
        force_pos_def: bool
        memory: int
        min_abs_s: float
        min_div_fac: float
        stepsize: alpaqa._alpaqa_d.LBFGSStepsize
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        @typing.overload
        def __init__(self, params: dict) -> None:
            ...
        @typing.overload
        def __init__(self, **kwargs) -> None:
            ...
        def to_dict(self) -> dict:
            ...
    class Sign:
        """
        C++ documentation :cpp:enum:`alpaqa::LBFGS::Sign`
        
        Members:
        
          Positive
        
          Negative
        """
        Negative: typing.ClassVar[LBFGS.Sign]  # value = <Sign.Negative: 1>
        Positive: typing.ClassVar[LBFGS.Sign]  # value = <Sign.Positive: 0>
        __members__: typing.ClassVar[dict[str, LBFGS.Sign]]  # value = {'Positive': <Sign.Positive: 0>, 'Negative': <Sign.Negative: 1>}
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Negative: typing.ClassVar[LBFGS.Sign]  # value = <Sign.Negative: 1>
    Positive: typing.ClassVar[LBFGS.Sign]  # value = <Sign.Positive: 0>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def update_valid(params: LBFGS.Params, yᵀs: float, sᵀs: float, pᵀp: float) -> bool:
        ...
    @typing.overload
    def __init__(self, params: LBFGS.Params | dict) -> None:
        ...
    @typing.overload
    def __init__(self, params: LBFGS.Params | dict, n: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    def apply(self, q: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], γ: float) -> bool:
        ...
    def apply_masked(self, q: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], γ: float, J: list[int]) -> bool:
        ...
    def current_history(self) -> int:
        ...
    def reset(self) -> None:
        ...
    def resize(self, n: int) -> None:
        ...
    def s(self, i: int) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def scale_y(self, factor: float) -> None:
        ...
    def update(self, xk: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], xkp1: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], pk: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], pkp1: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], sign: LBFGS.Sign = LBFGS.Sign.Positive, forced: bool = False) -> bool:
        ...
    def update_sy(self, sk: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], yk: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], pkp1Tpkp1: float, forced: bool = False) -> bool:
        ...
    def y(self, i: int) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def α(self, i: int) -> float:
        ...
    def ρ(self, i: int) -> float:
        ...
    @property
    def n(self) -> int:
        ...
    @property
    def params(self) -> LBFGS.Params:
        ...
class LBFGSDirection:
    """
    C++ documentation: :cpp:class:`alpaqa::LBFGSDirection`
    """
    class DirectionParams:
        """
        C++ documentation: :cpp:class:`alpaqa::LBFGSDirection::DirectionParams`
        """
        rescale_on_step_size_changes: bool
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        @typing.overload
        def __init__(self, params: dict) -> None:
            ...
        @typing.overload
        def __init__(self, **kwargs) -> None:
            ...
        def to_dict(self) -> dict:
            ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, lbfgs_params: LBFGS.Params | dict = {}, direction_params: LBFGSDirection.DirectionParams | dict = {}) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def params(self) -> tuple[LBFGS.Params, LBFGSDirection.DirectionParams]:
        ...
class LipschitzEstimateParams:
    """
    C++ documentation: :cpp:class:`alpaqa::LipschitzEstimateParams`
    """
    L_0: float
    Lγ_factor: float
    δ: float
    ε: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class NewtonTRDirection:
    """
    C++ documentation: :cpp:class:`alpaqa::NewtonTRDirection`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, accelerator_params: SteihaugCGParams | dict = {}, direction_params: NewtonTRDirectionParams | dict = {}) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def params(self) -> tuple[SteihaugCGParams, NewtonTRDirectionParams]:
        ...
class NewtonTRDirectionParams:
    """
    C++ documentation: :cpp:class:`alpaqa::NewtonTRDirectionParams`
    """
    finite_diff: bool
    finite_diff_stepsize: float
    hessian_vec_factor: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class NoopDirection:
    """
    C++ documentation: :cpp:class:`alpaqa::NoopDirection`
    """
    AcceleratorParams = None
    DirectionParams = None
    params = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def __str__(self) -> str:
        ...
class OCPEvaluator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Qk(self, k: int, u: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, μ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]:
        ...
    def Rk(self, k: int, u: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], mask: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]:
        ...
    def Sk(self, k: int, u: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], mask: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]:
        ...
    def __init__(self, problem: ControlProblem) -> None:
        ...
    def forward_backward(self, u: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, μ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None) -> tuple[float, numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]]:
        """
        :return: * Cost
                 * Gradient
        """
    def lqr_factor_solve(self, u: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], γ: float, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, μ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def lqr_factor_solve_QRS(self, u: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], γ: float, Q: list, R: list, S: list, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, μ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, masked: bool = True) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
class PANOCDirection:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, direction: NoopDirection) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, direction: LBFGSDirection) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, direction: StructuredLBFGSDirection) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, direction: StructuredNewtonDirection) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, direction: ConvexNewtonDirection) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, direction: AndersonDirection) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, direction: typing.Any) -> None:
        """
        Explicit conversion from a custom Python class.
        """
    def __str__(self) -> str:
        ...
    @property
    def params(self) -> typing.Any:
        ...
class PANOCOCPParams:
    """
    C++ documentation: :cpp:class:`alpaqa::PANOCOCPParams`
    """
    L_max: float
    L_max_inc: int
    L_min: float
    Lipschitz: LipschitzEstimateParams
    disable_acceleration: bool
    gn_interval: int
    gn_sticky: bool
    lbfgs_params: LBFGS.Params
    linesearch_strictness_factor: float
    linesearch_tolerance_factor: float
    lqr_factor_cholesky: bool
    max_iter: int
    max_no_progress: int
    max_time: datetime.timedelta
    min_linesearch_coefficient: float
    print_interval: int
    print_precision: int
    quadratic_upperbound_tolerance_factor: float
    reset_lbfgs_on_gn_step: bool
    stop_crit: alpaqa._alpaqa_d.PANOCStopCrit
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class PANOCOCPProgressInfo:
    """
    Data passed to the PANOC progress callback.
    
    C++ documentation: :cpp:class:`alpaqa::PANOCOCPProgressInfo`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def L(self) -> float:
        """
        Estimate of Lipschitz constant of objective :math:`L`
        """
    @property
    def fpr(self) -> float:
        """
        Fixed-point residual :math:`\\left\\|p\\right\\| / \\gamma`
        """
    @property
    def gn(self) -> bool:
        """
        Was :math:`q` a Gauss-Newton or L-BFGS step?
        """
    @property
    def grad_ψ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Gradient of objective :math:`\\nabla\\psi(u)`
        """
    @property
    def k(self) -> int:
        """
        Iteration
        """
    @property
    def lqr_min_rcond(self) -> float:
        """
        Minimum reciprocal condition number encountered in LQR factorization
        """
    @property
    def nJ(self) -> int:
        """
        Number of inactive constraints :math:`\\#\\mathcal J`
        """
    @property
    def norm_sq_p(self) -> float:
        """
        :math:`\\left\\|p\\right\\|^2`
        """
    @property
    def p(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Projected gradient step :math:`p`
        """
    @property
    def params(self) -> PANOCOCPParams:
        """
        Solver parameters
        """
    @property
    def problem(self) -> ControlProblem:
        """
        Problem being solved
        """
    @property
    def q(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Previous accelerated step :math:`q`
        """
    @property
    def status(self) -> alpaqa._alpaqa_d.SolverStatus:
        """
        Current solver status
        """
    @property
    def u(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Inputs
        """
    @property
    def u_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Inputs after projected gradient step
        """
    @property
    def x(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        States
        """
    @property
    def x_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        States after projected gradient step
        """
    @property
    def xu(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        States :math:`x` and inputs :math:`u`
        """
    @property
    def xu_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Variables after projected gradient step :math:`\\hat u`
        """
    @property
    def γ(self) -> float:
        """
        Step size :math:`\\gamma`
        """
    @property
    def ε(self) -> float:
        """
        Tolerance reached :math:`\\varepsilon_k`
        """
    @property
    def τ(self) -> float:
        """
        Line search parameter :math:`\\tau`
        """
    @property
    def φγ(self) -> float:
        """
        Forward-backward envelope :math:`\\varphi_\\gamma(u)`
        """
    @property
    def ψ(self) -> float:
        """
        Objective value :math:`\\psi(u)`
        """
    @property
    def ψ_hat(self) -> float:
        """
        Objective at x̂ :math:`\\psi(\\hat u)`
        """
class PANOCOCPSolver:
    """
    C++ documentation: :cpp:class:`alpaqa::PANOCOCPSolver`
    """
    Params = PANOCOCPParams
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __call__(self, problem: ControlProblem, opts: InnerSolveOptions = {}, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple:
        """
        Solve the given problem.
        
        :param problem: Problem to solve
        :param opts: Options (such as desired tolerance)
        :param x: Optional initial guess for the decision variables
        :param y: Lagrange multipliers (when used as ALM inner solver)
        :param Σ: Penalty factors (when used as ALM inner solver)
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`x`
                 * Updated Lagrange multipliers (only if parameter ``y`` was not ``None``)
                 * Constraint violation (only if parameter ``y`` was not ``None``)
                 * Statistics
        """
    def __copy__(self) -> PANOCOCPSolver:
        ...
    def __deepcopy__(self, memo: dict) -> PANOCOCPSolver:
        ...
    @typing.overload
    def __init__(self, other: PANOCOCPSolver) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, panoc_params: PANOCOCPParams | dict) -> None:
        """
        Create a PANOC solver.
        """
    def __str__(self) -> str:
        ...
    def set_progress_callback(self, callback: typing.Callable[[PANOCOCPProgressInfo], None]) -> PANOCOCPSolver:
        """
        Specify a callable that is invoked with some intermediate results on each iteration of the algorithm.
        """
    def stop(self) -> None:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def params(self) -> PANOCOCPParams:
        ...
class PANOCParams:
    """
    C++ documentation: :cpp:class:`alpaqa::PANOCParams`
    """
    L_max: float
    L_min: float
    Lipschitz: LipschitzEstimateParams
    eager_gradient_eval: bool
    force_linesearch: bool
    linesearch_coefficient_update_factor: float
    linesearch_strictness_factor: float
    linesearch_tolerance_factor: float
    max_iter: int
    max_no_progress: int
    max_time: datetime.timedelta
    min_linesearch_coefficient: float
    print_interval: int
    print_precision: int
    quadratic_upperbound_tolerance_factor: float
    recompute_last_prox_step_after_stepsize_change: bool
    stop_crit: alpaqa._alpaqa_d.PANOCStopCrit
    update_direction_in_candidate: bool
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class PANOCProgressInfo:
    """
    Data passed to the PANOC progress callback.
    
    C++ documentation: :cpp:class:`alpaqa::PANOCProgressInfo`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def L(self) -> float:
        """
        Estimate of Lipschitz constant of objective :math:`L`
        """
    @property
    def fpr(self) -> float:
        """
        Fixed-point residual :math:`\\left\\|p\\right\\| / \\gamma`
        """
    @property
    def grad_ψ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Gradient of objective :math:`\\nabla\\psi(x)`
        """
    @property
    def grad_ψ_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Gradient of objective at x̂ :math:`\\nabla\\psi(\\hat x)`
        """
    @property
    def k(self) -> int:
        """
        Iteration
        """
    @property
    def norm_sq_p(self) -> float:
        """
        :math:`\\left\\|p\\right\\|^2`
        """
    @property
    def p(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Projected gradient step :math:`p`
        """
    @property
    def params(self) -> PANOCParams:
        """
        Solver parameters
        """
    @property
    def problem(self) -> Problem:
        """
        Problem being solved
        """
    @property
    def q(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Previous quasi-Newton step :math:`\\nabla\\psi(\\hat x)`
        """
    @property
    def status(self) -> alpaqa._alpaqa_d.SolverStatus:
        """
        Current solver status
        """
    @property
    def x(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Decision variable :math:`x`
        """
    @property
    def x_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Decision variable after projected gradient step :math:`\\hat x`
        """
    @property
    def y(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Lagrange multipliers :math:`y`
        """
    @property
    def y_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Candidate updated multipliers at x̂ :math:`\\hat y(\\hat x)`
        """
    @property
    def Σ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Penalty factor :math:`\\Sigma`
        """
    @property
    def γ(self) -> float:
        """
        Step size :math:`\\gamma`
        """
    @property
    def ε(self) -> float:
        """
        Tolerance reached :math:`\\varepsilon_k`
        """
    @property
    def τ(self) -> float:
        """
        Previous line search parameter :math:`\\tau`
        """
    @property
    def φγ(self) -> float:
        """
        Forward-backward envelope :math:`\\varphi_\\gamma(x)`
        """
    @property
    def ψ(self) -> float:
        """
        Objective value :math:`\\psi(x)`
        """
    @property
    def ψ_hat(self) -> float:
        """
        Objective at x̂ :math:`\\psi(\\hat x)`
        """
class PANOCSolver:
    """
    C++ documentation: :cpp:class:`alpaqa::PANOCSolver`
    """
    Params = PANOCParams
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __call__(self, problem: Problem, opts: InnerSolveOptions = {}, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple:
        """
        Solve the given problem.
        
        :param problem: Problem to solve
        :param opts: Options (such as desired tolerance)
        :param x: Optional initial guess for the decision variables
        :param y: Lagrange multipliers (when used as ALM inner solver)
        :param Σ: Penalty factors (when used as ALM inner solver)
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`x`
                 * Updated Lagrange multipliers (only if parameter ``y`` was not ``None``)
                 * Constraint violation (only if parameter ``y`` was not ``None``)
                 * Statistics
        """
    def __copy__(self) -> PANOCSolver:
        ...
    def __deepcopy__(self, memo: dict) -> PANOCSolver:
        ...
    @typing.overload
    def __init__(self, other: PANOCSolver) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, panoc_params: PANOCParams | dict = {}, lbfgs_params: LBFGS.Params | dict = {}, direction_params: StructuredLBFGSDirection.DirectionParams | dict = {}) -> None:
        """
        Create a PANOC solver using structured L-BFGS directions.
        """
    @typing.overload
    def __init__(self, panoc_params: PANOCParams | dict, direction: PANOCDirection) -> None:
        """
        Create a PANOC solver using a custom direction.
        """
    def __str__(self) -> str:
        ...
    def set_progress_callback(self, callback: typing.Callable[[PANOCProgressInfo], None]) -> PANOCSolver:
        """
        Specify a callable that is invoked with some intermediate results on each iteration of the algorithm.
        """
    def stop(self) -> None:
        ...
    @property
    def direction(self) -> PANOCDirection:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def params(self) -> PANOCParams:
        ...
class PANTRDirection:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, direction: NewtonTRDirection) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, direction: typing.Any) -> None:
        """
        Explicit conversion from a custom Python class.
        """
    def __str__(self) -> str:
        ...
    @property
    def params(self) -> typing.Any:
        ...
class PANTRParams:
    """
    C++ documentation: :cpp:class:`alpaqa::PANTRParams`
    """
    L_max: float
    L_min: float
    Lipschitz: LipschitzEstimateParams
    TR_tolerance_factor: float
    compute_ratio_using_new_stepsize: bool
    disable_acceleration: bool
    initial_radius: float
    max_iter: int
    max_no_progress: int
    max_time: datetime.timedelta
    min_radius: float
    print_interval: int
    print_precision: int
    quadratic_upperbound_tolerance_factor: float
    radius_factor_acceptable: float
    radius_factor_good: float
    radius_factor_rejected: float
    ratio_approx_fbe_quadratic_model: bool
    ratio_threshold_acceptable: float
    ratio_threshold_good: float
    recompute_last_prox_step_after_direction_reset: bool
    stop_crit: alpaqa._alpaqa_d.PANOCStopCrit
    update_direction_on_prox_step: bool
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class PANTRProgressInfo:
    """
    Data passed to the PANTR progress callback.
    
    C++ documentation: :cpp:class:`alpaqa::PANTRProgressInfo`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def L(self) -> float:
        """
        Estimate of Lipschitz constant of objective :math:`L`
        """
    @property
    def fpr(self) -> float:
        """
        Fixed-point residual :math:`\\left\\|p\\right\\| / \\gamma`
        """
    @property
    def grad_ψ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Gradient of objective :math:`\\nabla\\psi(x)`
        """
    @property
    def grad_ψ_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Gradient of objective at x̂ :math:`\\nabla\\psi(\\hat x)`
        """
    @property
    def k(self) -> int:
        """
        Iteration
        """
    @property
    def norm_sq_p(self) -> float:
        """
        :math:`\\left\\|p\\right\\|^2`
        """
    @property
    def p(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Projected gradient step :math:`p`
        """
    @property
    def params(self) -> PANTRParams:
        """
        Solver parameters
        """
    @property
    def problem(self) -> Problem:
        """
        Problem being solved
        """
    @property
    def q(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Previous quasi-Newton step :math:`\\nabla\\psi(\\hat x)`
        """
    @property
    def status(self) -> alpaqa._alpaqa_d.SolverStatus:
        """
        Current solver status
        """
    @property
    def x(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Decision variable :math:`x`
        """
    @property
    def x_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Decision variable after projected gradient step :math:`\\hat x`
        """
    @property
    def y(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Lagrange multipliers :math:`y`
        """
    @property
    def y_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Candidate updated multipliers at x̂ :math:`\\hat y(\\hat x)`
        """
    @property
    def Δ(self) -> float:
        """
        Previous trust radius :math:`\\Delta`
        """
    @property
    def Σ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Penalty factor :math:`\\Sigma`
        """
    @property
    def γ(self) -> float:
        """
        Step size :math:`\\gamma`
        """
    @property
    def ε(self) -> float:
        """
        Tolerance reached :math:`\\varepsilon_k`
        """
    @property
    def ρ(self) -> float:
        """
        Previous decrease ratio :math:`\\rho`
        """
    @property
    def τ(self) -> float:
        """
        Acceptance (1) or rejection (0) of previous accelerated step :math:`\\tau`
        """
    @property
    def φγ(self) -> float:
        """
        Forward-backward envelope :math:`\\varphi_\\gamma(x)`
        """
    @property
    def ψ(self) -> float:
        """
        Objective value :math:`\\psi(x)`
        """
    @property
    def ψ_hat(self) -> float:
        """
        Objective at x̂ :math:`\\psi(\\hat x)`
        """
class PANTRSolver:
    """
    C++ documentation: :cpp:class:`alpaqa::PANTRSolver`
    """
    Params = PANTRParams
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __call__(self, problem: Problem, opts: InnerSolveOptions = {}, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple:
        """
        Solve the given problem.
        
        :param problem: Problem to solve
        :param opts: Options (such as desired tolerance)
        :param x: Optional initial guess for the decision variables
        :param y: Lagrange multipliers (when used as ALM inner solver)
        :param Σ: Penalty factors (when used as ALM inner solver)
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`x`
                 * Updated Lagrange multipliers (only if parameter ``y`` was not ``None``)
                 * Constraint violation (only if parameter ``y`` was not ``None``)
                 * Statistics
        """
    def __copy__(self) -> PANTRSolver:
        ...
    def __deepcopy__(self, memo: dict) -> PANTRSolver:
        ...
    @typing.overload
    def __init__(self, other: PANTRSolver) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, pantr_params: PANTRParams | dict = {}, steihaug_params: SteihaugCGParams | dict = {}, direction_params: NewtonTRDirectionParams | dict = {}) -> None:
        """
        Create a PANTR solver using a structured Newton CG subproblem solver.
        """
    @typing.overload
    def __init__(self, pantr_params: PANTRParams | dict, direction: PANTRDirection) -> None:
        """
        Create a PANTR solver using a custom direction.
        """
    def __str__(self) -> str:
        ...
    def set_progress_callback(self, callback: typing.Callable[[PANTRProgressInfo], None]) -> PANTRSolver:
        """
        Specify a callable that is invoked with some intermediate results on each iteration of the algorithm.
        """
    def stop(self) -> None:
        ...
    @property
    def direction(self) -> PANTRDirection:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def params(self) -> PANTRParams:
        ...
class Problem:
    """
    C++ documentation: :cpp:class:`alpaqa::TypeErasedProblem`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> Problem:
        ...
    def __deepcopy__(self, memo: dict) -> Problem:
        ...
    @typing.overload
    def __init__(self, other: Problem) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, problem: CasADiProblem) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, problem: DLProblem) -> None:
        """
        Explicit conversion.
        """
    @typing.overload
    def __init__(self, problem: typing.Any) -> None:
        """
        Explicit conversion from a custom Python class.
        """
    def __str__(self) -> str:
        ...
    def check(self) -> None:
        ...
    def eval_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    def eval_f_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], g: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_f_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_fx: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_f_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple:
        ...
    @typing.overload
    def eval_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], gx: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_grad_L(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_L: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_n: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_fx: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_f(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_grad_f_grad_g_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_f: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_gxy: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_g_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_gxy: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_g_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_grad_gi(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], i: int, grad_gi: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_n: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_m: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_hess_L(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float = 1.0) -> tuple[typing.Any, alpaqa._alpaqa_d.Symmetry]:
        """
        Returns the Hessian of the Lagrangian and its symmetry.
        """
    def eval_hess_L_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float, v: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Hv: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def eval_hess_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float = 1.0) -> tuple[typing.Any, alpaqa._alpaqa_d.Symmetry]:
        """
        Returns the Hessian of the augmented Lagrangian and its symmetry.
        """
    def eval_hess_ψ_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], scale: float, v: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Hv: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], J: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]) -> int:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]:
        ...
    def eval_jac_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[typing.Any, alpaqa._alpaqa_d.Symmetry]:
        """
        Returns the Jacobian of the constraints and its symmetry.
        """
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], e: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_proj_multipliers(self, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], M: float) -> None:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], x_hat: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], p: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], float]:
        ...
    @typing.overload
    def eval_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], ŷ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[float, numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]]:
        ...
    @typing.overload
    def eval_ψ_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_n: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], work_m: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_ψ_grad_ψ(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[float, numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]]:
        ...
    def get_box_C(self) -> Box:
        ...
    def get_box_D(self) -> Box:
        ...
    def provides_check(self) -> bool:
        ...
    def provides_eval_f_g(self) -> bool:
        ...
    def provides_eval_f_grad_f(self) -> bool:
        ...
    def provides_eval_grad_L(self) -> bool:
        ...
    def provides_eval_grad_f_grad_g_prod(self) -> bool:
        ...
    def provides_eval_grad_gi(self) -> bool:
        ...
    def provides_eval_grad_ψ(self) -> bool:
        ...
    def provides_eval_hess_L(self) -> bool:
        ...
    def provides_eval_hess_L_prod(self) -> bool:
        ...
    def provides_eval_hess_ψ(self) -> bool:
        ...
    def provides_eval_hess_ψ_prod(self) -> bool:
        ...
    def provides_eval_inactive_indices_res_lna(self) -> bool:
        ...
    def provides_eval_jac_g(self) -> bool:
        ...
    def provides_eval_ψ(self) -> bool:
        ...
    def provides_eval_ψ_grad_ψ(self) -> bool:
        ...
    def provides_get_box_C(self) -> bool:
        ...
    def provides_get_box_D(self) -> bool:
        ...
    def provides_get_hess_L_sparsity(self) -> bool:
        ...
    def provides_get_hess_ψ_sparsity(self) -> bool:
        ...
    def provides_get_jac_g_sparsity(self) -> bool:
        ...
    @property
    def m(self) -> int:
        """
        Number of general constraints, dimension of :math:`g(x)`
        """
    @property
    def n(self) -> int:
        """
        Number of decision variables, dimension of :math:`x`
        """
class ProblemWithCounters:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def evaluations(self) -> alpaqa._alpaqa_d.EvalCounter:
        ...
    @property
    def problem(self) -> Problem:
        ...
class SteihaugCGParams:
    """
    C++ documentation: :cpp:class:`alpaqa::SteihaugCGParams`
    """
    max_iter_factor: float
    tol_max: float
    tol_scale: float
    tol_scale_root: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class StructuredLBFGSDirection:
    """
    C++ documentation: :cpp:class:`alpaqa::StructuredLBFGSDirection`
    """
    class DirectionParams:
        """
        C++ documentation: :cpp:class:`alpaqa::StructuredLBFGSDirection::DirectionParams`
        """
        full_augmented_hessian: bool
        hessian_vec_factor: float
        hessian_vec_finite_differences: bool
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        @typing.overload
        def __init__(self, params: dict) -> None:
            ...
        @typing.overload
        def __init__(self, **kwargs) -> None:
            ...
        def to_dict(self) -> dict:
            ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, lbfgs_params: LBFGS.Params | dict = {}, direction_params: StructuredLBFGSDirection.DirectionParams | dict = {}) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def params(self) -> tuple[LBFGS.Params, StructuredLBFGSDirection.DirectionParams]:
        ...
class StructuredNewtonDirection:
    """
    C++ documentation: :cpp:class:`alpaqa::StructuredNewtonDirection`
    """
    class DirectionParams:
        """
        C++ documentation: :cpp:class:`alpaqa::StructuredNewtonDirection::DirectionParams`
        """
        hessian_vec_factor: float
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        @typing.overload
        def __init__(self, params: dict) -> None:
            ...
        @typing.overload
        def __init__(self, **kwargs) -> None:
            ...
        def to_dict(self) -> dict:
            ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, direction_params: StructuredNewtonDirection.DirectionParams | dict = {}) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def params(self) -> StructuredNewtonDirection.DirectionParams:
        ...
class UnconstrProblem:
    """
    C++ documentation: :cpp:class:`alpaqa::UnconstrProblem`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __copy__(self) -> UnconstrProblem:
        ...
    def __deepcopy__(self, memo: dict) -> UnconstrProblem:
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, other: UnconstrProblem) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, n: int) -> None:
        """
        :param n: Number of unknowns
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def eval_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], g: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def eval_grad_g_prod(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_gxy: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def eval_grad_gi(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], i: int, grad_gi: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], J: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]) -> int:
        ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.int32]]:
        ...
    def eval_jac_g(self, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], J_values: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], e: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def eval_proj_multipliers(self, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], M: float) -> None:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], x_hat: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], p: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> float:
        ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], grad_ψ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> tuple[numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], float]:
        ...
    def resize(self, n: int) -> None:
        ...
    @property
    def m(self) -> int:
        """
        Number of general constraints, dimension of :math:`g(x)`
        """
    @property
    def n(self) -> int:
        """
        Number of decision variables, dimension of :math:`x`
        """
class ZeroFPRParams:
    """
    C++ documentation: :cpp:class:`alpaqa::ZeroFPRParams`
    """
    L_max: float
    L_min: float
    Lipschitz: LipschitzEstimateParams
    force_linesearch: bool
    linesearch_strictness_factor: float
    linesearch_tolerance_factor: float
    max_iter: int
    max_no_progress: int
    max_time: datetime.timedelta
    min_linesearch_coefficient: float
    print_interval: int
    print_precision: int
    quadratic_upperbound_tolerance_factor: float
    recompute_last_prox_step_after_stepsize_change: bool
    stop_crit: alpaqa._alpaqa_d.PANOCStopCrit
    update_direction_from_prox_step: bool
    update_direction_in_accel: bool
    update_direction_in_candidate: bool
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, params: dict) -> None:
        ...
    @typing.overload
    def __init__(self, **kwargs) -> None:
        ...
    def to_dict(self) -> dict:
        ...
class ZeroFPRProgressInfo:
    """
    Data passed to the ZeroFPR progress callback.
    
    C++ documentation: :cpp:class:`alpaqa::ZeroFPRProgressInfo`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def L(self) -> float:
        """
        Estimate of Lipschitz constant of objective :math:`L`
        """
    @property
    def fpr(self) -> float:
        """
        Fixed-point residual :math:`\\left\\|p\\right\\| / \\gamma`
        """
    @property
    def grad_ψ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Gradient of objective :math:`\\nabla\\psi(x)`
        """
    @property
    def grad_ψ_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Gradient of objective at x̂ :math:`\\nabla\\psi(\\hat x)`
        """
    @property
    def k(self) -> int:
        """
        Iteration
        """
    @property
    def norm_sq_p(self) -> float:
        """
        :math:`\\left\\|p\\right\\|^2`
        """
    @property
    def p(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Projected gradient step :math:`p`
        """
    @property
    def params(self) -> ZeroFPRParams:
        """
        Solver parameters
        """
    @property
    def problem(self) -> Problem:
        """
        Problem being solved
        """
    @property
    def q(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Previous quasi-Newton step :math:`\\nabla\\psi(\\hat x)`
        """
    @property
    def status(self) -> alpaqa._alpaqa_d.SolverStatus:
        """
        Current solver status
        """
    @property
    def x(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Decision variable :math:`x`
        """
    @property
    def x_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Decision variable after projected gradient step :math:`\\hat x`
        """
    @property
    def y(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Lagrange multipliers :math:`y`
        """
    @property
    def y_hat(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Candidate updated multipliers at x̂ :math:`\\hat y(\\hat x)`
        """
    @property
    def Σ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Penalty factor :math:`\\Sigma`
        """
    @property
    def γ(self) -> float:
        """
        Step size :math:`\\gamma`
        """
    @property
    def ε(self) -> float:
        """
        Tolerance reached :math:`\\varepsilon_k`
        """
    @property
    def τ(self) -> float:
        """
        Previous line search parameter :math:`\\tau`
        """
    @property
    def φγ(self) -> float:
        """
        Forward-backward envelope :math:`\\varphi_\\gamma(x)`
        """
    @property
    def ψ(self) -> float:
        """
        Objective value :math:`\\psi(x)`
        """
    @property
    def ψ_hat(self) -> float:
        """
        Objective at x̂ :math:`\\psi(\\hat x)`
        """
class ZeroFPRSolver:
    """
    C++ documentation: :cpp:class:`alpaqa::ZeroFPRSolver`
    """
    Params = ZeroFPRParams
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __call__(self, problem: Problem, opts: InnerSolveOptions = {}, x: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, y: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, Σ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]] | None = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple:
        """
        Solve the given problem.
        
        :param problem: Problem to solve
        :param opts: Options (such as desired tolerance)
        :param x: Optional initial guess for the decision variables
        :param y: Lagrange multipliers (when used as ALM inner solver)
        :param Σ: Penalty factors (when used as ALM inner solver)
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`x`
                 * Updated Lagrange multipliers (only if parameter ``y`` was not ``None``)
                 * Constraint violation (only if parameter ``y`` was not ``None``)
                 * Statistics
        """
    def __copy__(self) -> ZeroFPRSolver:
        ...
    def __deepcopy__(self, memo: dict) -> ZeroFPRSolver:
        ...
    @typing.overload
    def __init__(self, other: ZeroFPRSolver) -> None:
        """
        Create a copy
        """
    @typing.overload
    def __init__(self, zerofpr_params: ZeroFPRParams | dict = {}, lbfgs_params: LBFGS.Params | dict = {}, direction_params: StructuredLBFGSDirection.DirectionParams | dict = {}) -> None:
        """
        Create a ZeroFPR solver using structured L-BFGS directions.
        """
    @typing.overload
    def __init__(self, zerofpr_params: ZeroFPRParams | dict, direction: PANOCDirection) -> None:
        """
        Create a ZeroFPR solver using a custom direction.
        """
    def __str__(self) -> str:
        ...
    def set_progress_callback(self, callback: typing.Callable[[ZeroFPRProgressInfo], None]) -> ZeroFPRSolver:
        """
        Specify a callable that is invoked with some intermediate results on each iteration of the algorithm.
        """
    def stop(self) -> None:
        ...
    @property
    def direction(self) -> PANOCDirection:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def params(self) -> ZeroFPRParams:
        ...
def control_problem_with_counters(problem: CasADiControlProblem) -> ControlProblemWithCounters:
    """
    Wrap the problem to count all function evaluations.
    
    :param problem: The original problem to wrap. Copied.
    :return: * Wrapped problem.
             * Counters for wrapped problem.
    """
def deserialize_casadi_problem(functions: dict[str, str]) -> CasADiProblem:
    """
    Deserialize a CasADi problem from the given serialized functions.
    """
def kkt_error(arg0: Problem, arg1: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]], arg2: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> KKTError:
    ...
def load_casadi_control_problem(so_name: str, N: int) -> CasADiControlProblem:
    """
    Load a compiled CasADi optimal control problem.
    """
def load_casadi_problem(so_name: str) -> CasADiProblem:
    """
    Load a compiled CasADi problem.
    """
@typing.overload
def problem_with_counters(problem: CasADiProblem) -> ProblemWithCounters:
    """
    Wrap the problem to count all function evaluations.
    
    :param problem: The original problem to wrap. Copied.
    :return: * Wrapped problem.
             * Counters for wrapped problem.
    """
@typing.overload
def problem_with_counters(problem: DLProblem) -> ProblemWithCounters:
    """
    Wrap the problem to count all function evaluations.
    
    :param problem: The original problem to wrap. Copied.
    :return: * Wrapped problem.
             * Counters for wrapped problem.
    """
@typing.overload
def problem_with_counters(problem: typing.Any) -> ProblemWithCounters:
    ...
def provided_functions(problem: Problem) -> str:
    """
    Returns a string representing the functions provided by the problem.
    """
@typing.overload
def prox(self: functions.NuclearNorm, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version overwrites the given output arguments.
    
    .. seealso:: :py:func:`alpaqa.prox_step`
    """
@typing.overload
def prox(self: functions.NuclearNorm, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1) -> tuple[float, numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]]:
    """
    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version returns the outputs as a tuple.
    
    .. seealso:: :py:func:`alpaqa.prox_step`
    """
@typing.overload
def prox(self: functions.L1Norm, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version overwrites the given output arguments.
    
    .. seealso:: :py:func:`alpaqa.prox_step`
    """
@typing.overload
def prox(self: functions.L1Norm, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1) -> tuple[float, numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]]:
    """
    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version returns the outputs as a tuple.
    
    .. seealso:: :py:func:`alpaqa.prox_step`
    """
@typing.overload
def prox(self: functions.L1NormElementwise, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version overwrites the given output arguments.
    
    .. seealso:: :py:func:`alpaqa.prox_step`
    """
@typing.overload
def prox(self: functions.L1NormElementwise, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1) -> tuple[float, numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]]:
    """
    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version returns the outputs as a tuple.
    
    .. seealso:: :py:func:`alpaqa.prox_step`
    """
@typing.overload
def prox(self: Box, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version overwrites the given output arguments.
    
    .. seealso:: :py:func:`alpaqa.prox_step`
    """
@typing.overload
def prox(self: Box, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1) -> tuple[float, numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]]:
    """
    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version returns the outputs as a tuple.
    
    .. seealso:: :py:func:`alpaqa.prox_step`
    """
@typing.overload
def prox_step(self: functions.NuclearNorm, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], input_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1, γ_step: float = -1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version overwrites the given output arguments.
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
@typing.overload
def prox_step(self: functions.NuclearNorm, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], input_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1, γ_step: float = -1) -> tuple[float, numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]]:
    """
    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version returns the outputs as a tuple.
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
@typing.overload
def prox_step(self: functions.L1Norm, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], input_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1, γ_step: float = -1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version overwrites the given output arguments.
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
@typing.overload
def prox_step(self: functions.L1Norm, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], input_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1, γ_step: float = -1) -> tuple[float, numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]]:
    """
    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version returns the outputs as a tuple.
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
@typing.overload
def prox_step(self: functions.L1NormElementwise, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], input_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1, γ_step: float = -1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version overwrites the given output arguments.
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
@typing.overload
def prox_step(self: functions.L1NormElementwise, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], input_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1, γ_step: float = -1) -> tuple[float, numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]]:
    """
    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version returns the outputs as a tuple.
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
@typing.overload
def prox_step(self: Box, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], input_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], output_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1, γ_step: float = -1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version overwrites the given output arguments.
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
@typing.overload
def prox_step(self: Box, input: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], input_step: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], γ: float = 1, γ_step: float = -1) -> tuple[float, numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]]:
    """
    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version returns the outputs as a tuple.
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
