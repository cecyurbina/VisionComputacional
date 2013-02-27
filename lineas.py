#!/usr/bin/python
from PIL import Image, ImageTk
import math
import sys
import filtros
import random
import ImageFont, ImageDraw
import Image
from math import pi, atan, floor, fabs, sqrt, sin, cos, ceil

def normalize(d):
    h = len(d)
    w = len(d[0])
    minimo = min(min(d))
    maximo = max(max(d))
    div = maximo - minimo
    for y in xrange(h):
        for x in xrange(w):
            d[y][x] = (d[y][x] - minimo) / div
    return d

def euclidean(imagenx, imageny):
    pix_x = imagenx.load()
    pix_y = imageny.load()
    w, h = imagenx.size
    m = list()
    for y in xrange(h):
        c = list()
        for x in xrange(w):
            c.append(sqrt(pix_x[x,y][0]**2 + pix_y[x,y][0]**2))
        m.append(c)
    return m

def main():
    """funcion principal
    """
    umb = 1
    try:
        imagen_path = sys.argv[1]
        print imagen_path
        imagen = filtros.abrir_imagen(imagen_path)
        
    except:
        print "No seleccionaste una imagen"
        return
    imagen = filtros.hacer_gris(imagen)
    sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    CERO = 0.00001
    imagenx = filtros.convolucion(imagen, sobelx)
    imageny = filtros.convolucion(imagen, sobely)
    imagenx = filtros.normalizar(imagenx)
    imageny = filtros.normalizar(imageny)
    imagenx = filtros.umbral(imagenx)
    imageny = filtros.umbral(imageny)
    imagenx.save("imagenx.png")
    imageny.save("imageny.png")
    lin_x = imagenx.load()
    lin_y = imageny.load()
    lista = []
    dicc = {}
    cont_hor = 0
    cont_ver = 0
    frec = {}
    angulos = []
    w, h = imagen.size
    colores = []
    for i in range(360):
        r = int(random.random()*250)
        g = int(random.random()*250)
        b = int(random.random()*250)
        colores.append([i, (r,g,b)])
    print colores
    for i in range(w):
        temp = []
        for j in range(h):
            x = lin_x[i, j][0]
            y = lin_y[i, j][0]
            ang = 0.0
            if abs(x) + abs(y) <= 0.0:
                ang = None
            elif x == 0 and y == 255:
                ang = 90
            else:
                ang = math.degrees(abs(y/x))
            if ang != None:
                p = abs((i) * math.cos(ang) + (j) * math.sin(ang))
                if not ang in angulos:  
                    angulos.append(ang)
                if i > 0 and i < w-1 and j > 0 and j < h - 1:
                    if (p, ang) in dicc:
                        dicc[(p, ang)] += 1
                    else:
                        dicc[(p, ang)] = 1
                temp.append((p, ang))
            else:
                temp.append((None, None))
        lista.append(temp)
    dicc = sorted(dicc.items(), key=lambda x: x[1], reverse = True)
    lar = int(math.ceil(len(dicc) * umb))
    for i in range(lar):
        (p, ang) = dicc[i][0]
        frec[(p, ang)] = dicc[1]
    pixeles = imagen.load()
    for i in range(w):
        for j in range(h):
            if i > 0 and j > 0 and i < w and j < h:
                p, ang = lista[i][j]
                if (p, ang) in frec:
                    if ang == 0:
                        pixeles[i, j] = (255, 0, 0)
                        cont_hor += 1
                    elif ang == 90:
                        pixeles[i, j] = (0, 0, 255)
                        cont_ver += 1
    print "total de pixeles verticales %s" %cont_hor
    print "total de pixeles horizontales %s" %cont_ver
    imagen.save('lineas.png', 'png')
    return imagen

if __name__ == "__main__":
    main()


