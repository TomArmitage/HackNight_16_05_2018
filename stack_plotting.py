import math
import matplotlib.pyplot as plt
import numpy as np


colors = ['#109EDB', '#8C6AAA', '#DB5143', '#E48523', '#0BADB2', '#EBB320', '#DB4988', '#7CB82F']


def stack_plot(data, colors=colors, str_width=1.2,
               num_width=0.3, offset=0.1, str_height=2):
    """
    Draw stack bar chart
    :param data: row list with title
    :param colors: list of colors for each stack
    :param str_width: bar width for str values
    :param num_width: bar width for num values
    :param offset: offset between two bars
    :param str_height: height for string value
    :return:
    """

    bar_count = len(data[0])
    row_count = len(data) - 1
    title = data[0]
    values = data[1:]

    # get index of string columns
    str_index = []
    for i in range(bar_count):
        if type(data[1][i]) == str:
            str_index.append(i)

    # replace string values with height value
    values_proc = []
    for i in range(len(values)):
        processed = [str_height if j in str_index else values[i][j] 
                     for j in range(bar_count)]
        values_proc.append(processed)

    # width and center of the bars
    width = [str_width if j in str_index else num_width for j in range(bar_count)]
    ind = [0]
    for i in range(bar_count - 1):
        ind.append(round(ind[i] + width[i] / 2 + offset + width[i + 1] / 2, 2))

    # Draw stack bar for the records
    top_array = np.array([0. for i in range(bar_count)])
    len_color = len(colors)
    total_raw_array = []

    for i in range(row_count):
        top_array += np.array(values_proc[i])
        total_raw_array.append(np.array(top_array))

    last_row = total_raw_array[-1]
    max_val = max(last_row)
    bottom_array = np.array([0. for i in range(bar_count)])
    scale_list = [round(max_val / last_row[i], 2) for i in range(bar_count)]
    total_array = []
    top_array = np.array([0. for i in range(bar_count)])
    scaled_values = [[round(values_proc[i][j] * scale_list[j], 2) 
                        for j in range(bar_count)] for i in range(row_count)]
    for i in range(row_count):
        if i:
            bottom_array = [bottom_array[j] + scaled_values[i - 1][j] for j in range(bar_count)]
        top_array += np.array(scaled_values[i])
        total_array.append(np.array(top_array))
        _plt = plt.bar(ind, scaled_values[i], width, bottom=np.array(bottom_array), 
                       color=colors[i % len_color])
    # additional markers
    # plt.ylabel('Scores')
    # plt.title('Scores by group and gender')
    # plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    # plt.yticks(np.arange(0, 81, 10))
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    # Draw border line between rows (optional)
    total_plot_array = []
    for i in range(row_count):
        tmp = []
        for j in range(bar_count):
            tmp.append(total_array[i][j])
            if j < bar_count - 1:
                tmp.append(total_array[i][j])
        total_plot_array.append(tmp)

    node_list = []
    for i in range(bar_count):
        node_list.append(round(ind[i] - width[i] / 2, 2))
        if i == bar_count - 1:
            continue
        node_list.append(round(ind[i] + width[i] / 2, 2))

    plt.plot(node_list, np.array(total_plot_array).T, color='#FFFFFF', linestyle='-',
             marker='', linewidth=1.0)

    # fill colors between border lines
    first = np.array([0. for i in range(len(total_plot_array[0]))])
    second = np.array(total_plot_array[0])
    for i in range(row_count):
        plt.fill_between(node_list, first, second, facecolor=colors[i % len_color],
                         alpha=0.5, interpolate=True)
        first = np.array(total_plot_array[i])
        if i == row_count - 1:
            continue
        second = np.array(total_plot_array[i + 1])

    rects = _plt.patches
    sum_array = np.array([0. for i in range(bar_count)])
    sum_label = np.array([0. for i in range(bar_count)])
    for j in range(row_count):
        labels = [round(value, 2) for value in values_proc[j]]
        scaled_heights = [round(value, 2) for value in scaled_values[j]]
        i = 0
        for rect, label in zip(rects, labels):
            height = float(sum_array[i]) + scaled_heights[i] / 2

            if i in str_index:
                label = values[j][i]
            plt.text(rect.get_x() + rect.get_width() / 2, 
                     height, label, ha='center', va='center', color='#FFFFFF')

            if j == row_count - 1:
                plt.text(rect.get_x() + rect.get_width() / 2, 
                         height + scaled_heights[i] / 2, 
                         title[i], ha='center', va='bottom', color='#000000')
            i += 1
        sum_array += np.array(scaled_heights)
        sum_label += np.array(labels)
    sum_label = [str(round(sum_label[i], 2)) if i not in str_index else '' for i in range(bar_count)]
    plt.xticks(ind, sum_label)
    plt.show()
