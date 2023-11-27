from matplotlib import pyplot as plt


if __name__ == '__main__':
    ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

    dev_y = [38496, 42000, 46752, 49320, 53200,
             56000, 62316, 64928, 67317, 68748, 73752]

    py_dev_y = [45372, 48876, 53850, 57287, 63016,
                65998, 70003, 70000, 71496, 75370, 83640]

    # this is the style for the graph, there is also 'ggplot' is good, not that it is not necessary to set
    # the colors and fonts in the plot and it will be nice too
    plt.style.use("fivethirtyeight")

    plt.plot(ages_x, dev_y, color="k", linestyle='--', marker=".", label="all devs")
    plt.plot(ages_x, py_dev_y, color="b", marker="o", linewidth=3, label="py devs")
    plt.xlabel("Ages")
    plt.ylabel("Median Salary (USD)")
    plt.title("A Salary for developers among ages")
    # This is to define what each signal is for, using the labels that we have defined for each plot
    plt.legend()
    # if you want to make a grid view in the graph
    # plt.grid(True)

    plt.show()


