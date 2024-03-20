import pandas as pd
import data
import plots

def main():
    # Collect Lego sets data and save data to files.
    df = data.get_lego_info()

    # Create plots from gathered data and save them as 'lego_plots.png'.
    if not df.empty:
        plots.create_plots(df)

if __name__ == "__main__":
    main()