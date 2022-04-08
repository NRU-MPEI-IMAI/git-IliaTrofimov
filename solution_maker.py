import random
import numpy as np
from fpdf import FPDF
from automaton import DFA
import os



ACTIONS = {
    "^": "Intersection",
    "v": "Union",
    "\\": "Compliment",
    "-": "Negation"
}

class Solution:
    def __init__(self, g1: DFA, g2: DFA, action: str):
        if action not in ACTIONS: raise AttributeError(f"Unknown action '{action}'")
        self.g1 = g1
        self.g2 = g2
        self.g3 = None
        self.action = action
        self.__pdf = FPDF()
        self.__temp_files = []

    def create(self, filename):
        self.__pdf.add_page()
        self.__header()
        self.__input_data()
        self.__get__solution()
        self.__pdf.output(filename)
        self.__clear()
        print(f"Solution is saved to file {filename}")
        print("All temporary files are cleared")
        return self.g3

    def __clear(self):
        for f in self.__temp_files:
            os.system(f"del {f}")

    def __header(self):
        self.__pdf.set_font('Courier', 'B', 15)
        self.__pdf.cell(0, 5, f"{ACTIONS[self.action].upper()} OF TWO AUTOMATONS", ln=1)
        self.__pdf.set_font('Courier', 'I', 10)
        self.__pdf.cell(0, 5, 'Auto-generated in Python with FPDF and Graphviz', "B", ln=1)
        self.__pdf.ln(10)

    def __input_data(self):
        self.__pdf.set_font('Courier', "B", size=13)
        self.__pdf.cell(0, 5, "Given automatons:", ln=1)
        self.__pdf.set_font('Courier', size=12)
        rand = random.randint(1000, 20000)

        self.g1.save(f"g1-{rand}.dot", f"g1-{rand}.png", clear=True)
        self.__pdf.cell(0, 5, "Automaton L1:", ln=1)
        self.__pdf.image(f"g1-{rand}.png", w=100)
        self.__temp_files.append(f"g1-{rand}.png")

        if self.g2:
            self.g2.save(f"g2-{rand}.dot", f"g2-{rand}.png", clear=True)
            self.__pdf.cell(0, 5, "Automaton L2:", ln=1)
            self.__pdf.image(f"g2-{rand}.png", w=100)
            self.__temp_files.append(f"g2-{rand}.png")

        self.__pdf.ln(10)

    def __print_states(self, g: DFA, title_states: str, title_terminals: str,):
        self.__pdf.cell(0, 5, title_states, ln=1)
        self.__pdf.cell(0, 5, ', '.join(f"<{l}>" for l in g.labels), ln=1)

        self.__pdf.cell(0, 5, title_terminals, ln=1)
        self.__pdf.cell(0, 5, ', '.join(f"<{l}>" for l in g.labels[np.where(g.terminals)[0]]), ln=1)

    def __print_transitions(self, g: DFA, title: str = "Transitions are:"):
        self.__pdf.cell(0, 5, title, ln=1)
        for i in range(g.states_count()):
            lbl = g.labels[i]
            self.__pdf.cell(0, 5, f"({lbl}):", ln=1)
            for j in range(g.alphabet_len()):
                self.__pdf.cell(0, 5, f"\t-({g.alphabet[j]})-> ({g.labels[g.edges[i, j]]})", ln=1)
            self.__pdf.ln(1)


    def __get__solution(self):
        if not self.g2  and self.action != "-":
            raise AttributeError(f"Cannot apply binary operation '{self.action}' to one automaton")

        self.__pdf.set_font('Courier', "B", size=13)
        self.__pdf.cell(0, 5, "Solution steps:", ln=1)
        self.__pdf.set_font('Courier', size=12)

        if self.action == "^":
            self.__get_intersection()
        elif self.action == "v":
            self.__get_union()
        elif self.action == "\\":
            self.__get_complement()
        elif self.action == "-":
            self.__get_negation()

        self.__print_result()

    def __print_result(self, title=None):
        rand = random.randint(1000, 20000)
        self.g3.save(f"g3-{rand}.dot", f"g3-{rand}.png", clear=True)
        self.__pdf.ln(10)
        self.__pdf.set_font('Courier', "B", size=13)
        self.__pdf.cell(0, 5, f"Result L1 {self.action} L2 = L3:" if not title else title, ln=1)
        self.__pdf.image(f"g3-{rand}.png", w=100)

        self.__temp_files.append(f"g3-{rand}.png")
        self.__pdf.set_font('Courier', size=12)

    def __get_intersection(self):
        self.g3 = self.g1.intersection(self.g2)
        self.__print_states(self.g3,
                            "Resulting automaton's states are:",
                            "Terminal states are:")
        self.__print_transitions(self.g3)


    def __get_negation(self):
        self.g3 = self.g1.negation()
        self.__print_states(self.g3,
                            "Resulting automaton's states are the same:",
                            "Terminal states are:")

    def __get_union(self):
        self.g3 = self.g1.union(self.g2)
        self.__print_states(self.g3,
                            "Resulting automaton's states are:",
                            "Terminal states are:")
        self.__print_transitions(self.g3)


    def __get_complement(self):
        self.g3 = self.g2.negation()
        self.__pdf.cell(0, 5, "First, we will calculate -L2, beacause L3 = L1 \ L2 = L1 ^ -L2", ln=1)
        self.__print_states(self.g3,
                            "-L2 states are the same:",
                            "-L2 terminal states are:")
        self.__print_result("-L2 automaton:")

        self.g3 = self.g1.intersection(self.g3)
        self.__print_states(self.g3,
                            "Resulting automaton's states are:",
                            "Terminal states are:")
        self.__print_transitions(self.g3)


