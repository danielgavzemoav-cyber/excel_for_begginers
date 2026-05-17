#main.py
from fittings import Fits

from float_analysis import data_analist
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
                    Analyser.save_option()
                except KeyError:
                    print('Column not found, please try again')
            elif operation == '2':
                print('\nThese are the float columns', list(Analyser.clean.columns))
                col1 = input('\nWhat column do you want to use? :  ')
                col2 = input('\nWhat other column do you want to use? :  ')
                try:
                    Analyser.subtracting_col(col1, col2)
                    print('\nThe new column', Analyser.clean[col1 + '-' + col2])
                    Analyser.save_option()
                except KeyError:
                    print('Column not found, please try again')
            elif operation == '3':
                print('\nThese are the float columns', list(Analyser.clean.columns))
                col1 = input('\nWhat column do you want to use? :  ')
                col2 = input('\nWhat other column do you want to use? :  ')
                try:
                    Analyser.multiplication_col(col1, col2)
                    print('\nThe new column', Analyser.clean[col1 + '*' + col2])
                    Analyser.save_option()
                except KeyError:
                    print('Column not found, please try again')
            elif operation == '4':
                print('\nThese are the float columns', list(Analyser.clean.columns))
                col1 = input('\nWhat column do you want to use? :  ')
                col2 = input('\nWhat other column do you want to use? :  ')
                try:
                    Analyser.division_col(col1, col2)
                    print('\nThe new column', Analyser.clean[col1 + '/' + col2])
                    Analyser.save_option()
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
                while True:
                    print('\nThese are the float columns', list(Analyser.clean.columns))
                    col1 = input('\nWhat column do you want to use? :  ')
                    col2 = input('\nWhat other column do you want to use? :  ')
                    print('\n How would you like to plot?')
                    print('1: Just the scatter')
                    print('2: With a fit')
                    print('q: Back to main menu')
                    way = str(input('\nEnter your choice: '))
                    if way == 'q':
                        break
                    elif way == '1':
                        try:
                            Analyser.our_plot_scat(col1, col2)
                        except KeyError:
                            print('Column not found, please try again')
                    elif way == '2':
                        fit = Fits(Analyser.clean,col1,col2)
                        print(fit.x)
                        print(fit.y)
                        print(fit.x.isnull().sum())  # how many NaN in x
                        print(fit.y.isnull().sum())
                        while True:
                            print('\nWhat fit would you like to plot?')
                            print('1: Polynomial')
                            print('2: Exponential')
                            print('3: Trigonometrical')
                            print('4: FFT')
                            print('q: Back to main menu')
                            fitting = str(input('\nEnter your choice: '))
                            if fitting == 'q':
                                break
                            elif fitting == '1':

                                level = int(input('\nWhat degree polynomial do you want? :  '))
                                title = str(input('\nWhat title do you want for the plot?: '))
                                print('what scale would you like to use?')
                                print('1: Linear')
                                print('2: Loglog')
                                print('q: Back to main menu')
                                scale = str(input('\nEnter your choice: '))
                                if scale == 'q':
                                    break
                                elif scale == '1':
                                    try:
                                        fit.polynomial(level, title)
                                    except Exception as e:
                                        print(f'Fit failed: {e}')
                                elif scale == '2':
                                    try:
                                        fit.polyloglog(level, title)
                                    except Exception as e:
                                            print(f'Fit failed: {e}')
                                else:
                                    print('Invalid choice, please try again')
                            elif fitting == '2':
                                title = str(input('\nWhat title do you want for the plot?: '))
                                guess = input('\nDo you want to provide initial guesses? (y/n): ')
                                if guess == 'y':
                                    p0 = list(map(float, input('Enter 3 values separated by commas (a,b,c): ').split(',')))
                                else:
                                    p0 = None
                                print('What scale would you like to use?')
                                print('1: Linear')
                                print('2: Logy')
                                print('q: Back to main menu')
                                scale = str(input('\nEnter your choice: '))
                                if scale == 'q':
                                    break
                                elif scale == '1':
                                    try:
                                        fit.exponential(title,p0=p0)
                                    except Exception as e:
                                        print(f'Fit failed: {e}')
                                elif scale == '2':
                                    try:
                                        fit.exponentiallog(title,p0=p0)
                                    except Exception as e:
                                        print(f'Fit failed: {e}')
                                else:
                                    print('Invalid choice, please try again')
                            elif fitting == '3':
                                title = str(input('\nWhat title do you want for the plot?: '))
                                guess = input('\nDo you want to provide initial guesses? (y/n): ')
                                if guess == 'y':
                                    p0 = list(map(float, input('Enter 4 values separated by commas (a,b,c,d): ').split(',')))
                                else:
                                    p0 = None
                                try:
                                    fit.trigonometric(title,p0=p0)
                                except Exception as e:
                                    print(f'Fit failed: {e}')
                            elif fitting == '4':
                                title = str(input('\nWhat title do you want for the plot?: '))
                                try:
                                    fit.Fast_FT(title)
                                except Exception as e:
                                    print(f'Fit failed: {e}')
                            else:
                                print('Invalid choice, please try again')

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

print('Goodbye!')
##usage of the class

#Analyser = data_analist('/home/daniel/Documents/lab_3/T2_7.CSV')
