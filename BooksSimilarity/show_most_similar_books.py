import matplotlib.pyplot as plt


def show_similaryty_chart(df, title):
    values = df[title]
    values_sorted = values.sort_values()
    similarity_chart = values_sorted.plot(kind='barh')
    similarity_chart.set_title('Similarity Score')
    similarity_chart.set_xlabel('Similarities')
    similarity_chart.set_ylabel('Titles')
    plt.savefig(title + '_similarities.pdf')
