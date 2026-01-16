import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# --- Custom styles ---
mpl.style.use(["/home/hugo/Thèse/common/styles.mplstyle", "acta-acustica.mplstyle"])

# --- Width and Height ---
mm = 1 / (2.54 * 10)
WIDTH = 190 * mm
RATIO = 4 / 3
HEIGHT = WIDTH / RATIO
plt.rcParams["figure.figsize"] = (WIDTH, HEIGHT)


# --- Confidence interval function to use instead of seaborn's ---
def ci(a):
    m = np.mean(a)
    s = 1.96 * np.std(a) / np.sqrt(len(a))
    return m - s, m + s


def linear_mean(a):
    lin = 10 ** (a / 20)
    m = np.sqrt(np.mean(lin**2))
    m_db = 20 * np.log10(m)
    return m_db


colors = {
    1: "black",
    2: "darkgrey",
    "klimke": "C0",
    "levaggi": "C1",
    "stoppani": "C2",
    "own": "C1",
}

VIOLIN_MAP = {
    "klimke": "Klimke (Test)",
    "levaggi": "Levaggi (Control)",
    "stoppani": "Stoppani (Control)",
    "own": "Test player's violin",
}

PHASES_MAP = ["Phase 1", "Phase 2"]

SCOPES_MAP = {"test": "Test violinist", "control": "Control group"}

CRITERION_MAP = {
    "P": "Power",
    "F": "Ease of Playing",
    "T": "Tone",
}
