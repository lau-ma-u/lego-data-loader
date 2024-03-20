import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def create_plots(legos_df):
    """Creates some plots based on the data in the DataFrame and saves them in the file 'lego_plots.png'. """

    plt.style.use("seaborn-v0_8")

    # Create the figure and axes
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2,
                                                 ncols=2,
                                                 figsize=(20, 20))
    # Plot the data
    ax1.bar(legos_df["set_num"],
                      legos_df["num_parts"])

    # Customize the plot
    ax1.set(title="Number of Parts per Set",
           xlabel="Set Number",
           ylabel="Parts")

    ax1.grid(axis='y', linestyle="--")
    ax1.set_xticks(ax1.get_xticks(), ax1.get_xticklabels(), rotation=20, ha='right', fontsize=8)


    # Plot the data
    ax2.bar(legos_df["set_num"],
            legos_df["num_mocs"])

    # Customize the plot
    ax2.set(title="Number of MOCs per Set",
            xlabel="Set Number",
            ylabel="MOCs")

    ax2.grid(axis='y', linestyle="--")
    ax2.set_xticks(ax2.get_xticks(), ax2.get_xticklabels(), rotation=20, ha='right', fontsize=8)

    # Set mean line
    ax2.axhline(legos_df["num_mocs"].mean(),
                linestyle='--', color="red")

    # Sort the dataframe for the next plot
    sorted_df = legos_df.sort_values("avg_moc_parts", ascending=False)

    # Plot the data
    ax3.bar(sorted_df["set_num"],
            sorted_df["avg_moc_parts"])

    # Customize the plot
    ax3.set(title="Average Number of parts in a MOC per Set",
            xlabel="Set Number",
            ylabel="Average MOC Parts")

    ax3.grid(axis='y', linestyle="--")
    ax3.set_xticks(ax3.get_xticks(), ax3.get_xticklabels(), rotation=20, ha='right', fontsize=8)

    # Plot the data
    ax4.scatter(x=legos_df["num_parts"],
                y=legos_df["avg_moc_parts"])

    # Customize the plot
    ax4.set(title="",
            xlabel="Number of Parts",
            ylabel="Average MOC Parts")

    ax4.grid(axis='y', linestyle="--")
    ax4.set_xticks(ax4.get_xticks(), ax4.get_xticklabels(), rotation=20, ha='right', fontsize=8)

    # Set trend line
    sns.regplot(x=legos_df["num_parts"], y=legos_df["avg_moc_parts"], ci=False, line_kws={'color': 'red'}, ax=ax4)

    # Save the figure as a file
    fig.savefig("lego_plots.png")

