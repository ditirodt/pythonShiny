from shiny import App, render, ui, reactive
import pandas as pd
from plotnine import ggplot, aes, geom_density, theme_light, geom_point, stat_smooth, facet_wrap

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(ui.input_slider(
            id="mass",
            label= "Max Body Mass",
            min=2000,
            max=8000,
            value=6000
        ),
        ui.input_action_button("reset", "Reset Filter")),
        ui.panel_main(ui.output_table("summary"), ui.output_plot("histogram"))
    )
)


def server(input, output, session):
    penguins = pd.read_csv("penguins.csv")

    @reactive.Calc
    def filtered_data():
        df = penguins.copy()
        df = df.loc[df["body_mass_g"] < input.mass()]
        return df

    @reactive.Effect
    @reactive.event(input.reset)
    def _():
        print("Pushed!!!!!")
        ui.update_slider("mass", values=6000)


    @output
    @render.table
    def summary():
        filt_df = filtered_data()
        filt_df = filt_df.groupby("species", as_index=False).size()
        return filt_df

    @output
    @render.plot
    def histogram():
        plot_df = filtered_data()
        
        plot = (
            ggplot(plot_df, aes(x="body_mass_g", fill="species"))
            + geom_density(alpha=0.2)
            + theme_light()
        ) 

        return plot


app = App(app_ui, server)
