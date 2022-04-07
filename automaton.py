from __future__ import annotations
from itertools import product
import numpy as np
import os


class DFA:
    """ Class represents deterministic finite automaton. """

    def __init__(self, alphabet: set[str]|list[str], labels: list[str]|set[str]):
        """
        Creates empty automata for given alphabet and states\n
        :param alphabet: all symbols that automaton will recognize. Will remove duplicates
        :param labels: labels for automata's states. Will remove duplicates
        """
        if len(labels) == 0:
            raise AttributeError(f"Cannot create graph with 0 vertices")

        self.alphabet = np.array(list(set(alphabet)), dtype=np.str)
        self.edges = np.array([[-1 for _ in self.alphabet] for _ in labels])
        self.terminals = np.full((len(labels)), False, dtype=bool)
        self.labels = np.array(labels, dtype=np.str)

    def alphabet_len(self):
        """ Alphabet's length """
        return self.alphabet.shape[0]

    def states_count(self):
        """ All states count """
        return self.labels.shape[0]

    def get_index(self, item: str):
        """
        Returns index of given node\n
        :param item: node label
        """
        idx = np.where(self.labels == item)[0]
        if len(idx) == 0:
            raise AttributeError(f"Node with label '{item}' does not exist")
        elif len(idx) > 1:
            raise AttributeError(f"{len(idx)} nodes with label '{item}' exist, cannot determine exact one")
        return idx[0]

    def set_terminal(self, item: str):
        """
        Makes given node terminal or non-terminal (if that node was already terminal)\n
        :param item: node label
        """
        idx = self.get_index(item)
        self.terminals[idx] = not self.terminals[idx]

    def connect(self, first: str, second: str, key: str):
        """
        Creates a transition between two nodes\n
        :param first: initial node's label
        :param second: final node's label
        :param key: symbol to jump to
        """
        idx_key = np.where(self.alphabet == key)
        if len(idx_key) == 0:
            raise Exception(f"Symbol '{key}' is not present in alphabet")

        idx_a = self.get_index(first)
        idx_b = self.get_index(second)
        self.edges[idx_a][idx_key] = idx_b

    def negation(self):
        """ Creates automata which negates current one. """
        res = DFA(self.alphabet, self.labels)
        res.terminals = ~self.terminals
        res.edges = np.copy(self.edges)
        return res

    def _cross_product(self, graph: DFA, strict_terminals: bool = True):
        """
        Cross product of two automatons\n
        :param strict_terminals: True if terminals in the new graph must be made from two terminals from old ones,
        Fasle if only one terminal from any graph is enough for new node to be terminal
        :return:
        """
        new_idx = list(product(range(len(self.labels)), range(len(graph.labels))))
        new_len = len(self.labels) * len(graph.labels)
        new_lbs = list([f"{self.labels[p[0]]},{graph.labels[p[1]]}" for p in new_idx])

        res = DFA(list(set(self.alphabet).union(graph.alphabet)), new_lbs)
        alpha_set = set(self.alphabet).intersection(graph.alphabet)

        for lbl, p in zip(new_lbs, new_idx):
            if (strict_terminals and self.terminals[p[0]] and graph.terminals[p[1]] or
                not strict_terminals and (self.terminals[p[0]] or graph.terminals[p[1]])):
                res.set_terminal(lbl)

            for a in alpha_set:
                edge_a = self.edges[p[0], np.where(self.alphabet == a)[0]]
                edge_b = graph.edges[p[1], np.where(graph.alphabet == a)[0]]
                if edge_a != -1 and edge_b != -1:
                    res.connect(lbl, f"{self.labels[edge_a][0]},{graph.labels[edge_b][0]}", a)
        return res

    def intersection(self, graph: DFA):
        """
        Creates intersection of two automatons\n
        :param graph: graph to intersect with
        """
        return self._cross_product(graph, True)

    def union(self, graph: DFA):
        """
        Creates union of two automatons\n
        :param graph: graph to unite with
        """
        return self._cross_product(graph, False)

    def complement(self, graph: DFA):
        """
        Creates complement of two automatons\n
        :param graph: graph to complement with
        """
        return self._cross_product(graph.negation(), True)

    def save(self, dot_name: str, image_name: str = None, img_fmt: str = "png", clear: bool = True):
        """
        Writes graph to .dot file or create. Requires graphiz to be installed on your machine and dot.exe added to PATH\n
        :param dot_name: name of the .dot file to write graph to
        :param image_name: name of the image in which created .dot file will be compiled. Set None to not compile.
        :param img_fmt: format of the image, can use all formats that graphiz uses
        :param clear: if True, deletes .dot file after creating image, if image_name is None does nothing
        """
        with open(dot_name, "w") as file:
            file.writelines(["digraph G{\n", "rankdir=LR;\n"])
            file.write("node [shape = none]; \"\";\n")
            file.write("node [shape = doublecircle];")

            for label in self.labels[np.where(self.terminals)]:
                file.write(f" \"{label}\";")
            file.write("\nnode [shape = circle];\n")
            for label in self.labels[np.where(~self.terminals)]:
                file.write(f" \"{label}\";")

            file.write(f"\"\" -> \"{self.labels[0]}\";\n")
            for i in range(self.states_count()):
                temp = dict()
                for j in range(self.alphabet_len()):
                    if self.edges[i, j] == -1: continue

                    elif self.edges[i, j] in temp.keys(): temp[self.edges[i, j]].append(self.alphabet[j])
                    else: temp[self.edges[i, j]] = [self.alphabet[j]]
                for k, v in temp.items():
                    file.write(f"\"{self.labels[i]}\" -> \"{self.labels[k]}\" [label = \"{', '.join(v)}\"];\n")
            file.write("}")

        if image_name:
            os.system(f"dot -T{img_fmt.lower()} {dot_name} -o {image_name}")
            print(f"Your graph image saved to {image_name}")
            if clear: os.system(f"del {dot_name}")
            else: print(f"Your graph saved to {dot_name}")
        else:
            print(f"Your graph saved to {dot_name}")
