import numpy as np
from individual import Individual
from genetic_algorithm import parents_index_selection, crossover
from genetic_algorithm import sum_based_prob, roulette
from random import randrange


class Population:
    def __init__(self, max_arg_count, pm_row_count, pm_col_count, x_count,
                 u_count, q_count, sv_mat_row_count, func_count,
                 u_min, u_max, q_min, q_max, pm_permitted_rows, pm_permitted_cols):
        self.sv_mat_row_count = sv_mat_row_count
        self.pm_col_count = pm_col_count
        self.pm_row_count = pm_row_count

        self.u_count = u_count
        self.x_count = x_count

        self.q_count = q_count
        self.q_min = q_min
        self.q_max = q_max

        self.pm_permitted_rows = pm_permitted_rows
        self.pm_permitted_cols = pm_permitted_cols

        self.individual_object = Individual(max_arg_count, pm_row_count, pm_col_count, x_count, u_count, q_count,
                                            sv_mat_row_count, func_count, u_min, u_max, q_min, q_max, pm_permitted_rows,
                                            pm_permitted_cols)

    def encode(self, pop_size):
        pop = np.zeros((pop_size, self.sv_mat_row_count, 4), dtype=int)
        pop_q = np.zeros((pop_size, self.q_count))

        for k in range(pop_size):
            pop[k], pop_q[k] = self.individual_object.encode()
        return pop, pop_q

    def calculate_scores(self, pop_sv, pop_q, x, y_target, samples):
        pop_size, sv_mat_row_count, sv_mat_col_count = pop_sv.shape
        scores = np.full(pop_size, np.inf)
        for k in range(pop_size):
            scores[k] = self.individual_object.calc_score(pop_sv[k], pop_q[k], x, y_target, samples)
        return scores

    def calculate_y(self, pop_sv, pop_q, x, samples):
        pop_size, sv_mat_row_count, sv_mat_col_count = pop_sv.shape
        y = np.zeros((pop_size, self.u_count, samples))
        for k in range(pop_size):
            y[k] = self.individual_object.calculate_y(pop_sv[k], pop_q[k], x, samples)
        return y

    def calculate_expressions(self, pop_sv, pop_q):
        pop_size, sv_mat_row_count, sv_mat_col_count = pop_sv.shape
        expressions = []
        for k in range(pop_size):
            expressions.append(self.individual_object.calculate_y_symbol(pop_sv[k], pop_q[k]))
        return expressions

    def apply_to_basic_solution(self, pop):
        pop_size, sv_mat_row_count, sv_mat_col_count = pop.shape
        pm_pop = np.zeros((pop_size, self.pm_row_count, self.pm_col_count), dtype=int)
        for k in range(pop_size):
            pm_pop[k] = self.individual_object.apply_to_basic_solution(pop[k])
        return pm_pop

    @staticmethod
    def parents_index_selection(probabilities):
        parent_index_1, parent_index_2 = parents_index_selection(probabilities)
        return parent_index_1, parent_index_2

    @staticmethod
    def probability_calculation_method(scores):
        return sum_based_prob(scores)

    def crossover(self, x, y_target, samples, parent_1, parent_2, parent_q_1, parent_q_2, children_return_count):
        offsprings_sv, offsprings_q = crossover(parent_1, parent_2, parent_q_1, parent_q_2)
        offsprings_scores = self.calculate_scores(offsprings_sv, offsprings_q, x, y_target, samples)
        offsprings_sorted_indexes = np.argsort(offsprings_scores)
        return (offsprings_sv[offsprings_sorted_indexes[0:children_return_count]],
                offsprings_q[offsprings_sorted_indexes[0:children_return_count]],
                offsprings_scores[offsprings_sorted_indexes[0:children_return_count]])

    def crossover_cycle(self, pop_sv, pop_q, x, y_target, samples, probabilities, children_return_count,
                        crossover_count):
        pop_new_size = crossover_count*children_return_count
        pop_sv_new = np.zeros((pop_new_size, self.sv_mat_row_count, 4), dtype=int)
        pop_q_new = np.zeros((pop_new_size, self.q_count))
        pop_scores_new = np.full(pop_new_size, np.inf)
        k = 0
        while k < pop_new_size:
            parent_index_1, parent_index_2 = self.parents_index_selection(probabilities)
            parent_1 = pop_sv[parent_index_1]
            parent_2 = pop_sv[parent_index_2]
            parent_q_1 = pop_q[parent_index_1]
            parent_q_2 = pop_q[parent_index_2]
            offsprings_sv, offsprings_q, offsprings_scores = self.crossover(x, y_target, samples, parent_1, parent_2,
                                                                            parent_q_1, parent_q_2,
                                                                            children_return_count)
            pop_sv_new[k:k + children_return_count] = offsprings_sv
            pop_q_new[k:k + children_return_count] = offsprings_q
            pop_scores_new[k:k + children_return_count] = offsprings_scores
            k += children_return_count
        return pop_sv_new, pop_q_new, pop_scores_new

    @staticmethod
    def individual_selection(pop_sv, pop_q, probabilities):
        individual_index = roulette(probabilities)
        sv_mat = pop_sv[individual_index]
        q = pop_q[individual_index]
        return sv_mat,  q, individual_index

    @staticmethod
    def mutation_indexes_selection(sv_mat, q):
        sv_mat_row_count, sv_mat_col_count = sv_mat.shape
        q_count = q.shape[0]
        sv_row_index = randrange(0, sv_mat_row_count)
        q_index = randrange(0, q_count)
        return sv_row_index, q_index

    def selection_and_mutation(self, pop_sv, pop_q, x, y_target, samples, probabilities):
        sv_mat, q, individual_index = self. individual_selection(pop_sv, pop_q, probabilities)
        sv_row_index, q_index = self.mutation_indexes_selection(sv_mat, q)

        offsprings_sv, offsprings_q = self.individual_object.mutation(sv_mat, q, sv_row_index, q_index)
        offsprings_scores = self.calculate_scores(offsprings_sv, offsprings_q, x, y_target, samples)
        offsprings_sorted_indexes = np.argsort(offsprings_scores)
        best_indexes = offsprings_sorted_indexes[0]
        return offsprings_sv[best_indexes], offsprings_q[best_indexes], offsprings_scores[best_indexes]

    def mutation_cycle(self, pop_sv, pop_q, x, y_target, samples, probabilities, mutation_count):
        pop_new_size = mutation_count
        pop_sv_new = np.zeros((pop_new_size, self.sv_mat_row_count, 4), dtype=int)
        pop_q_new = np.zeros((pop_new_size, self.q_count))
        scores_new = np.full(pop_new_size, np.inf)
        k = 0
        while k < pop_new_size:
            pop_sv_new[k], pop_q_new[k], scores_new[k] = \
                self.selection_and_mutation(pop_sv, pop_q, x, y_target, samples, probabilities)
            k += 1
        return pop_sv_new, pop_q_new, scores_new
