from quarto import render
import os

# Define the path to the Quarto file
quarto_file = "README.qmd"
render(quarto_file, output_format="md")

# run quartodoc build in terminal
os.system("quartodoc build")
# preview the docs
os.system("quarto preview")

