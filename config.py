import matplotlib as mpl
import numpy as np

mpl.style.use(["/home/hugo/Thèse/common/styles.mplstyle", "acta-acustica.mplstyle"])

mm = 1 / (2.54 * 10)

colors = {
    1: "black",
    2: "darkgrey",
    "klimke": "C0",
    "levaggi": "C1",
    "stoppani": "C2",
}


def ci(a):
    m = np.mean(a)
    s = 1.96 * np.std(a) / np.sqrt(len(a))
    return m - s, m + s


VIOLIN_MAP = {
    "Klimke": "Klimke (Test)",
    "Levaggi": "Levaggi (Control)",
    "Stoppani": "Stoppani (Control)",
}
