from automaton import DFA
from solution_maker import Solution
import os


g1 = DFA(["a", "b"], ["1", "2"])
g1.connect("1", "2", "a")
g1.connect("1", "1", "b")
g1.connect("2", "1", "a")
g1.connect("2", "2", "b")
g1.set_terminal("1")

g2 = DFA(["a", "b"], ["1", "2", "3"])
g2.connect("1", "2", "b")
g2.connect("1", "1", "a")
g2.connect("2", "3", "b")
g2.connect("2", "2", "a")
g2.connect("3", "1", "b")
g2.connect("3", "3", "a")
g2.set_terminal("1")


solution = Solution(g1, g2, "^")
g3 = solution.create("intersection.pdf")




