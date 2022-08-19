from file_manager import FileManager
import shelve
import shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import zipfile
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from tkinter import Text
from tkinter import END
from tkinter import Frame
# from tkinter import Button
from tkinter import INSERT
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Plotter:
    def __init__(self):
        self.fm = FileManager()

        self.current_path = Path.cwd()
        self.live_reg_data_folder_path = self.fm.live_reg_data_folder_path
        self.history_data_folder_path = self.fm.history_data_folder_path
        # root
        self.root = Tk()
        self.root.title('Symbolic Regression')
        self.root.geometry("1000x1000")
        # its self frame
        self.main_frame = Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="NSWE")

        # figure canvas
        self.fig, self.ax = self.generate_figure()
        self.chart = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.chart.get_tk_widget().grid(row=0, column=0, sticky="NSWE")
        self.plot_count = 0

        # text box for the expression
        self.expression_display = Text(self.main_frame, width=40, height=10, font=("Helvetica", 16))
        self.expression_display.grid(row=1, column=0, sticky="NSWE")
        self.expression_display.insert(END, "Expression: ")
        # self.plot_history_button = Button(self.main_frame, text='plot history', command=self.plot_history_data)
        # self.plot_history_button.grid(row=2, column=0)
        
        # fonts
        self.font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
        self.font2 = {'family': 'serif', 'color': 'blue', 'size': 15}

        self.current_generation = 0
        self.max_generations = 100
        self.continue_flag = True

        self.fm.backup_history_results()
        # unzip history results
        self.unzipped_file_path = self.unzip_history_data()
        # get the target data
        self.x, self.y_target, self.y_target_expression = self.get_target_data()
        self.y_regression = np.zeros_like(self.x)
        self.y_regression_expression = "0"

    @staticmethod
    def generate_figure():
        fig, ax = plt.subplots(num=1, clear=True, figsize=(10, 8), dpi=80)
        return fig, ax

    def plot(self, x, y_target, y_regression, current_generation):
        # plot the solution
        self.ax.plot(x, y_target, '-b', linewidth=2, label='target')
        self.ax.plot(x, y_regression, '--r',
                     linewidth=2, label='regression' + str(current_generation))
        self.ax.legend(loc="upper left")
        # handles, labels = plt.gca().get_legend_handles_labels()
        # by_label = dict(zip(labels, handles))
        # ax.legend(by_label.values(), by_label.keys(), loc="upper left")
        self.chart.draw()

    def clear_figure(self):
        self.ax.clear()
        self.ax.set_title("target function vs regression function", fontdict=self.font1)
        self.ax.set_xlabel("independent variable-x", fontdict=self.font2)
        self.ax.set_ylabel("dependent variable-y", fontdict=self.font2)
    
    def unzip_history_data(self):
        zip_file_path = askopenfilename(initialdir=self.history_data_folder_path, title='Select Zip File',
                                        filetypes=[("zip files", "*.zip")])
        zip_file_path = Path(zip_file_path)
        # file name without extension
        zip_file_name = zip_file_path.stem
        unzipped_file_path = self.history_data_folder_path / zip_file_name
        zip_object = zipfile.ZipFile(zip_file_path)
        # extract all the files from the folder
        zip_object.extractall(unzipped_file_path)
        return unzipped_file_path

    def get_target_data(self):
        # getting the target shelf file information
        target_shelf_file = shelve.open(str(self.unzipped_file_path / Path('target')))
        x = target_shelf_file['x_data']
        y_target = target_shelf_file['y_target']
        y_target_expression = target_shelf_file['y_target_expression']
        target_shelf_file.close()
        return x, y_target, y_target_expression

    def get_generation_data(self, file_name):
        reg_shelf_file = shelve.open(str(self.unzipped_file_path / Path(file_name)))
        self.y_regression = reg_shelf_file['y_regression']
        self.y_regression_expression = reg_shelf_file['y_regression_expression']
        reg_shelf_file.close()

    def plot_history_data(self):
        file_name = 'reg_' + str(self.current_generation)
        if self.fm.check_shelve_file(self.unzipped_file_path, file_name):
            self.get_generation_data(file_name)
            my_x = self.x[0]
            my_y_regression = self.y_regression[0]
            sorted_indexes = np.argsort(my_x)
            self.clear_figure()
            self.plot(my_x[sorted_indexes], self.y_target[sorted_indexes], my_y_regression[sorted_indexes],
                      self.current_generation)
            self.chart.get_tk_widget().after(1000, self.plot_history_data)
            self.expression_display.delete('1.0', END)
            self.expression_display.insert(INSERT, 'target: ' + self.y_target_expression)
            self.expression_display.insert(END, '\nregression: ' + self.y_regression_expression[0])
            self.expression_display.insert(END, '\ngeneration: ' + str(self.current_generation))
            self.current_generation += 1
        else:
            # delete the unzipped folder and all its content
            shutil.rmtree(self.unzipped_file_path)
            self.continue_flag = False
            print('\n Program Done.')
