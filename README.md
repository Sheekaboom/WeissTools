# WeissTools 

A set of Tools for a variety of things and languages to make my life easier (and more automated). This currently most useful for generating nicely formatted plots for publishing, along with getting automatically typeset data for latex. Further Documentation can be found by building :code:`/docs` with sphinx.

## Python Tools

The following set of tools are for usage in Python for a variety of purposes.

### PlotTools.py

This file contains tools used for plotting. This currently only supports plotly plots. This includes the following methods:

#### format_plot

This method will take a plotly plot and add consistent and more readable formatting to it. This will do things such as increase font size, change linestyle, and change marker shapes.

#### save_plot

This method will take a plotly figure handle, format it (if not specified), and then save it out to a variety of filetypes. This is extremely useful when multiple filetypes are or may be desired and prevents the user from needing to go back and resave the plot as a new file type.

## Matlab Tools

The following are MATLAB functions to assist with a variety of applications.

### Plotting Tools

The following tools are used for help with plotting and formatting of plots

#### format_plot

Like its python counterpart, this function takes a figure handle and formats it for readability and publishability.

#### save_plot

Again, like its python counterpart, this function will format the plot and save it out to a variety of file types

#### set_unique_color_linestyle

This is used by format_plot to select both a unique color and linestyle/marker pair for publishing plots that could be in color or BW.

### Typesetting Tools

These are tools used to take data in MATLAB and create typeset information out of it. This will typically be to convert MATLAB data to latex formats.

#### matrix2latex

this is a function to nicely and more easily take a matlab matrix and quickly get latex code for that matrix. While this is possible in MATLAB, this provides more flexibility and is more straightforward to use.

