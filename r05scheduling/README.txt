Programming exercise: DPLL and Scheduling
--------------------------------------------------------------------------------

In this exercise, we will encode the constraints of scheduling problems
as propositional formulas and solve them as a SAT problem.


Instructions
============
1. In this exercise, you need the Z3 SMT solver; to install it, you can use the
   following command:

   `pip install z3-solver`

   See https://github.com/Z3Prover/z3 for more information.
2. Copy the file `template-scheduling.py` to `scheduling.py`.
3. Read and understand the `logic.py` and the `scheduling.py` files.
4. Complete the required sections in `scheduling.py`.
5. Test your implementation and verify its correctness. Again, you can find
   some unit tests in `test_scheduling.py`.
6. Well done! Submit your code.


Structure
=========
./
├── README.txt
├── logic.py
├── template-scheduling.py
├── test_scheduling.py
└── z3_wrapper.py

What are Scheduling problems?
=============================

This exercise formalize a general framework for scheduling based on tasks,
ordering constraints on tasks (a task must precede another), and on
resource needs of the tasks with the constraint that at most one task can
use a given resource at a time (so that if two tasks need the same resource,
they must be performed at different times.)

Formally, a scheduling problem in this exercise consists of:
- A collection of tasks, expressed by a set T
- Ordering constraints, which is a set of pairs of tasks (a subset of T X T)
- Resource needs, which is a mapping from tasks to resources T -> R, where
  R is the set of all resources (machines).
- A natural number N indicating the maximum duration of the schedule

An assumption here is that all tasks have the same (unit) duration.
Hence a solution to the scheduling problem is an assignment of a number 0..N-1
(the time when the task is performed) to every task so that the ordering
constraints are satisfied and no two tasks that need the same resource are
assigned the same time point.

This formalization of scheduling is sufficiently general to represent many
of the most general types of scheduling problems, including the well-known
job shop scheduling problem.

To solve this problem by using a SAT solver, we need to translate the scheduling
problem to the propositional logic.

What needs to be encoded in the propositional logic is the following.
1. Each task is performed at exactly one time point 0..N-1.
2. Two tasks that use the same resource cannot be at the same time point.
3. With ordering constraint t1 < t2 and t1 at time i, then t2 cannot be at 0..i.

All of these constraints are necessary: if any constraint is missing,
incorrect solutions are likely to be obtained.

Testing
=======
1. `python test_scheduling.py`: Using your encoding, it tries to define some
   basic scheduling problems for SAT solvers. Then, it feeds the encoded problem
   to the SAT solver and shows its result.

GL HF :)
