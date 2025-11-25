# 1. Define your targets
PDF = article.pdf
TYP_SRC = article.typ
PLOT_SCRIPT = scripts/generate_plots.py
PLOT_IMG = figures/acoustics_plot.svg

# 2. The default command (runs when you type 'make')
all: $(PDF)

# 3. Rule to build the PDF (Depends on the Typst file AND the plot image)
$(PDF): $(TYP_SRC) $(PLOT_IMG)
	typst compile $(TYP_SRC)

# 4. Rule to build the Plot (Depends on the Python script)
$(PLOT_IMG): $(PLOT_SCRIPT)
	python $(PLOT_SCRIPT)

# 5. Clean up command
clean:
	rm $(PDF) $(PLOT_IMG)