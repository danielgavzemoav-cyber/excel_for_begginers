#float_analysis.py


import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from cleaning import load_clean_csv
class data_analist:
    def __init__(self, filepath):
        self.clean = load_clean_csv(filepath)


   ##now after we cleaned the data we can start apply some statistical manipulations
    def our_data_describe(self, col, stat1):
        describe_data = self.clean.describe()
        describe_data = describe_data.transpose()
        return describe_data.loc[col, stat1]

    #amplitude (half the difference between the greatest value to the lowest value)

    def our_data_amplitude (self,stat1):
        amplitude_data = (self.clean[stat1].max() - self.clean[stat1].min())*0.5
        return amplitude_data

    def our_data_peek_to_peek (self,stat1):
        #needed_data = clean.loc[:, clean.dtypes == float]
        peek_to_peek_data = (self.clean[stat1].max() - self.clean[stat1].min())
        return peek_to_peek_data

    def our_data_covariance(self, stat1, stat2):
        #needed_data = clean.loc[:, clean.dtypes == float]
        cov_mat = self.clean.cov()
        return cov_mat.loc[stat1, stat2]

    def our_data_RMS (self,stat1):
        RMS_data =  np.sqrt((self.clean[stat1]**2).mean())
        return RMS_data

    #columns operations

    def adding_col(self, stat1, stat2):
        self.clean[stat1 + '+' + stat2] = self.clean[stat1] + self.clean[stat2]

    def subtracting_col(self, stat1, stat2):
        self.clean[stat1 + '-' + stat2] = self.clean[stat1] - self.clean[stat2]

    def multiplication_col(self, stat1, stat2):
        self.clean[stat1 + '*' + stat2] = self.clean[stat1] * self.clean[stat2]

    def division_col(self, stat1, stat2):
        self.clean[stat1 + '/' + stat2] = self.clean[stat1] / self.clean[stat2]

    def save_option(self):
        save = input('\nDo you want to save? (y/n): ')
        if save == 'y':
            save_path = input('Enter file path to save: ')
            try:
                self.clean.to_csv(save_path, index=False)
                print(f'File saved successfully to {save_path}')
            except Exception as e:
                print(f'Error saving file: {e}')
    ####plotting things


    def our_plot_hist(self,stat1,variable):
        #counts the number of times a value arrives
        #new_data = pd.cut(clean[stat], bins = variable).value_counts()
        sns.histplot(self.clean[stat1], bins = variable)
        plt.show()
        plt.close()

    ## to do here a function that limits the values enter the histogram


    def our_plot_scat(self,stat1,stat2):
        sns.scatterplot(data = self.clean, x = stat1, y = stat2,s = 20)
        plt.show()
        plt.close()

    def our_plot_scat_error_both(self,stat1,stat2,stat1_err,stat2_err):
        sns.scatterplot(data = self.clean, x = stat1, y = stat2, s = 1)
        plt.errorbar(self.clean[stat1],self.clean[stat2],xerr=self.clean[stat1_err],yerr=self.clean[stat2_err],fmt='none',ecolor='red')
        plt.show()
        plt.close()

    def our_plot_scat_error_x(self,stat1,stat2,stat1_err):
        sns.scatterplot(data = self.clean, x = stat1, y = stat2, s = 1)
        plt.errorbar(self.clean[stat1],self.clean[stat2],xerr=self.clean[stat1_err],fmt='none',ecolor='red')
        plt.show()
        plt.close()

    def our_plot_scat_error_y(self, stat1, stat2, stat2_err):
        sns.scatterplot(data=self.clean, x=stat1, y=stat2, s=1)
        plt.errorbar(self.clean[stat1], self.clean[stat2], yerr=self.clean[stat2_err],fmt='none', ecolor='red')
        plt.show()
        plt.close()
    def our_boxplot(self,stat1):
        sns.boxplot(data = self.clean[[stat1]])
        plt.show()
        plt.close()