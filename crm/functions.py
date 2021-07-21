import random

import numpy as np

def generarcolores(cant):
    colores_css=[]
    colores_template=[]
    for i in range(500):
        color = list(np.random.choice(range(256), size=3))
        colores_css.append(color)
    colores=random.sample(list(colores_css) , cant)
    
    for c in colores:
        color='rgba({}, {}, {})'.format(c[0],c[1],c[2])
        colores_template.append(color)

    return colores_template