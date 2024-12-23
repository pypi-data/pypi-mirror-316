from .env_plot import EnvPlot
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

class EnvPlot3D(EnvPlot):

    def __init__(
        self,grid_map=None,
        objects=[],
        x_range=[0, 10],
        y_range=[0, 10],
        z_range=[0, 10],
        saved_figure=dict(),
        saved_ani=dict(),
        dpi: int = 100,
        figure_pixels: list =[1920, 1080],
        **kwargs,
    ):
        super().__init__(grid_map, objects, x_range, y_range, saved_figure, saved_ani, dpi, figure_pixels, **kwargs)
        
        self.clear_components()
        self.ax.remove()

        self.ax = self.fig.add_subplot(projection='3d')
        self.z_range = z_range

        self.init_plot(grid_map, objects, **kwargs)
        self.ax.set_zlim(z_range)




