import os
import pandas as pd
import numpy as np
from pdf2image import convert_from_path

copy_to_clipboard = True

try:
    import pyperclip

except ModuleNotFoundError:
    copy_to_clipboard = False

def convert_to_latex_table(**kwargs):
    """Pass key word argument of filename, which is a path
    to a .csv file, or key word argument table, which is a 2D
    iterable. This function creates a LaTeX version of the
    data and copies it to your clipboard."""

    if 'filename' in kwargs:

        table = pd.read_csv(kwargs['filename'], header=None).iloc[:, :].values

    elif 'table' in kwargs:

        table = kwargs['table']

    else:

        print('ERROR: Please supply a keyword argument of filename or table')
        exit()

    nan_indices = pd.isnull(table)
    table[nan_indices] = ''

    latex_tabular = '\\begin{tabular}{' + 'c'*len(table[0])+'}\n'

    for row in table:

        latex_tabular += '\t'

        for index, element in enumerate(row):

            latex_tabular += str(element)

            if index == len(row)-1:
                latex_tabular += ' \\\\\n'

            else:
                latex_tabular += " & "

    latex_tabular += '\\end{tabular}'

    print('The following as been added to your clipboard.')
    print(latex_tabular)

    if copy_to_clipboard:
        pyperclip.copy(latex_tabular)  # copy to clipboard

    return table


def convert_pdf_to_latex(filename):
    """Get bounding box of image in pdf.
    Print the includegraphics command with
    bb command."""

    image = np.array(convert_from_path(filename)[0])
    image = np.mean(image, axis=2)  # convert to grayscale

    non_white_pixels = np.where(image!=255)

    xmin = np.min(non_white_pixels[1])
    xmax = np.max(non_white_pixels[1])
    ymin = np.min(non_white_pixels[0])
    ymax = np.max(non_white_pixels[0])

    xfactor = 8.5/image.shape[1]
    yfactor = 11./image.shape[0]

    bb = str(xfactor*xmin)+'in ' + str(yfactor*ymin)+'in ' +\
         str(xfactor*xmax)+'in ' + str(yfactor*ymax)+'in'

    latex = '\\includegraphics[bb='+bb+',scale=1]{'+filename+'}'

    print(latex)

    if copy_to_clipboard:
        pyperclip.copy(latex)  # copy to clipboard


if __name__ == "__main__":

    path = input('Enter path to file: ')

    if '.csv' in path:
        convert_to_latex_table(filename=path)

    elif '.pdf' in path:
        convert_pdf_to_latex(filename=path)

    else:
        print('ERROR: unknown file type.')
