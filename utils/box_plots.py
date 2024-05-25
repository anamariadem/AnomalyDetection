import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


def generate_box_plot(raw_data, columns, x_label, y_label, file_name=''):
    data = pd.DataFrame(raw_data, columns=columns)
    print(data)
    # define the order in which the categories will be plotted on the x-axis
    order = np.sort(data[columns[0]].unique())  # you could also create a list by hand if you want a specific order

    sns.set_style("ticks")

    ax = sns.stripplot(x=columns[0], y=columns[1], order=order, jitter=True, size=6, zorder=0, alpha=0.5, linewidth=1,
                       data=data)
    ax = sns.boxplot(x=columns[0],
                     y=columns[1],
                     order=order,
                     showfliers=True,
                     linewidth=0.8,
                     showmeans=True,
                     data=data,
                     dodge=False,
                     hue='window_size'
                     )

    ax = sns.pointplot(x=columns[0], y=columns[1], order=order, data=data, errorbar=None, color='black')
    means = data.groupby(columns[0])[columns[1]].mean().reindex(order)  # calculate the means and ensure they are
    # displayed in the same order as the boxplots
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    if len(file_name) > 0:
        plt.savefig(file_name)
    plt.show()


raw_data_hst_memory = {
    'window_size': [100, 500, 1000, 100, 500, 1000, 100, 500, 1000],
    'memory': [66.97009582863535,
               65.7746714997738,
               68.88573275165682,
               72.77534169367445,
               73.72143390589946,
               73.83068108457103,
               73.579154334038,
               74.00670749925159,
               74.12147585984039, ]
}

raw_data_hst_cpu = {
    'window_size': [100, 500, 1000, 100, 500, 1000, 100, 500, 1000],
    'memory': [27.457179055541854
        , 26.214940506532248
        , 28.70321762274802
        , 27.416849769268705
        , 23.118506843960045
        , 21.716958742283328
        , 21.99808472625969
        , 21.540311432112713
        , 23.048324942223076]
}

raw_data_gaussian_memory = {
    'window_size': [100, 500, 1000, 100, 500, 1000, 100, 500, 1000],
    'memory': [68.44933032567226,
               68.48451314217273,
               70.12897030341964,
               73.80551014656331,
               73.8728020334909,
               73.9385361124581,
               74.16811389907001,
               73.32415596056016,
               73.8432192444296, ]
}

raw_data_gaussian_cpu = {
    'window_size': [100, 500, 1000, 100, 500, 1000, 100, 500, 1000],
    'memory': [23.73549750303997
        , 21.60378805910245
        , 30.82000200482166
        , 22.21139935791291
        , 22.43813181607917
        , 22.368530135371223
        , 23.276674170073303
        , 26.574483095869436
        , 26.95673232160155]
}

generate_box_plot(raw_data_hst_memory,
                    ['window_size', 'memory'],
                    'Window size',
                    'Memory usage (%) - HST',
                    '../box_plots/hst_memory.png')

generate_box_plot(raw_data_hst_cpu,
                    ['window_size', 'memory'],
                    'Window size',
                    'CPU usage (%) - HST',
                    '../box_plots/hst_cpu.png')

generate_box_plot(raw_data_gaussian_memory,
                    ['window_size', 'memory'],
                    'Window size',
                    'Memory usage (%) - Gaussian Detector',
                    '../box_plots/gaussian_memory.png')

generate_box_plot(raw_data_gaussian_cpu,
                    ['window_size', 'memory'],
                    'Window size',
                    'CPU usage (%) - Gaussian Detector',
                    '../box_plots/gaussian_cpu.png')


# generate_box_plot(raw_data_gaussian_roc_auc_heart_rate,
#                   ['window_size', 'roc_auc'],
#                   'Window size',
#                   'ROC AUC Score - Gaussian Detector - Heart Rate',
#                   '../box_plots/gaussian_roc_auc_heart_rate.png')
#
# generate_box_plot(raw_data_gaussian_precision_heart_rate,
#                   ['window_size', 'precision'],
#                   'Window size',
#                   'Precision - Gaussian Detector - Heart Rate',
#                   '../box_plots/gaussian_precision_heart_rate.png')
#
# generate_box_plot(raw_data_gaussian_recall_heart_rate,
#                   ['window_size', 'recall'],
#                   'Window size',
#                   'Recall - Gaussian Detector - Heart Rate',
#                   '../box_plots/gaussian_recall_heart_rate.png')
