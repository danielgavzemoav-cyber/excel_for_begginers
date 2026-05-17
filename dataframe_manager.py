
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


### cleaning the data
def load_clean_csv(filepath):
    raw = pd.read_csv(filepath, header=None)

    for col_name, col_data in raw.items():
        if pd.to_numeric(col_data, errors='coerce').notna().mean() < 0.5:
            continue

        last_string_idx = 0

        for i, value in enumerate(col_data):
            try:
                float(value)
                if pd.isna(value):
                    raise ValueError
                break
            except (ValueError, TypeError):
                if pd.notna(value):  # only update if value is not NaN
                    last_string_idx = i


        header = col_data.iloc[last_string_idx]
        data = pd.to_numeric(col_data.iloc[last_string_idx + 1:], errors='coerce')
        data = data.dropna().reset_index(drop=True)
        data.name = header

        raw[col_name] = data
        raw.rename(columns={col_name: header}, inplace=True)

    raw.dropna(axis=1, how='all', inplace=True)

    return raw.loc[:, raw.dtypes == float]

#print(clean_our_data.dtypes)

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

    ####plotting things


    def our_plot_hist(self,stat1,variable):
        #counts the number of times a value arrives
        #new_data = pd.cut(clean[stat], bins = variable).value_counts()
        sns.histplot(self.clean[stat1], bins = variable)
        plt.show()
        plt.close()

    ## to do here a function that limits the values enter the histogram


    def our_plot_scat(self,stat1,stat2):
        sns.scatterplot(data = self.clean, x = stat1, y = stat2,s = 1)
        plt.show()
        plt.close()


    def our_boxplot(self,stat1):
        sns.boxplot(data = self.clean[[stat1]])
        plt.show()
        plt.close()


    ### inserting the data
filepath = input('Enter file path of your CSV: ')
Analyser = data_analist(filepath)

while True:
    print('\n Choose Category: ')
    print('1: Statistics')
    print('2: Columns operations')
    print('3: Plotting')
    print('q: Quit')
    category = str(input('\nEnter your choice: '))
    try:
        if category == 'q':
            break

        elif category == '1':
            while True:
                print('\nChoose Statistics: ')
                print('1: mean, std, variance, max, min,\n count, 25%, 50%, 75% ')
                print('2: Amplitude')
                print('3: Peek to peek')
                print('4: Covariance')
                print('5: RMS')
                print('q: Back to main menu')
                statistic = str(input('\nEnter your choice: '))
                if statistic == 'q':
                    break
                elif statistic == '1':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col = input('\nWhat column do you want to use? :  ')
                    stat1 = input('\n Choose one :mean, std, variance, max, min,\n count, 25%, 50%, 75% ')
                    try:
                        print(Analyser.our_data_describe(col, stat1))
                    except KeyError:
                        print('Column or stat not found, please try again')
                elif statistic == '2':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col = input('\nWhat column do you want to use? :  ')
                    try:
                        print(Analyser.our_data_amplitude(col))
                    except KeyError:
                        print('Column not found, please try again')
                elif statistic == '3':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col = input('\nWhat column do you want to use? :  ')
                    try:
                        print(Analyser.our_data_peek_to_peek(col))
                    except KeyError:
                        print('Column not found, please try again')
                elif statistic == '4':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col1 = input('\nWhat column do you want to use? :  ')
                    col2 = input('\nWhat other column do you want to use? :  ')
                    try:
                        print(Analyser.our_data_covariance(col1, col2))
                    except KeyError:
                        print('Column not found, please try again')
                elif statistic == '5':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col = input('\nWhat column do you want to use? :  ')
                    try:
                        print(Analyser.our_data_RMS(col))
                    except KeyError:
                        print('Column not found, please try again')
                else:
                    print('Invalid choice, please try again')
        elif category == '2':
            while True:
                print('\nChoose columns operation: ')
                print('1: addition')
                print('2: subtraction')
                print('3: multiplication')
                print('4: division')
                print('q: Back to main menu')
                operation = str(input('\nEnter your choice: '))
                if operation == 'q':
                    break
                elif operation == '1':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col1 = input('\nWhat column do you want to use? :  ')
                    col2 = input('\nWhat other column do you want to use? :  ')
                    try:
                        Analyser.adding_col(col1, col2)
                        print('\nThe new column', Analyser.clean[col1 + '+' + col2])
                    except KeyError:
                        print('Column not found, please try again')
                elif operation == '2':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col1 = input('\nWhat column do you want to use? :  ')
                    col2 = input('\nWhat other column do you want to use? :  ')
                    try:
                        Analyser.subtracting_col(col1, col2)
                        print('\nThe new column', Analyser.clean[col1 + '-' + col2])
                    except KeyError:
                        print('Column not found, please try again')
                elif operation == '3':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col1 = input('\nWhat column do you want to use? :  ')
                    col2 = input('\nWhat other column do you want to use? :  ')
                    try:
                        Analyser.multiplication_col(col1, col2)
                        print('\nThe new column', Analyser.clean[col1 + '*' + col2])
                    except KeyError:
                        print('Column not found, please try again')
                elif operation == '4':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col1 = input('\nWhat column do you want to use? :  ')
                    col2 = input('\nWhat other column do you want to use? :  ')
                    try:
                        Analyser.division_col(col1, col2)
                        print('\nThe new column', Analyser.clean[col1 + '/' + col2])
                    except KeyError:
                        print('Column not found, please try again')
                    except ZeroDivisionError:
                        print('Cannot divide by zero')
                else:
                    print('Invalid choice, please try again')
        elif category == '3':
            while True:
                print('\nWhat kind of graph do you want?')
                print('1: Histogram')
                print('2: Scatter')
                print('3: Boxplot')
                print('q: Back to main menu')
                graph = str(input('\nEnter your choice: '))
                if graph == 'q':
                    break
                elif graph == '1':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col1 = input('\nWhat column do you want to use? :  ')
                    try:
                        variable = int(input('\nHow many Bars do you want? :  '))
                        Analyser.our_plot_hist(col1, variable)
                    except ValueError:
                        print('Please enter a valid number')
                    except KeyError:
                        print('Column not found, please try again')
                elif graph == '2':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col1 = input('\nWhat column do you want to use? :  ')
                    col2 = input('\nwhat other column do you want to use? :  ')
                    try:
                        Analyser.our_plot_scat(col1, col2)
                    except KeyError:
                        print('Column not found, please try again')
                elif graph == '3':
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col1 = input('\nWhat column do you want to use? :  ')
                    try:
                        Analyser.our_boxplot(col1)
                    except KeyError:
                        print('Column not found, please try again')
                else:
                    print('Invalid choice, please try again')
        else:
            print('Invalid choice, please try again')
    except KeyError:
        print('Column not found, please try again')
    except ValueError:
        print('Please enter a valid number')

print('Goodbye!')
##usage of the class

#Analyser = data_analist('/home/daniel/Documents/lab_3/T2_7.CSV')

"""
print(Analyser.our_data_amplitude(col))
print(Analyser.our_data_peek_to_peek(col))
print(Analyser.our_data_covariance('1 (VOLT)','3 (VOLT)'))
print(Analyser.our_data_RMS('1 (VOLT)'))
print(Analyser.adding_col('1 (VOLT)','3 (VOLT)'))
print(Analyser.subtracting_col('1 (VOLT)','3 (VOLT)'))
print(Analyser.multiplication_col('1 (VOLT)','3 (VOLT)'))
print(Analyser.division_col('1 (VOLT)','3 (VOLT)'))
Analyser.our_plot_hist('1 (VOLT)',50)
Analyser.our_plot_scat('1 (VOLT)','Time (s)')
Analyser.our_boxplot('1 (VOLT)')

"""