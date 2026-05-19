import streamlit as st
from float_analysis import data_analist
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
from fittings import Fits
from ML_Analysis import ML

st.title('CSV Analysis Tool')

uploaded_file = st.file_uploader('Upload your CSV file', type='csv')

if uploaded_file:
    file_contents = uploaded_file.read()
    Analyser = data_analist(io.BytesIO(file_contents))
    st.session_state['file_contents'] = file_contents
    st.write('### Data preview')
    st.dataframe(Analyser.clean)
    st.write(f' **Columns:** {list(Analyser.clean.columns)}')

    # sidebar menu
    with st.sidebar:
        st.title('Analysis Menu')
        category = st.radio('Choose category',
                            ['Statistics', 'Column Operations', 'Plotting', 'Machine Learning'])
    if category == 'Statistics':
        st.write('### Statistics')

        stat_choice = st.selectbox('Choose statistic',
                                   ['Describe', 'Amplitude', 'Peek to peek', 'Covariance', 'RMS'])

        if stat_choice == 'Describe':
            col = st.selectbox('Choose column', list(Analyser.clean.columns))
            stat = st.selectbox('Choose stat', ['mean', 'std', 'min', 'max', 'count', '25%', '50%', '75%'])
            if st.button('Calculate'):
                st.write(Analyser.our_data_describe(col, stat))

        elif stat_choice == 'Amplitude':
            col = st.selectbox('Choose column', list(Analyser.clean.columns))
            if st.button('Calculate'):
                st.write(Analyser.our_data_amplitude(col))

        elif stat_choice == 'Peek to peek':
            col = st.selectbox('Choose column', list(Analyser.clean.columns))
            if st.button('Calculate'):
                st.write(Analyser.our_data_peek_to_peek(col))

        elif stat_choice == 'Covariance':
            col1 = st.selectbox('Choose first column', list(Analyser.clean.columns))
            col2 = st.selectbox('Choose second column', list(Analyser.clean.columns))
            if st.button('Calculate'):
                st.write(Analyser.our_data_covariance(col1, col2))

        elif stat_choice == 'RMS':
            col = st.selectbox('Choose column', list(Analyser.clean.columns))
            if st.button('Calculate'):
                st.write(Analyser.our_data_RMS(col))
    elif category == 'Column Operations':
        st.write('### Column Operations')

        operation = st.selectbox('Choose operation',['Addition', 'Subtraction', 'Multiplication', 'Division'])

        col1 = st.selectbox('Choose first column', list(Analyser.clean.columns), key='op_col1')
        col2 = st.selectbox('Choose second column', list(Analyser.clean.columns), key='op_col2')

        if st.button('Calculate'):
            if operation == 'Addition':
                Analyser.adding_col(col1, col2)
                st.write(Analyser.clean[col1 + '+' + col2])
            elif operation == 'Subtraction':
                Analyser.subtracting_col(col1, col2)
                st.write(Analyser.clean[col1 + '-' + col2])
            elif operation == 'Multiplication':
                Analyser.multiplication_col(col1, col2)
                st.write(Analyser.clean[col1 + '*' + col2])
            elif operation == 'Division':
                Analyser.division_col(col1, col2)
                st.write(Analyser.clean[col1 + '/' + col2])
            st.session_state['col_op_done'] = True

        if st.session_state.get('col_op_done'):
            import io

            csv_buffer = io.StringIO()
            Analyser.clean.to_csv(csv_buffer, index=False)
            st.download_button(label='Download updated CSV',data=csv_buffer.getvalue(),file_name='updated_data.csv',mime='text/csv')
            st.session_state['col_op_done'] = False
            save_path = st.text_input('Enter save path')
            if st.button('Save', key='save_col'):
                Analyser.clean.to_csv(save_path, index=False)
                st.success(f'Saved successfully!')
                st.session_state['col_op_done'] = False
    elif category == 'Plotting':
        st.write('### Plotting')

        plot_type = st.selectbox('Choose plot type', ['Histogram', 'Scatter', 'Boxplot'])

        if plot_type == 'Histogram':
            col = st.selectbox('Choose column', list(Analyser.clean.columns), key='hist_col')
            bins = st.slider('Number of bins', min_value=5, max_value=100, value=50)
            if st.button('Plot'):
                fig, ax = plt.subplots()
                sns.histplot(Analyser.clean[col], bins=bins, ax=ax)
                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                st.download_button(label='Download plot',data=buf,file_name='plot.png',mime='image/png')
        elif plot_type == 'Scatter':
            col1 = st.selectbox('Choose x column', list(Analyser.clean.columns), key='scat_col1')
            col2 = st.selectbox('Choose y column', list(Analyser.clean.columns), key='scat_col2')
            point_size = st.slider('Point size', min_value=1, max_value=100, value=20)

                # error bars
            error_bars = st.checkbox('Add error bars')
            x_err = None
            y_err = None
            if error_bars:
                x_err = st.selectbox('X error column (optional)',
                                     ['None'] + list(Analyser.clean.columns), key='x_err')
                y_err = st.selectbox('Y error column (optional)',
                                     ['None'] + list(Analyser.clean.columns), key='y_err')
                x_err = None if x_err == 'None' else x_err
                y_err = None if y_err == 'None' else y_err
                # fit options
            add_fit = st.checkbox('Add fit')
            fit_type = None
            degree = None
            p0 = None
            p0_input = None
            if add_fit:
                fit_type = st.selectbox('Choose fit',
                                        ['Polynomial', 'Exponential', 'Exponential log',
                                         'Trigonometric', 'FFT'])
                if fit_type == 'Polynomial':
                    degree = st.number_input('Degree', min_value=1, max_value=10, value=1)
                p0_input = st.checkbox('Provide initial guesses')
                if p0_input:
                    if fit_type in ['Exponential', 'Exponential log']:
                        p0_str = st.text_input('Enter 3 values (a,b,c)')
                        if p0_str:
                            p0 = list(map(float, p0_str.split(',')))
                    elif fit_type == 'Trigonometric':
                        p0_str = st.text_input('Enter 4 values (a,b,c,d)')
                        if p0_str:
                            p0 = list(map(float, p0_str.split(',')))

            title = st.text_input('Plot title', value=f'{col2} vs {col1}')

            if st.button('Plot', key='scat_plot'):
                fig, ax = plt.subplots()

                if not add_fit:
                    if not error_bars:
                        sns.scatterplot(data=Analyser.clean, x=col1, y=col2, s=point_size, ax=ax)
                    else:
                        ax.errorbar(Analyser.clean[col1], Analyser.clean[col2],
                                        xerr=Analyser.clean[x_err] if x_err else None,
                                        yerr=Analyser.clean[y_err] if y_err else None,
                                        fmt='o', markersize=point_size / 10, color='red')
                else:
                    fit = Fits(Analyser.clean, col1, col2, x_err=x_err, y_err=y_err)
                    if fit_type == 'Polynomial':
                        fit.polynomial(degree, title)
                    elif fit_type == 'Exponential':
                        fit.exponential(title, p0=p0)
                    elif fit_type == 'Exponential log':
                        fit.exponentiallog(title, p0=p0)
                    elif fit_type == 'Trigonometric':
                        fit.trigonometric(title, p0=p0)
                    elif fit_type == 'FFT':
                        fit.Fast_FT(title)
                    fig = plt.gcf()

                ax.set_title(title)
                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                st.download_button(label='Download plot', data=buf,
                                   file_name='scatter.png', mime='image/png')
    elif category == 'Machine Learning':
        st.write('### Machine Learning')


        ml = ML(Analyser.clean)

        ml_choice = st.selectbox('Choose ML method',
                                         ['Polynomial Regression', 'Anomaly Detection'])

        if ml_choice == 'Polynomial Regression':
            x_col = st.selectbox('Choose x column', list(Analyser.clean.columns), key='ml_x')
            y_col = st.selectbox('Choose y column', list(Analyser.clean.columns), key='ml_y')
            degree = st.number_input('Degree (1 = linear)', min_value=1, max_value=10, value=1)

            if st.button('Run'):
                results = ml.linear_regression([x_col], y_col, degree)
                st.write(f'**Coefficients:** {results["coefficients"]}')
                st.write(f'**Intercept:** {results["intercept"]:.2f}')
                st.write(f'**Train R²:** {results["train_r2"]:.2f}')
                st.write(f'**Test R²:** {results["test_r2"]:.2f}')
                st.pyplot(results['fig'])

        elif ml_choice == 'Anomaly Detection':
            x_col = st.selectbox('Choose x column', list(Analyser.clean.columns), key='anom_x')
            y_col = st.selectbox('Choose y column', list(Analyser.clean.columns), key='anom_y')
            contamination = st.slider('Expected % of anomalies',
                                              min_value=0.01, max_value=0.5, value=0.1)

            if st.button('Run'):
                results = ml.Anomalie([x_col], y_col, contamination=contamination)
                st.write(f'**Normal points:** {results["normal_count"]}')
                st.write(f'**Anomalies found:** {results["anomaly_count"]}')
                st.pyplot(results['fig'])