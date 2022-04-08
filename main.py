from automaton import DFA
from solution_maker import Solution

# СОЗДАЁМ ДКА ВРУЧНУЮ (ДЗ задание 2.5)
# вычисляем L5 = L2 \ L3 = L2 ∩ (¬L3) = L2 ∩ (¬(g1 ∩ g2))
# L2 предварительно вычислено, оно тоже является результатом выражения в 2.2
# g1 и g2 - два автомата из условия 2.3

g1 = DFA(["a", "b"],        # алфавит
         ["1", "2"])        # состояния
g1.connect("1", "2", "a")   # создаём переход от "1" к "2" по "a"
g1.connect("1", "1", "b")
g1.connect("2", "1", "a")
g1.connect("2", "2", "b")
g1.set_terminal("1")        # делаем состояние "1" терминалом

g2 = DFA(["a", "b"], ["1", "2", "3"])
g2.connect("1", "2", "b")
g2.connect("1", "1", "a")
g2.connect("2", "3", "b")
g2.connect("2", "2", "a")
g2.connect("3", "1", "b")
g2.connect("3", "3", "a")
g2.set_terminal("1")

l2 = DFA(["a", "b"], ["1", "2", "3", "4"])
l2.connect("1", "2", "a")
l2.connect("1", "2", "b")
l2.connect("2", "3", "a")
l2.connect("2", "3", "b")
l2.connect("3", "4", "a")
l2.connect("3", "4", "b")
l2.connect("4", "3", "a")
l2.connect("4", "3", "b")
l2.set_terminal("4")

l3 = g1.intersection(g2)        # находим пересечение
l3_neg = l3.negation()          # отрицание результата
l3_neg.reset_labels()           # сбрасываем названия узлов, чтобы они стали выглядеть проще
l5 = l2.intersection(l3_neg)    # находим пересечение

g1.save("g1.dot", "g1.png", clear=True)     # сохраняем в png
g2.save("g2.dot", "g2.png", clear=True)     # .dot файл нужен как промежуточный, потом удаляется
l2.save("l2.dot", "l2.png", clear=True)
l3_neg.save("l3_neg.dot", "l3_neg.png", clear=True)
l5.save("l5.dot", "l5.png", clear=True)

Solution(l2, l3, "\\").create("solution.pdf")   # создаём решение выражения L5 = L2 \ L3
