from population import Population
from elite import Elite
from file_manager import FileManager
import numpy as np
from pathlib import Path
import shelve
from random import uniform
from datetime import datetime


class SymbolicRegression:
    def __init__(self, max_arg_count, pm_row_count, x_count, u_count, q_count, q_min, q_max, sv_mat_row_count,
                 func_count, u_min, u_max, pop_size, elite_size, x_data, y_target):
        # parameters for population
        self.max_arg_count = max_arg_count
        self.pm_row_count = pm_row_count  # minimum value: 2*x_count - 1
        self.pm_col_count = 1 + max_arg_count + 1
        self.x_count = x_count
        self.u_count = u_count
        self.q_count = q_count
        self.q_min = q_min
        self.q_max = q_max
        self.sv_mat_row_count = sv_mat_row_count
        self.func_count = func_count
        self.u_min = u_min
        self.u_max = u_max

        self.x_data = x_data
        self.y_target = y_target
        self.samples = x_data.shape[1]

        self.pm_permitted_rows = [k for k in range(2 * self.x_count - 1, self.pm_row_count + 1)]
        self.pm_permitted_cols = [k for k in range(1, self.pm_col_count)]

        self.pop = Population(self.max_arg_count, self.pm_row_count, self.pm_col_count, self.x_count, self.u_count,
                              self.q_count, self.sv_mat_row_count, self.func_count, self.u_min, self.u_max, self.q_min,
                              self.q_max, self.pm_permitted_rows, self.pm_permitted_cols)

        # #######################file manager################################################## #
        self.fm = FileManager()
        self.current_path = Path.cwd()
        self.live_reg_data_folder_path = self.current_path / Path('live_regression_data')
        self.history_data_folder_path = self.current_path / Path('history_regression_data')
        self.resume_data_folder_path = self.current_path / Path('resume')
        self.optimization_data_folder_path = self.current_path / Path('optimization')

        # #######################population################################################## #
        self.pop_size = pop_size
        # parameters for the crossover process
        self.crossover_population = int(pop_size * 0.8)
        self.children_return_count = 2
        self.crossover_count = self.crossover_population // self.children_return_count
        # ensure children return count can fill exactly the crossover population
        assert self.crossover_population % self.children_return_count == 0

        # parameters for the mutation process
        self.mutation_population = int(pop_size * 0.2)
        self.mutation_count = self.mutation_population
        assert self.crossover_population + self.mutation_population == self.pop_size
        # ########################################################################################## #
        self.elite_size = elite_size
        self.elite = Elite()

    def initial_backup(self):
        # check and create folders for the live and history results
        self.fm.check_and_create_folder(self.resume_data_folder_path)
        self.fm.check_and_create_folder(self.optimization_data_folder_path)
        # backup history results
        # self.fm.backup_all_shelve_files_to_zip_files(self.live_reg_data_folder_path, self.history_data_folder_path)
        # delete saved results from the live folder
        # self.fm.delete_shelf_files(self.live_reg_data_folder_path)

    def check_folders(self):
        # check and create folders for the resume and optimization results
        self.fm.check_and_create_folder(self.resume_data_folder_path)
        self.fm.check_and_create_folder(self.optimization_data_folder_path)
        # backup history results
        # self.fm.backup_all_shelve_files_to_zip_files(self.live_reg_data_folder_path, self.history_data_folder_path)
        # delete saved results from the live folder
        # self.fm.delete_shelf_files(self.live_reg_data_folder_path)

    def create_target_shelf_file_and_status_file(self):
        # creating the target shelf file
        target_shelf_file = shelve.open(str(self.live_reg_data_folder_path / Path('target')))
        target_shelf_file['x_data'] = self.x_data
        target_shelf_file['y_target'] = self.y_target
        target_shelf_file['y_target_expression'] = '0.5*cos(x1) + sin(x1)'
        target_shelf_file.close()
        # checking or creating the program status file
        self.fm.set_program_status(self.live_reg_data_folder_path, True)
        # ########################################################################################## #
        
    def initialize_elite_solutions(self):
        # elite solutions
        elite_svs = np.zeros((self.elite_size, self.sv_mat_row_count, 3), dtype=int)
        elite_qs = np.zeros((self.elite_size, self.q_count))
        elite_ys = np.zeros((self.elite_size, self.samples))
        elite_scores = np.full(self.elite_size, np.inf)
        elite_expressions = ["0" for _ in range(self.elite_size)]
        return elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions
    
    def initial_population_generation_and_score_calculation(self):
        # initial population generation
        pop_sv, pop_q = self.pop.encode(self.pop_size)
        # initial population scores calculation
        scores = self.pop.calculate_scores(pop_sv, pop_q, self.x_data, self.y_target, self.samples)
        # initial generation probabilities calculation
        probabilities = self.pop.probability_calculation_method(scores)
        return pop_sv, pop_q, scores, probabilities
    
    def best_solution_calculation(self, pop_sv, pop_q, scores):
        # population scores sorting
        sorted_indexes = np.argsort(scores)
        # best calculation
        best_index = sorted_indexes[0:1]
        best_sv_mat = pop_sv[best_index]
        best_q = pop_q[best_index]
        best_score = scores[best_index]
        best_expression = self.pop.calculate_expressions(best_sv_mat, best_q)
        best_y = self.pop.calculate_y(best_sv_mat, best_q, self.x_data, self.samples)
        return best_sv_mat, best_q, best_score, best_y, best_expression
    
    def save_best_solution(self, best_y, best_expression, best_score, current_generation):
        # save the best solutions of every generation
        reg_shelf_file = shelve.open(str(self.live_reg_data_folder_path / Path('reg_' + str(current_generation))))
        reg_shelf_file['y_regression'] = best_y
        reg_shelf_file['y_regression_expression'] = best_expression
        reg_shelf_file['score'] = best_score
        reg_shelf_file.close()

    def save_last_generation(self, pop_sv, pop_q, scores, probabilities):
        reg_shelf_file = shelve.open(str(self.live_reg_data_folder_path / Path('last_generation')))
        reg_shelf_file['pop_sv'] = pop_sv
        reg_shelf_file['pop_q'] = pop_q
        reg_shelf_file['scores'] = scores
        reg_shelf_file['probabilities'] = probabilities
        reg_shelf_file.close()

    def create_resume_file(self, elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions, pop_sv, pop_q, scores,
                           probabilities):
        reg_shelf_file_path = self.resume_data_folder_path / Path('resume')
        print('Resume File Path: ', reg_shelf_file_path)
        reg_shelf_file = shelve.open(str(reg_shelf_file_path))
        reg_shelf_file['x_count'] = self.x_count
        reg_shelf_file['u_count'] = self.u_count
        reg_shelf_file['u_min'] = self.u_min
        reg_shelf_file['u_max'] = self.u_max
        reg_shelf_file['x_data'] = self.x_data
        reg_shelf_file['y_target'] = self.y_target

        reg_shelf_file['q_count'] = self.q_count
        reg_shelf_file['q_min'] = self.q_min
        reg_shelf_file['q_max'] = self.q_max

        reg_shelf_file['pm_row_count'] = self.pm_row_count
        reg_shelf_file['sv_mat_row_count'] = self.sv_mat_row_count

        reg_shelf_file['pop_size'] = self.pop_size
        reg_shelf_file['elite_size'] = self.elite_size

        reg_shelf_file['elite_svs'] = elite_svs
        reg_shelf_file['elite_qs'] = elite_qs
        reg_shelf_file['elite_scores'] = elite_scores
        reg_shelf_file['elite_ys'] = elite_ys
        reg_shelf_file['elite_expressions'] = elite_expressions

        reg_shelf_file['pop_sv'] = pop_sv
        reg_shelf_file['pop_q'] = pop_q
        reg_shelf_file['scores'] = scores
        reg_shelf_file['probabilities'] = probabilities
        reg_shelf_file.close()

    def save_resume_file(self, elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions, pop_sv, pop_q, scores,
                         probabilities):
        reg_shelf_file_path = self.resume_data_folder_path / Path('resume')
        reg_shelf_file = shelve.open(str(reg_shelf_file_path))
        reg_shelf_file['elite_svs'] = elite_svs
        reg_shelf_file['elite_qs'] = elite_qs
        reg_shelf_file['elite_scores'] = elite_scores
        reg_shelf_file['elite_ys'] = elite_ys
        reg_shelf_file['elite_expressions'] = elite_expressions

        reg_shelf_file['pop_sv'] = pop_sv
        reg_shelf_file['pop_q'] = pop_q
        reg_shelf_file['scores'] = scores
        reg_shelf_file['probabilities'] = probabilities
        reg_shelf_file.close()
    
    def main_loop(self, pop_sv, pop_q, scores, probabilities, elite_svs, elite_qs, elite_scores, elite_ys,
                  elite_expressions, current_generation, reset_max_attempts, current_attempt, simulation_best_score):
        if current_attempt < reset_max_attempts:
            # crossover process
            pop_sv_new_crossed, pop_q_new_crossed, scores_new_crossed = \
                self.pop.crossover_cycle(pop_sv, pop_q, self.x_data, self.y_target, self.samples, probabilities,
                                         self.children_return_count, self.crossover_count)
            # mutation process
            pop_sv_new_mutated, pop_q_new_mutated, scores_new_mutated = \
                self.pop.mutation_cycle(pop_sv, pop_q, self.x_data, self.y_target, self.samples, probabilities,
                                        self.mutation_count)
            # new population assembly
            pop_sv_new = np.concatenate((pop_sv_new_crossed, pop_sv_new_mutated), axis=0)
            pop_q_new = np.concatenate((pop_q_new_crossed, pop_q_new_mutated), axis=0)
            scores_new = np.concatenate((scores_new_crossed, scores_new_mutated), axis=0)
            # new population probabilities calculation
            probabilities_new = self.pop.probability_calculation_method(scores_new)
            # best calculation
            best_sv_mat, best_q, best_score, best_y, best_expression = \
                self.best_solution_calculation(pop_sv_new, pop_q_new, scores_new)
            # stack in the elite population and save the elite information in disk
            elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions = \
                self.elite.stack(best_sv_mat, best_q, best_score, best_y, best_expression, elite_svs, elite_qs,
                                 elite_scores, elite_ys, elite_expressions)
            if best_score < simulation_best_score:
                simulation_best_score = best_score
                current_attempt = 0
            else:
                current_attempt += 1
            print('current generation = ', current_generation,
                  'best score = ', best_score, 'expression = ', best_expression, 'best historic score = ',
                  elite_scores[0],
                  'times stuck=', current_attempt)
            # passing to the new generation
            pop_sv = pop_sv_new.copy()
            pop_q = pop_q_new.copy()
            probabilities = probabilities_new.copy()
            current_generation += 1
        else:
            print('reached maximum attempts to reduce the score, restarting the genetic algorithm')
            # initial population generation and score and probabilities calculation
            pop_sv, pop_q, scores, probabilities = self.initial_population_generation_and_score_calculation()
            # best calculation
            best_sv_mat, best_q, best_score, best_y, best_expression = self.best_solution_calculation(pop_sv, pop_q,
                                                                                                      scores)
            # stack in the elite population and save the elite information in disk
            elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions = \
                self.elite.stack(best_sv_mat, best_q, best_score, best_y, best_expression, elite_svs, elite_qs,
                                 elite_scores, elite_ys, elite_expressions)
            current_attempt = 0
            simulation_best_score = best_score
            print('current generation = ', current_generation,
                  'best score = ', best_score, 'expression = ', best_expression, 'best historic score = ',
                  elite_scores[0],
                  'times stuck=', current_attempt)
        return pop_sv, pop_q, scores, probabilities, elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions, \
               current_generation, current_attempt, simulation_best_score, best_score[0], best_expression[0]

    def backup_resume_data_to_zip(self):
        # backup resume results
        today_date = datetime.today().strftime('%Y-%m-%d')  # get the today's date
        basename = 'resume_' + today_date + '_'
        self.fm.backup_all_shelve_files_to_zip_files(self.resume_data_folder_path, self.resume_data_folder_path,
                                                     basename)
        # delete current resume results after backup
        self.fm.delete_shelf_files(self.resume_data_folder_path)
        print('\n Main Loop Done.')

    def resume_simulation(self, max_generations, reset_max_attempts):
        # elite population initialization
        elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions = self.initialize_elite_solutions()
        # initial population generation and score and probabilities calculation
        pop_sv, pop_q, scores, probabilities = self.initial_population_generation_and_score_calculation()
        current_generation = 0
        self.main_loop(pop_sv, pop_q, scores, probabilities, elite_svs, elite_qs, elite_scores, elite_ys,
                       elite_expressions, current_generation, max_generations, reset_max_attempts)
        print('\n Program Done.')


