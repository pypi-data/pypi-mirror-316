"""
Decorators for functions that
1. take ``model: Model`` and ``layout: Layout`` as inputs (nothing else)
2. return a generator the iterates over stim.Circuit(s)
"""


def qec_circuit(func):
    """
    Decorator for adding the attribute ``"log_op_type"`` and setting it to
    ``"qec_cycle"`` to a function.
    """
    func.log_op_type = "qec_cycle"
    return func


def sq_gate(func):
    """
    Decorator for adding the attribute ``"log_op_type"`` and setting it to
    ``"sq_unitary_gate"`` to a function.
    """
    func.log_op_type = "sq_unitary_gate"
    return func


def tq_gate(func):
    """
    Decorator for adding the attribute ``"log_op_type"`` and setting it to
    ``"tq_unitary_gate"`` to a function.
    """
    func.log_op_type = "tq_unitary_gate"
    func.num_qubits = 1
    return func


def qubit_init_z(func):
    """
    Decorator for adding the attribute ``"log_op_type", "rot_basis"`` and setting
    them to ``"qubit_init", False`` (respectively) to a function.
    """
    func.log_op_type = "qubit_init"
    func.rot_basis = False
    return func


def qubit_init_x(func):
    """
    Decorator for adding the attribute ``"log_op_type", "rot_basis"`` and setting
    them to ``"qubit_init", False`` (respectively) to a function.
    """
    func.log_op_type = "qubit_init"
    func.rot_basis = True
    return func


def logical_measurement_z(func):
    """
    Decorator for adding the attributes ``"log_op_type", "rot_basis"`` and setting
    them to ``"measurement", False`` (respectively) to a function.
    """
    func.log_op_type = "measurement"
    func.rot_basis = False
    return func


def logical_measurement_x(func):
    """
    Decorator for adding the attributes ``"log_op_type", "rot_basis"`` and setting
    them to ``"measurement", True`` (respectively) to a function.
    """
    func.log_op_type = "measurement"
    func.rot_basis = True
    return func
