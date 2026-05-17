## different slope fittings
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class Fits:
    def __init__(self,data,x_col,y_col):
        self.x = data[x_col]
        self.y = data[y_col]
        self.x_col = x_col
        self.y_col = y_col
    def polynomial(self,deg,title):
        fit_coefficient = np.polyfit(self.x,self.y,deg)
        x_smooth = np.linspace(self.x.min(),self.x.max(),100)
        y_smooth = np.polyval(fit_coefficient,x_smooth)
        plt.scatter(self.x,self.y,color = 'red',label='Data')
        plt.plot(x_smooth, y_smooth, color='blue', label=f'Fit: {np.poly1d(np.round(fit_coefficient, 3))}')
        plt.xlabel(self.x_col)
        plt.ylabel(self.y_col)
        plt.title(title)
        plt.legend()
        plt.show()
        plt.close()

    def polyloglog(self, deg, title):
        if (self.x <= 0).any() or (self.y <= 0).any():
            print('Log-log plot requires all values to be positive')
            return

        fit_coefficient = np.polyfit(self.x, self.y, deg)
        x_smooth = np.linspace(self.x.min(), self.x.max(), 100)
        y_smooth = np.polyval(fit_coefficient, x_smooth)
        plt.scatter(self.x, self.y, color='red', label='Data')
        coeffs = np.round(fit_coefficient, 3)
        plt.plot(x_smooth, y_smooth, color='blue', label=f'Fit: {np.poly1d(coeffs)}')
        plt.xlabel(self.x_col)
        plt.ylabel(self.y_col)
        plt.loglog()
        plt.title(title)
        plt.legend()
        plt.show()
        plt.close()

    def exponential(self,title,p0 = None):
        if p0 is None:
            p0 = [1,1,1]
        def exponential_fit(x,a,b,c):
            return a * np.exp(-b * (x - c))
        fit_coefficient,_ = curve_fit(exponential_fit, self.x,self.y, p0=p0)
        y_fit = exponential_fit(self.x,*fit_coefficient)

        plt.scatter(self.x,self.y,color = 'red', label= 'Data')
        a, b, c = np.round(fit_coefficient, 3)
        plt.plot(self.x, y_fit, color='blue', label=f'Fit: {a}*exp(-{b}*(x-{c}))')
        plt.title(title)
        plt.xlabel(self.x_col)
        plt.ylabel(self.y_col)
        plt.legend()
        plt.show()
        plt.close()
    def exponentiallog(self,title,p0=None):
        if p0 is None:
            p0 = [1,1,1]
        def exponential_fit(x,a,b,c):
            return a * np.exp(-b * (x - c))
        if (self.y<=0).any():
            print('semilogy plot requires all y values to be positive')
            return
        fit_coefficient,_ = curve_fit(exponential_fit, self.x,self.y, p0=p0)
        y_fit = exponential_fit(self.x,*fit_coefficient)

        plt.scatter(self.x,self.y,color = 'red', label= 'Data')
        a, b, c = np.round(fit_coefficient, 3)
        plt.plot(self.x, y_fit, color='blue', label=f'Fit: {a}*exp(-{b}*(x-{c}))')
        plt.title(title)
        plt.xlabel(self.x_col)
        plt.ylabel(self.y_col)
        plt.semilogy()
        plt.legend()
        plt.show()
        plt.close()

    def trigonometric(self,title,p0=None):
        if p0 is None:
            p0 = [self.y.max(),1,0,self.y.mean()]
        def trigonometric_fit(x,a,b,c,d):
            return a*np.sin(b*x+c) + d
        fit_coefficient,_ = curve_fit(trigonometric_fit, self.x,self.y,p0 = p0)
        y_fit = trigonometric_fit(self.x,*fit_coefficient)

        plt.scatter(self.x,self.y,color = 'red',label = 'Data')
        a, b, c, d = np.round(fit_coefficient, 3)
        plt.plot(self.x, y_fit, color='blue', label=f'Fit: {a}*sin({b}*x+{c})+{d}')
        plt.title(title)
        plt.xlabel(self.x_col)
        plt.ylabel(self.y_col)
        plt.legend()
        plt.show()
        plt.close()

    def Fast_FT(self, title):
        ts = self.x.iloc[1] - self.x.iloc[0]
        fft_result = np.fft.fft(self.y)
        fft_freq = np.fft.fftfreq(len(self.y), ts)

        positive_mask = fft_freq > 0
        frequencies = fft_freq[positive_mask]
        magnitude = np.abs(fft_result[positive_mask])

        plt.plot(frequencies, magnitude)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.title(title)
        plt.show()
        plt.close()






