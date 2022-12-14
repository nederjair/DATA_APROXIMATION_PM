from file_manager import FileManager
from my_functions import synthesis_function_list as function_list
import shelve
from random import uniform
import threading
import numpy as np
from pathlib import Path
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import CENTER
from tkinter import DISABLED
from tkinter import NORMAL
from symbolic_regression import SymbolicRegression
import customtkinter
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


class Gui:
    def __init__(self):
        # self.sr_object =
        self.continue_flag = True
        self.fm = FileManager()
        self.current_path = Path.cwd()
        self.live_reg_data_folder_path = self.current_path / Path('history_regression_data')
        self.history_data_folder_path = self.current_path / Path('live_regression_data')
        self.optimization_data_folder_path = self.current_path / Path('optimization')
        self.resume_data_folder_path = self.current_path / Path('resume')
        self.unzipped_optimization_data_folder_path = None
        self.unzipped_resume_data_folder_path = None
        self.stop_flag = False
        # ######################################MAIN WINDOW##################################
        # create the main window
        self.root = self.create_main_window()
        # create the main frame
        self.main_frame = self.create_main_frame(self.root)
        # create the output frame
        self.output_frame = self.create_output_frame(self.main_frame)
        # create output label frames
        self.generation_label, self.score_label, self.historic_score_label, self.expression_label = \
            self.create_output_label_frames(self.output_frame)

        # create button frame
        self.button_frame = self.create_button_frame(self.main_frame)
        # create buttons
        self.start_from_scratch_button, self.resume_button, self.stop_button = self.create_buttons(self.button_frame)
        # #####################################SECONDARY WINDOW#############################

    def stop_simulation(self):
        self.continue_flag = False

    @staticmethod
    def configure_widget(widget, row_list, col_list, row_weight_list, col_weight_list):
        for k in range(len(row_list)):
            widget.rowconfigure(row_list[k], weight=row_weight_list[k])
        for k in range(len(col_list)):
            widget.columnconfigure(col_list[k], weight=col_weight_list[k])

    @staticmethod
    def create_main_window():
        # root
        root = customtkinter.CTk()  # create CTk window like you do with the Tk window
        root.title('Symbolic Regression')
        # root.state('zoomed')
        root.geometry("800x800")
        return root
        
    def create_main_frame(self, parent_frame):
        main_frame = customtkinter.CTkFrame(parent_frame)
        main_frame.grid(row=0, column=0, sticky='nsew')
        self.configure_widget(parent_frame, row_list=[0], col_list=[0], row_weight_list=[1], col_weight_list=[1])
        return main_frame
        
    def create_output_frame(self, parent_frame):
        self.configure_widget(parent_frame, row_list=[0, 1], col_list=[0], row_weight_list=[500, 1],
                              col_weight_list=[1])
        output_frame = customtkinter.CTkFrame(parent_frame, bg='#5F5F9E')
        output_frame.grid(row=0, column=0, sticky='nsew')
        return output_frame

    def create_output_label_frames(self, parent_frame):
        # label frame for generation
        generation_frame = customtkinter.CTkFrame(parent_frame)
        generation_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        # label frame for score
        score_frame = customtkinter.CTkFrame(parent_frame)
        score_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        # label frame for historic score
        historic_score_frame = customtkinter.CTkFrame(parent_frame)
        historic_score_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        # label frame for expression
        expression_frame = customtkinter.CTkFrame(parent_frame)
        expression_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # ###################################labels#####################################################
        # label for generation
        generation_label = customtkinter.CTkLabel(generation_frame, text='Generation\n ---')
        generation_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        # label for score
        score_label = customtkinter.CTkLabel(score_frame, text='Best Score\n ---')
        score_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        # label for score
        historic_score_label = customtkinter.CTkLabel(historic_score_frame, text='Best Historic Score\n ---')
        historic_score_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        # label for expression
        expression_label = customtkinter.CTkLabel(expression_frame, text='Best Expression\n ---')
        expression_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.configure_widget(parent_frame, row_list=[0, 1, 2], col_list=[0, 1], row_weight_list=[1, 1, 1],
                              col_weight_list=[1, 1])

        return generation_label, score_label, historic_score_label, expression_label

    @staticmethod
    def create_button_frame(parent_frame):
        button_frame = customtkinter.CTkFrame(parent_frame)
        button_frame.grid(row=1, column=0, sticky='nsew')
        return button_frame

    @staticmethod
    def set_stop_flag_to_true(sr):
        sr.stop_flag = True
        print('the stop flag has been settled to true')

    def create_buttons(self, parent_frame):
        # button for start from scratch
        start_from_scratch_button = customtkinter.CTkButton(master=parent_frame, text="start simulation from scratch",
                                                            command=self.ask_user_for_optimization_file)
        start_from_scratch_button.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # resume button
        resume_button = customtkinter.CTkButton(parent_frame, text='resume simulation',
                                                command=self.ask_user_for_resume_file)
        resume_button.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # stop button
        stop_button = customtkinter.CTkButton(parent_frame, text='stop simulation', state=DISABLED,
                                              command=self.stop_simulation)
        stop_button.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        self.configure_widget(parent_frame, row_list=[0, 1, 2], col_list=[0], row_weight_list=[1, 1, 1],
                              col_weight_list=[1])
        return start_from_scratch_button, resume_button, stop_button

    @staticmethod
    def create_secondary_window(parent_window):
        window = customtkinter.CTkToplevel(parent_window)
        window.title('Set the parameters of the simulation')
        window.geometry("800x300")
        return window

    def create_parameter_frame(self, parent_frame):
        parameter_frame = customtkinter.CTkFrame(parent_frame)
        parameter_frame.grid(row=0, column=0, sticky='nsew')
        self.configure_widget(parent_frame, row_list=[0, 1], col_list=[0], row_weight_list=[3, 1],
                              col_weight_list=[1])
        return parameter_frame

    def create_start_parameter_entries(self, parent_frame):
        # q_count frame
        q_count_frame = customtkinter.CTkFrame(parent_frame)
        q_count_frame.grid(row=0, column=0, sticky='nsew')
        # q_count label
        q_count_label = customtkinter.CTkLabel(q_count_frame, text='q_count')
        q_count_label.grid(row=0, column=0, sticky='nsew')
        # q_count entry
        q_count_entry = customtkinter.CTkEntry(q_count_frame)
        q_count_entry.insert(0, str(3))
        q_count_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(q_count_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1], col_weight_list=[1, 1])

        # q_min frame
        q_min_frame = customtkinter.CTkFrame(parent_frame)
        q_min_frame.grid(row=1, column=0, sticky='nsew')
        # q_min label
        q_min_label = customtkinter.CTkLabel(q_min_frame, text='q_min')
        q_min_label.grid(row=0, column=0, sticky='nsew')
        # q_min entry
        q_min_entry = customtkinter.CTkEntry(q_min_frame)
        q_min_entry.insert(0, str(0))
        q_min_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(q_min_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1], col_weight_list=[1, 1])

        # q_max frame
        q_max_frame = customtkinter.CTkFrame(parent_frame)
        q_max_frame.grid(row=2, column=0, sticky='nsew')
        # q_max label
        q_max_label = customtkinter.CTkLabel(q_max_frame, text='q_max')
        q_max_label.grid(row=0, column=0, sticky='nsew')
        # q_max entry
        q_max_entry = customtkinter.CTkEntry(q_max_frame)
        q_max_entry.insert(0, str(10))
        q_max_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(q_max_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1], col_weight_list=[1, 1])

        # sv_mat_row_count frame
        sv_mat_row_count_frame = customtkinter.CTkFrame(parent_frame)
        sv_mat_row_count_frame.grid(row=0, column=1, sticky='nsew')
        # sv_mat_row_count label
        sv_mat_row_count_label = customtkinter.CTkLabel(sv_mat_row_count_frame, text='small variations\n amount')
        sv_mat_row_count_label.grid(row=0, column=0, sticky='nsew')
        # sv_mat_row_count entry
        sv_mat_row_count_entry = customtkinter.CTkEntry(sv_mat_row_count_frame)
        sv_mat_row_count_entry.insert(0, str(7))
        sv_mat_row_count_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(sv_mat_row_count_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1],
                              col_weight_list=[1, 1])

        # pm_row_count frame
        pm_row_count_frame = customtkinter.CTkFrame(parent_frame)
        pm_row_count_frame.grid(row=1, column=1, sticky='nsew')
        # pm_row_count label
        pm_row_count_label = customtkinter.CTkLabel(pm_row_count_frame, text='parse matrix\n row amount')
        pm_row_count_label.grid(row=0, column=0, sticky='nsew')
        # pm_row_count entry
        pm_row_count_entry = customtkinter.CTkEntry(pm_row_count_frame)
        pm_row_count_entry.insert(0, str(10))
        pm_row_count_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(pm_row_count_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1],
                              col_weight_list=[1, 1])

        # elite_size frame
        elite_size_frame = customtkinter.CTkFrame(parent_frame)
        elite_size_frame.grid(row=2, column=1, sticky='nsew')
        # elite_size label
        elite_size_label = customtkinter.CTkLabel(elite_size_frame, text='elite population\n size')
        elite_size_label.grid(row=0, column=0, sticky='nsew')
        # elite_size entry
        elite_size_entry = customtkinter.CTkEntry(elite_size_frame)
        elite_size_entry.insert(0, str(5))
        elite_size_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(elite_size_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1],
                              col_weight_list=[1, 1])

        # pop_size frame
        pop_size_frame = customtkinter.CTkFrame(parent_frame)
        pop_size_frame.grid(row=0, column=2, sticky='nsew')
        # pop_size label
        pop_size_label = customtkinter.CTkLabel(pop_size_frame, text='population\n size')
        pop_size_label.grid(row=0, column=0, sticky='nsew')
        # pop_size entry
        pop_size_entry = customtkinter.CTkEntry(pop_size_frame)
        pop_size_entry.insert(0, str(100))
        pop_size_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(pop_size_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1],
                              col_weight_list=[1, 1])

        # max_gens frame
        max_gens_frame = customtkinter.CTkFrame(parent_frame)
        max_gens_frame.grid(row=1, column=2, sticky='nsew')
        # max_gens label
        max_gens_label = customtkinter.CTkLabel(max_gens_frame, text='generations')
        max_gens_label.grid(row=0, column=0, sticky='nsew')
        # max_gens entry
        max_gens_entry = customtkinter.CTkEntry(max_gens_frame)
        max_gens_entry.insert(0, str(5))
        max_gens_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(max_gens_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1],
                              col_weight_list=[1, 1])

        # reset_gens frame
        reset_gens_frame = customtkinter.CTkFrame(parent_frame)
        reset_gens_frame.grid(row=2, column=2, sticky='nsew')
        # reset_gens label
        reset_gens_label = customtkinter.CTkLabel(reset_gens_frame, text='generational \nconvergence limit')
        reset_gens_label.grid(row=0, column=0, sticky='nsew')
        # reset_gens entry
        reset_gens_entry = customtkinter.CTkEntry(reset_gens_frame)
        reset_gens_entry.insert(0, str(25))
        reset_gens_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(reset_gens_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1],
                              col_weight_list=[1, 1])

        self.configure_widget(parent_frame, row_list=[0, 1, 2], col_list=[0, 1, 2], row_weight_list=[1, 1, 1],
                              col_weight_list=[1, 1, 1])
        return (q_count_entry, q_min_entry, q_max_entry, sv_mat_row_count_entry, pm_row_count_entry, pop_size_entry,
                elite_size_entry, max_gens_entry, reset_gens_entry)

    def create_resume_parameter_entries(self, parent_frame):
        # max_gens frame
        max_gens_frame = customtkinter.CTkFrame(parent_frame)
        max_gens_frame.grid(row=1, column=2, sticky='nsew')
        # max_gens label
        max_gens_label = customtkinter.CTkLabel(max_gens_frame, text='generations')
        max_gens_label.grid(row=0, column=0, sticky='nsew')
        # max_gens entry
        max_gens_entry = customtkinter.CTkEntry(max_gens_frame)
        max_gens_entry.insert(0, str(5))
        max_gens_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(max_gens_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1],
                              col_weight_list=[1, 1])

        # reset_gens frame
        reset_gens_frame = customtkinter.CTkFrame(parent_frame)
        reset_gens_frame.grid(row=2, column=2, sticky='nsew')
        # reset_gens label
        reset_gens_label = customtkinter.CTkLabel(reset_gens_frame, text='generational \nconvergence limit')
        reset_gens_label.grid(row=0, column=0, sticky='nsew')
        # reset_gens entry
        reset_gens_entry = customtkinter.CTkEntry(reset_gens_frame)
        reset_gens_entry.insert(0, str(25))
        reset_gens_entry.grid(row=0, column=1, sticky='nsew')
        self.configure_widget(reset_gens_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1],
                              col_weight_list=[1, 1])

        self.configure_widget(parent_frame, row_list=[0], col_list=[0, 1], row_weight_list=[1],
                              col_weight_list=[1, 1])
        return max_gens_entry, reset_gens_entry

    def create_secondary_window_button_frame(self, parent_frame):
        # button frame
        buttons_frame = customtkinter.CTkFrame(parent_frame)
        buttons_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        # next button
        start_button = customtkinter.CTkButton(buttons_frame, text='Next')
        start_button.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)

        self.configure_widget(buttons_frame, row_list=[0], col_list=[0], row_weight_list=[1],
                              col_weight_list=[1])
        return start_button

    def ask_user_for_optimization_file(self):
        # self.artificially_create_optimization_data()
        # check if the optimization folder exits, if not then create it
        self.fm.check_and_create_folder(self.optimization_data_folder_path)
        optimization_zip_file_path = askopenfilename(initialdir=self.optimization_data_folder_path,
                                                     title='Select Optimization Zip File',
                                                     filetypes=[("zip files", "*.zip")])

        while optimization_zip_file_path == '':
            # the user did not select anything
            if messagebox.askokcancel("Quit", "You did not select a valid optimization file\n retry?"):
                optimization_zip_file_path = askopenfilename(initialdir=self.optimization_data_folder_path,
                                                             title='Select Optimization Zip File',
                                                             filetypes=[("zip files", "*.zip")])
            else:
                break
        if optimization_zip_file_path == '':
            pass
        else:
            self.start_from_scratch_button.configure(state=DISABLED)
            self.resume_button.configure(state=DISABLED)
            print('optimization file selected properly')

            # extract optimization shelve file
            self.fm.unzip_to_folder(zip_file_path=optimization_zip_file_path,
                                    folder_to_unzip=self.optimization_data_folder_path)
            self.create_fill_show_secondary_start_window()

    def ask_user_for_resume_file(self):
        # check if the resume folder exits, if not then create it
        self.fm.check_and_create_folder(self.resume_data_folder_path)
        resume_zip_file_path = askopenfilename(initialdir=self.resume_data_folder_path, title='Select Resume Zip File',
                                               filetypes=[("zip files", "*.zip")])

        while resume_zip_file_path == '':
            # the user did not select anything
            if messagebox.askokcancel("Quit", "You did not select a valid resume file\n retry?"):
                resume_zip_file_path = askopenfilename(initialdir=self.resume_data_folder_path,
                                                       title='Select Resume Zip File',
                                                       filetypes=[("zip files", "*.zip")])
            else:
                break
        if resume_zip_file_path == '':
            pass
        else:
            self.start_from_scratch_button.configure(state=DISABLED)
            self.resume_button.configure(state=DISABLED)
            print('resume file selected properly')

            # extract resume shelve file
            self.fm.unzip_to_folder(zip_file_path=resume_zip_file_path,
                                    folder_to_unzip=self.resume_data_folder_path)
            self.create_fill_show_secondary_resume_window()

    def create_fill_show_secondary_start_window(self):
        # #####################################parameter frame###############################
        top = self.create_secondary_window(self.root)
        self.start_from_scratch_button.configure(state=DISABLED)
        self.resume_button.configure(state=DISABLED)
        top.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(top))
        parameter_frame = self.create_parameter_frame(top)
        (q_count_entry, q_min_entry, q_max_entry, sv_mat_row_count_entry, pm_row_count_entry, pop_size_entry,
         elite_size_entry, max_gens_entry, reset_gens_entry) = self.create_start_parameter_entries(parameter_frame)
        start_button = self.create_secondary_window_button_frame(top)
        start_button.configure(command=lambda: self.start(top, q_count_entry, q_min_entry,
                                                          q_max_entry, sv_mat_row_count_entry,
                                                          pm_row_count_entry, pop_size_entry, elite_size_entry,
                                                          max_gens_entry, reset_gens_entry))

    def create_fill_show_secondary_resume_window(self):
        # #####################################parameter frame###############################
        top = self.create_secondary_window(self.root)
        self.start_from_scratch_button.configure(state=DISABLED)
        self.resume_button.configure(state=DISABLED)
        top.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(top))
        parameter_frame = self.create_parameter_frame(top)
        max_gens_entry, reset_gens_entry = self.create_resume_parameter_entries(parameter_frame)
        start_button = self.create_secondary_window_button_frame(top)
        start_button.configure(command=lambda: self.resume(top, max_gens_entry, reset_gens_entry))

    def start(self, top_window, q_count_entry, q_min_entry, q_max_entry, sv_mat_row_count_entry, pm_row_count_entry,
              pop_size_entry, elite_size_entry, max_gens_entry, reset_gens_entry):
        # get simulation parameters from the user
        (q_count, q_min, q_max, sv_mat_row_count, pm_row_count, pop_size, elite_size, max_gens, reset_max_attempts) = \
            self.get_start_simulation_parameters(q_count_entry, q_min_entry, q_max_entry, sv_mat_row_count_entry,
                                                 pm_row_count_entry, pop_size_entry, elite_size_entry, max_gens_entry,
                                                 reset_gens_entry)
        top_window.destroy()
        # get target parameters
        func_count = len(function_list)
        max_arg_count = 3
        # get the optimization data from the optimization shelf file
        x_count, u_count, u_min, u_max, x_data, y_target = self.get_optimization_data()
        # delete the shelf file after getting the optimization data
        self.fm.delete_shelf_files(self.optimization_data_folder_path)
        sr = SymbolicRegression(max_arg_count, pm_row_count, x_count, u_count, q_count, q_min, q_max, sv_mat_row_count,
                                func_count, u_min, u_max, pop_size, elite_size, x_data, y_target)

        # check resume and optimization folders
        sr.check_folders()
        # elite population initialization
        elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions = sr.initialize_elite_solutions()
        # initial population generation, score and probabilities calculation
        pop_sv, pop_q, scores, probabilities = sr.initial_population_generation_and_score_calculation()
        # create the resume file
        sr.create_resume_file(elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions, pop_sv, pop_q, scores,
                              probabilities)
        # best individual calculation
        best_sv_mat, best_q, generation_best_score, best_y, best_expression = sr.best_solution_calculation(pop_sv,
                                                                                                           pop_q,
                                                                                                           scores)

        # stack in the elite population and save the elite information in disk
        elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions = sr.elite.stack(best_sv_mat, best_q,
                                                                                        generation_best_score,
                                                                                        best_y, best_expression,
                                                                                        elite_svs, elite_qs,
                                                                                        elite_scores, elite_ys,
                                                                                        elite_expressions)

        current_attempt = 0
        simulation_best_score = generation_best_score
        print('current generation = initial, best score = ', generation_best_score, 'best historic score = ',
              elite_scores[0], 'times stuck=', current_attempt)
        # starts the genetic algorithm main loop
        current_generation = 0
        self.stop_button.configure(state=NORMAL)
        self.main_loop(sr, pop_sv, pop_q, scores, probabilities, elite_svs, elite_qs, elite_scores, elite_ys,
                       elite_expressions, current_generation, max_gens, reset_max_attempts, current_attempt,
                       simulation_best_score, generation_best_score[0], best_expression[0])

    def main_loop(self, sr, pop_sv, pop_q, scores, probabilities, elite_svs, elite_qs, elite_scores, elite_ys,
                  elite_expressions, current_generation, max_gens, reset_max_attempts, current_attempt,
                  simulation_best_score, generation_best_score, best_expression):
        if current_generation < max_gens and self.continue_flag:
            (pop_sv, pop_q, probabilities, elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions,
             current_generation, reset_max_attempts, current_attempt, simulation_best_score) = \
                sr.main_loop(pop_sv, pop_q, probabilities, elite_svs, elite_qs, elite_scores, elite_ys,
                             elite_expressions, current_generation, reset_max_attempts, current_attempt,
                             simulation_best_score)

            self.root.after(ms=10, func=lambda: self.main_loop(sr, pop_sv, pop_q, scores, probabilities, elite_svs,
                                                               elite_qs, elite_scores, elite_ys, elite_expressions,
                                                               current_generation, max_gens, reset_max_attempts,
                                                               current_attempt, simulation_best_score,
                                                               generation_best_score, best_expression))
        else:

            print('main loop finished, reached max gens')
            print('saving resume data to a zip file')
            sr.save_resume_file(elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions, pop_sv, pop_q, scores,
                                probabilities)
            u_data_array = elite_individuals
            x_data_array = optimizer.population_obj.calculate_states(u_data_array, optimizer.x0, optimizer.h)
            optimizer.create_plot_file(x_data_array, u_data_array)
            optimizer.backup_all_data_to_zip(self.resume_zip_file_path, first_time=self.first_time)
            sr.backup_resume_data_to_zip()
            print('Program Done.')
            print('main loop finished, reached max gens')
            print('saving resume data to a zip file')
            self.plot_button.configure(state=NORMAL)
            self.start_from_scratch_button.configure(state=NORMAL)
            self.stop_button.configure(state=DISABLED)
            self.resume_button.configure(state=NORMAL)
            self.continue_flag = True
            print('Program Done.')

    def resume(self, top_window, max_gens_entry, reset_gens_entry):
        # get simulation parameters from the user
        max_gens, reset_max_attempts = self.get_resume_simulation_parameters(max_gens_entry, reset_gens_entry)
        # get the rest of the simulation parameters from the resume file
        (x_count, u_count, u_min, u_max, x_data, y_target, q_count, q_min, q_max, sv_mat_row_count, pm_row_count,
         pop_size, elite_size, elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions, pop_sv, pop_q, scores,
         probabilities) = self.get_resume_data()
        top_window.destroy()
        func_count = len(function_list)
        max_arg_count = 3
        sr = SymbolicRegression(max_arg_count, pm_row_count, x_count, u_count, q_count, q_min, q_max, sv_mat_row_count,
                                func_count, u_min, u_max, pop_size, elite_size, x_data, y_target)
        # best individual calculation
        best_sv_mat, best_q, generation_best_score, best_y, best_expression = sr.best_solution_calculation(pop_sv,
                                                                                                           pop_q,
                                                                                                           scores)
        # stack in the elite population and save the elite information in disk
        elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions = sr.elite.stack(best_sv_mat, best_q,
                                                                                        generation_best_score,
                                                                                        best_y, best_expression,
                                                                                        elite_svs, elite_qs,
                                                                                        elite_scores, elite_ys,
                                                                                        elite_expressions)
        current_attempt = 0
        simulation_best_score = generation_best_score
        print('current generation = initial, best score = ', generation_best_score, 'best historic score = ',
              elite_scores[0], 'times stuck=', current_attempt)
        # starts the genetic algorithm main loop
        current_generation = 0
        self.stop_button.configure(state=NORMAL)
        self.update_user_output(current_generation, generation_best_score, elite_scores[0], best_expression)
        main_loop_thread = threading.Thread(target=sr.main_loop, args=[pop_sv, pop_q, scores, probabilities,
                                                                             elite_svs, elite_qs, elite_scores, elite_ys
                                                                             , elite_expressions, current_generation,
                                                                             max_gens, reset_max_attempts,
                                                                             current_attempt, simulation_best_score,
                                                                       self.stop_flag])
        # main_loop_thread = threading.Thread(target=self.long_function)
        main_loop_thread.start()
        # self.main_loop(main_loop_thread, current_generation, generation_best_score, elite_scores[0], best_expression)

        print('the resume routine has finished')
        # main_thread.join()
        
    def update_user_output(self, current_generation, generation_best_score, best_historic_score, best_expression):
        self.generation_label.configure(text='Generation: ' + str(current_generation))
        self.score_label.configure(text='Generation Best Score:\n' + str(generation_best_score))
        self.historic_score_label.configure(text='Best Historic Score:\n' + str(best_historic_score))
        self.expression_label.configure(text='Generation Best Expression:\n' + str(best_expression))

    def on_closing(self, window):
        if messagebox.askokcancel("Quit",
                                  "You did not save the parameters of the simulation\nAre you sure, you want to quit?"):
            self.start_from_scratch_button.configure(state=NORMAL)
            self.resume_button.configure(state=NORMAL)
            window.destroy()

    def get_optimization_data(self):
        reg_shelf_file = shelve.open(str(self.optimization_data_folder_path / Path('optimization')))
        x_count = reg_shelf_file['x_count']
        u_count = reg_shelf_file['u_count']
        u_min = reg_shelf_file['u_min']
        u_max = reg_shelf_file['u_max']
        x_data = reg_shelf_file['x_data']
        y_target = reg_shelf_file['y_target']
        reg_shelf_file.close()
        return x_count, u_count, u_min, u_max, x_data, y_target

    def get_resume_data(self):
        reg_shelf_file = shelve.open(str(self.resume_data_folder_path / Path('resume')))
        x_count = reg_shelf_file['x_count']
        u_count = reg_shelf_file['u_count']
        u_min = reg_shelf_file['u_min']
        u_max = reg_shelf_file['u_max']
        x_data = reg_shelf_file['x_data']
        y_target = reg_shelf_file['y_target']

        q_count = reg_shelf_file['q_count']
        q_min = reg_shelf_file['q_min']
        q_max = reg_shelf_file['q_max']

        pm_row_count = reg_shelf_file['pm_row_count']
        sv_mat_row_count = reg_shelf_file['sv_mat_row_count']

        pop_size = reg_shelf_file['pop_size']
        elite_size = reg_shelf_file['elite_size']

        elite_svs = reg_shelf_file['elite_svs']
        elite_qs = reg_shelf_file['elite_qs']
        elite_scores = reg_shelf_file['elite_scores']
        elite_ys = reg_shelf_file['elite_ys']
        elite_expressions = reg_shelf_file['elite_expressions']

        pop_sv = reg_shelf_file['pop_sv']
        pop_q = reg_shelf_file['pop_q']
        scores = reg_shelf_file['scores']
        probabilities = reg_shelf_file['probabilities']

        reg_shelf_file.close()
        return (x_count, u_count, u_min, u_max, x_data, y_target, q_count, q_min, q_max, sv_mat_row_count, pm_row_count,
                pop_size, elite_size, elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions, pop_sv, pop_q,
                scores, probabilities)

    @staticmethod
    def get_start_simulation_parameters(q_count_entry, q_min_entry, q_max_entry, sv_mat_row_count_entry,
                                        pm_row_count_entry, pop_size_entry, elite_size_entry, max_gens_entry,
                                        reset_gens_entry):
        q_count = int(q_count_entry.get())
        q_min = int(q_min_entry.get())
        q_max = int(q_max_entry.get())
        sv_mat_row_count = int(sv_mat_row_count_entry.get())
        pm_row_count = int(pm_row_count_entry.get())
        pop_size = int(pop_size_entry.get())
        elite_size = int(elite_size_entry.get())
        max_gens = int(max_gens_entry.get())
        reset_gens = int(reset_gens_entry.get())
        return q_count, q_min, q_max, sv_mat_row_count, pm_row_count, pop_size, elite_size, max_gens, reset_gens

    @staticmethod
    def get_resume_simulation_parameters(max_gens_entry, reset_gens_entry):
        max_gens = int(max_gens_entry.get())
        reset_gens = int(reset_gens_entry.get())
        return max_gens, reset_gens

    def artificially_create_optimization_data(self):
        self.fm.check_and_create_folder(self.optimization_data_folder_path)
        x = np.array([[uniform(-10, 10) for _ in range(50)] for _ in range(3)])
        y_target = np.sin(x[0]) + np.cos(x[1]) - 0.5 * x[2]
        reg_shelf_file = shelve.open(str(self.optimization_data_folder_path / Path('optimization')))
        reg_shelf_file['x_count'] = 3
        reg_shelf_file['u_count'] = 1
        reg_shelf_file['u_min'] = -10
        reg_shelf_file['u_max'] = 10
        reg_shelf_file['x_data'] = x
        reg_shelf_file['y_target'] = y_target
        reg_shelf_file.close()
        self.fm.backup_all_shelve_files_to_zip_files(self.optimization_data_folder_path,
                                                     self.optimization_data_folder_path, basename='optimization')
        self.fm.delete_shelf_files(self.optimization_data_folder_path)
