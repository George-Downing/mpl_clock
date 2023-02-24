import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
import datetime
import time

DEG = np.pi/180

class Gauge(object):
    def __init__(self, ax: matplotlib.axes.SubplotBase, N: int, N_Red: float, scl: list[float], l_scl: list[float], text: list[str]):
        ax.axis([-1, 1, -1, 1])
        ax.set_aspect(1)
        ax.set_facecolor("k")
        ax.set_xticks([])
        ax.set_yticks([])

        self.r_bak = -0.22
        self.r_frt = 0.88
        R = 0.93
        r_cyl = 0.06
        l_txt = 0.18
        w_ptr = 1.50
        w_arc = 1.50
        w_scl = 1.00
        s_txt = 9
        s_fnt = "Gill Sans"
        
        self.hand = ax.plot([], [], lw=w_ptr, c="r", zorder=90)[0]
        ax.add_artist(Arc([0, 0], 2 * R, 2 * R, 0, -45, 225, lw=w_arc, color="gray", zorder=50))
        ax.add_artist(Circle((0, 0), r_cyl, color="gray", zorder=80))

        theta_red = N_Red / N * 270
        for i in range(len(scl)):
            r = R - l_scl[i]
            Theta = np.arange(0, N + 0.5*scl[i], scl[i]) / N * 270
            for theta in Theta:
                X = R * np.cos((225 - theta) * DEG)
                x = r * np.cos((225 - theta) * DEG)
                Y = R * np.sin((225 - theta) * DEG)
                y = r * np.sin((225 - theta) * DEG)
                ax.plot([X, x], [Y, y], lw=w_scl, c="w" if theta < theta_red else "r", zorder=10)
        
        r = R - l_txt
        Theta = np.arange(0, N + 0.5*scl[0], scl[0]) / N * 270
        for theta, txt in zip(Theta, text):
            x = r * np.cos((225 - theta) * DEG)
            y = r * np.sin((225 - theta) * DEG)
            ax.text(x, y, txt, verticalalignment="center", horizontalalignment="center",
                    c="w", fontdict={"size": s_txt, "family": s_fnt}, zorder=10)

    def __call__(self, theta):
        x_bak = self.r_bak * np.cos((225 - theta) * DEG)
        y_bak = self.r_bak * np.sin((225 - theta) * DEG)
        x_frt = self.r_frt * np.cos((225 - theta) * DEG)
        y_frt = self.r_frt * np.sin((225 - theta) * DEG)
        self.hand.set_data([x_bak, x_frt], [y_bak, y_frt])
        plt.draw()

def button_press(event):
    ax = event.inaxes
    if ax is None:
        return
    x, y = event.xdata, event.ydata
    r = np.sqrt(x**2 + y**2)
    if r < 0.25:
        return
    print(event)
    x = x/r * (0.93 - 0.18)
    y = y/r * (0.93 - 0.18)
    if event.button == 1:
        ax.scatter(x, y, s=40, c="C0")
    elif event.button == 3:
        ax.scatter(x, y, s=40, c="C1")
    else:
        ax.scatter(x, y, s=40, c="C2")
    

if __name__ == "__main__":
    plate = plt.figure(0, [6, 2], 96)
    plate.set_facecolor("k")
    CONN = [plate.canvas.mpl_connect("button_press_event", button_press)]
    
    txt_maj = ["Feb", "10", "20", "Mar", "10", "20", "Apr", "10"]
    gauge_toefl = Gauge(plate.add_axes([0/3, 0, 1/3, 1]), 70, 64, [10, 5, 1], [0.07, 0.05, 0.03], txt_maj)
    
    txt_maj = ["Thu", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"]
    gauge_week = Gauge(plate.add_axes([1/3, 0, 1/3, 1]), 7*3*6, 19*6, [3*6, 6, 1], [0.07, 0.05, 0.03], txt_maj)

    txt_maj = [str(i) for i in range(6, 1 + 24, 3)]
    gauge_today = Gauge(plate.add_axes([2/3, 0, 1/3, 1]), 18 * 60, 16 * 60, [3*60, 60, 10], [0.07, 0.05, 0.03], txt_maj)


    plt.ion()
    plt.show()

    countdown = 6 * 3600
    dt = 300
    while countdown > 0:
        clock = datetime.datetime.now()
        d = (clock.month - 2) * 30 + (clock.day - 1)
        workhour = max(clock.hour - 6, 0)
        workday = (7 + clock.weekday() - 3) % 7

        theta = 270 * (d + workhour / 18) / 70
        gauge_toefl(theta)

        theta = 270 * (workday + workhour / 18 + clock.minute / 60 / 18) / 7
        gauge_week(theta)

        theta = 270 * (clock.hour - 6 + clock.minute / 60 + clock.second / 3600 + (dt / 2) / 3600) / 18
        gauge_today(theta)
        
        plt.pause(dt)
        countdown -= dt
