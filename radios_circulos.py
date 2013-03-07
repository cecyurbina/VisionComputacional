#!/usr/bin/python
from PIL import Image, ImageDraw
import random
import filtros
import time
from math import sqrt, fabs 
import sys
import math
CONT = 0

def dibuja_deteccion(imagen, radio, centros, DIA):
    """toma como parametros la imagen original, el radio
    y los centros que se detectaron y regresa una imagen con 
    los circulos que se encontraron dibujados
    """
    global CONT
    draw = ImageDraw.Draw(imagen)
    x_imagen, y_imagen = imagen.size
    for i in range(len(centros)):
        amarillo = (255, random.randint(120,255), random.randint(0, 40))
        x = centros[i][0]
        y = centros[i][1]
        draw.ellipse((x-radio,y-radio, x+radio,y+radio),
                     fill=None, outline=amarillo)
        draw.ellipse((x-radio,y-radio, x+radio,y+radio),
                     fill=None, outline=amarillo)
        radio = radio + 1
        draw.ellipse((x-radio,y-radio, x+radio,y+radio),
                     fill=None, outline=amarillo)
        radio = radio - 1
        draw.ellipse((x-radio,y-radio, x+radio,y+radio),
                     fill=None, outline=amarillo)
        draw.ellipse((x-1,y-1, x+1,y+1),
                     fill=None, outline="green")
        draw.text((x+2,y+2), str(CONT), fill="white")
        dia = radio*2.0
        p = (dia/DIA)*100
        print "ID  %s porcentaje %s" %(CONT, p)
        CONT = CONT + 1
    return imagen

def dibuja_circulo(num, imagen):
    """num es el numero de circulos aleatorios que se van a 
    dibujar, y la imagen es el canvas en el que se dibuja, 
    regresa la imagen con los circulos dibujados
    """
    global CONT
    draw = ImageDraw.Draw(imagen)
    x_imagen, y_imagen = imagen.size
    ruido = num
    for i in range(ruido):
        radio = random.randint(10, 30)
        x = random.randint(radio, x_imagen-radio)
        y = random.randint(radio, y_imagen-radio)
        draw.ellipse((x-radio,y-radio, x+radio,y+radio),
                     fill="black")
        print "Ruido dibujado con centro en (%s, %s) y radio de %s" %(x,y, radio)
    return imagen

def crea_imagen(dim):
    """crea una imagen con cierta dim, en blanco
    """
    im = Image.new('RGB', (dim,dim), (255,255,255))
    return im

def obtiene_votos(pix_x, pix_y, dim, radio):
    """se analiza la imagen, asi cada pixel detectado como
    borde da lugar al circulo con el radio, las celdas que 
    pertenecen a ese circulo reciben un voto
    """
    votos = []
    for pos in xrange(dim):
        votos.append([0] * dim)
    for ym in xrange(dim):
        y = dim / 2- ym
        for xm in xrange(dim):
            x = xm - dim / 2
            gx = pix_x[ym, xm][0]
            gy = pix_y[ym, xm][0]
            g = sqrt(gx ** 2 + gy ** 2)
            if fabs(g) > 0:
                cosTheta = gx / g
                sinTheta = gy / g
                xc = int(round(x - radio * cosTheta))
                yc = int(round(y - radio * sinTheta))
                xcm = xc + dim / 2
                ycm = dim / 2 - yc
                if xcm >= 0 and xcm < dim and ycm >= 0 and ycm < dim:
                    votos[ycm][xcm] += 1                    
    for rango in xrange (1, int(round(dim * 0.1))):
        agregado = True
        while agregado:
            agregado = False
            for y in xrange(dim):
                for x in xrange(dim):
                    v = votos[y][x]
                    if v > 0:
                        for dx in xrange(-rango, rango):
                            for dy in xrange(-rango, rango):
                                if not (dx == 0 and dy == 0):
                                    if y + dy >= 0 and y + dy < dim and x + dx >= 0 and x + dx < dim:
                                        w = votos[y + dy][x + dx]
                                        if w > 0:
                                            if v - rango >= w:
                                                votos[y][x] = v + w
                                                votos[y + dy][x + dx] = 0
                                                agregado = True
    return votos


def detecta_centros(votos, dim):
    """se encarga de detectar los centros
    """
    maximo = 0
    suma = 0.0
    for x in xrange(dim):
        for y in xrange(dim):
            v = votos[y][x]
            suma += v
            if v > maximo:
                maximo = v
    promedio = suma / (dim * dim)
    umbral = (maximo + promedio) / 2.0
    centros = []
    for x in xrange(dim):
        for y in xrange(dim):
            v = votos[y][x]
            if v > umbral:
                #print 'Posible centro detectado en (%d, %d). ' % (y,x)
                centros.append((y,x))
    return centros

def main():
    """funcion principal
    """
    try:
        num = int(sys.argv[1])
    except:
        #print "recuerda escribe el radio y el numero de circulos"
        return
    dim = 200
    im = crea_imagen(dim)
    im = dibuja_circulo(num,im)
    im.save("a.png")
    mascara = [[0,1,0],[1,-4,1],[0,1,0]]
    lap = filtros.convolucion(im, mascara)
    lap = filtros.umbral(lap)
    lap = filtros.umbral(lap)
    lap.save("lap.png")
    pix = lap.load()
    bordes = []
    #diagonal
    dia = math.sqrt( math.pow((im.size[0]) , 2) +  math.pow((im.size[1]) , 2))
    for i in range(dim):
        for j in range(dim):
            if pix[j, i][0] == 255:
                bordes.append((j,i))
    im.save("original.png")
    path = "circulos.png"
    im.save(path)
    im = filtros.abrir_imagen(path)
    im = filtros.hacer_gris(im)
    sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    Gx = filtros.convolucion(im, sobelx)
    Gy = filtros.convolucion(im, sobely)
    Gx.save("imagenx.png")
    Gy.save("imageny.png")
    votos = list()
    pix_x = Gx.load()
    pix_y = Gy.load()
    combinaciones = []
    for i in range(5, 45, 1):
        votos = obtiene_votos(pix_x, pix_y, dim, i)
        centros = detecta_centros(votos, dim)
        centros.insert(0, i)
        combinaciones.append(centros)
    puntos = []
    cen = []
    #print combinaciones
    for j in range(len(combinaciones)):
        #print combinaciones[j]
        cont = 0
        radio = combinaciones[j][0]
        for i in range(len(combinaciones[j])):
            #print combinaciones[j][i]
            if i == 0:
                continue
            cont = 0
            angulos = []
            for m in range(50): 
                angulos.append(random.randint(10, 360))
            for a in range(len(angulos)):
                x1 = int(radio*math.cos(math.degrees(angulos[a])))+combinaciones[j][i][0]
                x2 = int(radio*math.sin(math.degrees(angulos[a])))+combinaciones[j][i][1]
                s = (x1, x2)
                s1 = (x1, x2+1)
                s2 = (x1+1, x2)
                s3 = (x1+1, x2+1)
                s4 = (x1-1, x2-1)
                s5 = (x1, x2-1)
                s6 = (x1-1, x2)
                if s in bordes or s2 in bordes or s1 in bordes or s3 in bordes or s4 in bordes or s5 in bordes or s6 in bordes:
                    cont = cont + 1
            if cont >= 35:
                print "CIRCULO CON CENTRO (%s, %s)" %(x1, x2)
                im = dibuja_deteccion(im, radio, [(combinaciones[j][i][0], combinaciones[j][i][1])], dia)
    im.save("final.png")

main()
