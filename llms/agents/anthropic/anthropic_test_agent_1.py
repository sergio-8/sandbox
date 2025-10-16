# Standard library imports
import re
import json

# Local helper module
import utils_1
# Use this utils.py function to load the data into a dataframe
df = utils_1.load_and_prepare_data('coffee_sales.csv')

# Grab a random sample to display
utils_1.print_html(df.sample(n=5), title="Random Sample of Coffee Sales Data")

