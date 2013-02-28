#!/usr/bin/python
from PIL import Image, ImageTk
import math
import sys
import filtros
import random
import ImageFont, ImageDraw
import Image
from math import pi, atan, atan2, floor, fabs, sqrt, sin, cos, ceil, degrees

def frecuentes(histo, cantidad):
    frec = list()
    for valor in histo:
        if valor is None:
            continue
        frecuencia = histo[valor]
        acepta = False
        if len(frec) <= cantidad:
            acepta = True
        if not acepta:
            for (v, f) in frec:
                if frecuencia > f:
                    acepta = True
                    break
        if acepta:
            frec.append((valor, frecuencia))
            frec = sorted(frec, key = lambda tupla: tupla[1])
            if len(frec) > cantidad:
                frec.pop(0)
    incluidos = list()
    for (valor, frecuencia) in frec:
        incluidos.append(valor)
    return incluidos

def main():
    """funcion principal
    """
    umb = .75
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
    CERO = 0.0001
    imagenx = filtros.convolucion(imagen, sobelx)
    imageny = filtros.convolucion(imagen, sobely)
    #imagenx = filtros.normalizar(imagenx)
    #imageny = filtros.normalizar(imageny)
    imagenx = filtros.umbral(imagenx)
    imageny = filtros.umbral(imageny)
    imagenx.save("imagenx.png")
    imageny.save("imageny.png")
    lin_x = imagenx.load()
    lin_y = imageny.load()
    w, h = imagen.size
    res = []
    for j in xrange(h):
        datos = list()
        for i in xrange(w):
            x = lin_x[i,j][0]
            y = lin_y[i,j][0]
            if  fabs(x) + fabs(y) <= CERO:
                angulo = None
            else:
                angulo = atan2(y,x)
                print angulo
            if angulo is not None:
                p = int(i-w/2)*cos(angulo)+(h/2-j)*sin(angulo)
                angulo = int(degrees(angulo))
                print angulo
                datos.append(('%d' %angulo, '%.0f' %p))
                #print '%.2f' %angulo
            else:
                datos.append((None, None))
        res.append(datos)
    comb = dict()
    for y in xrange(h):
        for x in xrange(w):
            if x > 0 and y > 0 and x < w - 1 and y < h - 1: 
                (angulo, p) = res[y][x]
                if angulo is not None:
                    combinacion = (angulo, p)
                    if combinacion in comb:
                        comb[combinacion] += 1
                    else:
                        comb[combinacion] = 1
    frec = frecuentes(comb, int(ceil(len(comb) * 1)))
    #print frec

    for y in range(h):
        renglon = list()
        for x in range(w):
            (angulo, p) = res[y][x]
            if (angulo, p) in frec:
 #               if float(angulo) != 90 and float(angulo) != 0:
                    #print angulo
                if float(angulo) == 90 or float(angulo) == 270:
                    #print "90"
                    imagen.putpixel((x,y), (0,255,0))
                elif float(angulo) == 0 or float(angulo) == 180:
                    #print "0"
                    imagen.putpixel((x,y), (0,0,255))
                else:
                    imagen.putpixel((x,y), (255,0,0))
 
    imagen.save("res.png")
    return imagen

main()
