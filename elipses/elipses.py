#!/usr/bin/python
from PIL import Image, ImageDraw
import random
import filtros
import time
from math import sqrt, fabs, atan2, pi, cos, sin, ceil, degrees
import sys
import numpy

def dibuja_elipse(num,imagen):
    """dibuja elipses aleatorios para la imagen inicial
    """
    draw = ImageDraw.Draw(imagen)
    x_imagen, y_imagen = imagen.size
    rangox = 20*2
    rangoy = 50*2    
    for i in range(num):
        ancho = random.randint(rangox, rangoy)
        largo = random.randint(rangox, rangoy)
        x = random.randint(ancho, x_imagen-(ancho))
        y = random.randint(largo, y_imagen-(largo))
        if random.choice('ab') == 'b':
            draw.ellipse((x,y, x+ancho,y+largo),fill="black")
        else:
            draw.ellipse((x,y, x+ancho,y+ancho),fill="black")
    return imagen

def bfs(imagen, origen, color):
    """colorea todo el objeto recibe como parametros el 
    nuevo color con el que se pinta,la coordenada de inicio y
    la imagen, y regresa un arreglo con la masa y la imagen
    """
    print type(origen)
    c = []
    cola = []
    cont = 0
    masa = []
    pixeles = imagen.load()
    alto, ancho = imagen.size
    cola.append(origen)
    original = pixeles[origen]
    edges = []
    while len(cola) > 0:
        (x, y) = cola.pop(0)
        actual = pixeles[x, y]
        if actual == original or actual == color:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    candidato = (x + dx, y + dy)
                    pix_x = candidato[0]
                    pix_y = candidato[1]
                    if pix_x >= 0 and pix_x < alto and pix_y >= 0 and pix_y < ancho:
                        contenido = pixeles[pix_x, pix_y]
                        if contenido == original:
                            pixeles[pix_x, pix_y] = color
                            masa.append((pix_x,pix_y))
                            imagen.putpixel((pix_x, pix_y), color)
                            cont += 1
                            cola.append((pix_x, pix_y))
                            c.append((pix_x, pix_y))
    imagen.save('prueba', 'png')
    return imagen, cont, masa, c

def bfs2(imagen, origen, color, col):
    """colorea todo el objeto recibe como parametros el 
    nuevo color con el que se pinta,la coordenada de inicio y
    la imagen, y regresa un arreglo con la masa y la imagen
    """
    area = 0
    c = []
    cola = []
    cont = 0
    masa = []
    pixeles = imagen.load()
    alto, ancho = imagen.size
    cola.append(origen)
    original = pixeles[origen]
    edges = []
    while len(cola) > 0:
        (x, y) = cola.pop(0)
        actual = pixeles[x, y]
        if actual == original or actual == color or actual == (255,255,255):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    candidato = (x + dx, y + dy)
                    pix_x = candidato[0]
                    pix_y = candidato[1]
                    if pix_x >= 0 and pix_x < alto and pix_y >= 0 and pix_y < ancho:
                        contenido = pixeles[pix_x, pix_y]
                        if contenido == original or contenido == (255,255,255): 
                            pixeles[pix_x, pix_y] = color
                            masa.append((pix_x,pix_y))
                            imagen.putpixel((pix_x, pix_y), color)
                            cont += 1
                            cola.append((pix_x, pix_y))
                            c.append((pix_x, pix_y))
                            area = area + 1
    imagen.save('prueba', 'png')
    return imagen, cont, masa, c, area
 
def encuentra_figuras(imagen):
    """encuentra cada objeto y guarda en una lista
    los bordes de cada objeto
    """
    alto, ancho = imagen.size
    pixeles = imagen.load()
    colores = []
    porcentaje = []
    elipses = []
    for i in range(alto):
        for j in range(ancho):
            if pixeles[i,j] == (255,255,255):
                r = int(random.random()*250)
                g = int(random.random()*250)
                b = int(random.random()*250)
                nuevo_color = (r,g,b)
                imagen, cont, masa, c = bfs(imagen, (i,j), nuevo_color)
                elipses.append(c)
                total_x = 0
                total_y = 0
                por = (float(cont)/float(alto*ancho))*100
                for l in range(len(masa)):
                    total_x = total_x + masa[l][0]
                    total_y = total_y + masa[l][1]
                x_centro = total_x/len(masa)
                y_centro = total_y/len(masa)
                colores.append([nuevo_color,(x_centro, y_centro), por])
                porcentaje.append(por)
                pixeles = imagen.load()
                masa = []
    figura_mayor = max(porcentaje)
    i = porcentaje.index(figura_mayor)
    color_mayor = colores[i][0]
    imagen.save('colores.png', 'png')
    return imagen, colores, elipses


def puntos(elipses, ptos):
    """puntos aleatorios del contorno de cada
    figura
    """
    puntos_linea = []
    for elipse in elipses:
        punto1 = random.choice(elipse)
        punto2 = random.choice(elipse)
        ptos.append(punto1)
        ptos.append(punto2)
        puntos_linea.append((punto1, punto2))
    return puntos_linea, ptos

def crea_imagen(ancho, largo):
    """crea una imagen con cierta dim, en blanco
    """
    im = Image.new('RGB', (ancho,largo), (255,255,255))
    return im

def gradiente_sobel(punto, pixeles):
    #print punto
    x = punto[0]
    y = punto[1]
    #print x, y
    z1 = pixeles[x-1, y-1][0] 
    z2 = pixeles[x, y-1][0]
    z3 = pixeles[x+1, y-1][0]
    z4 = pixeles[x-1, y][0]
    z5 = pixeles[x, y][0]
    z6 = pixeles[x+1, y][0]
    z7 = pixeles[x-1, y+1][0]
    z8 = pixeles[x, y+1][0]
    z9 = pixeles[x+1, y+1][0]
    Gx = ((z3)+(2*z6)+z9)-((z1)+(2*z4)+(z7))
    Gy = ((z7)+(2*z8)+z9)-((z1)+(2*z2)+(z3))
    G = sqrt((Gx**2)+(Gy**2))
    angulo = atan2(Gy, Gx)
    angulo = angulo -(pi/2)
    #print G, angulo
    return x,y, angulo 

def alarga_linea(pendiente,x0, y0, matriz, im, Px, Py):
    """alarga el punto hasta que se termina el objeto relleno
    """
    draw = ImageDraw.Draw(im)
    pixeles = im.load()
    cont = 1
    while True:
        if Px > x0:
            x = x0 - 1
        else:
            x = x0 + 1            
        y = (pendiente*(x - x0)) + y0
        x0 = x
        y0 = y
        y = int(y)
        #print "la y es %s" %y
        matriz[x,y] = matriz[x,y] + 1
        try:
            #draw.ellipse((x-4, y-4,x-1,y-1), fill="blue")
            #print pixeles[x, y][0], cont
            if pixeles[x, y][0] == 255:
                break
        except:
            pass
        cont = cont + 1
    return matriz, im

def dibuja_ec_elipse(temp, centro, maxi, mini):
    """dibuja el elipse deacuerdo al los puntos
    centro y maximos y minimos encontrados con su ecuacion
    """
    puntos = []
    draw = ImageDraw.Draw(temp)
    a = 0.0
    color = (random.randint(175,255), random.randint(114, 196), 0)
    while True:
        x = centro[0]+(mini*cos(a))
        y = centro[1]+(maxi*sin(a))
        puntos.append((x,y))
        draw.ellipse((x-1, y-1, x+1,y+1), fill=color)
        a = a + .01
        if a > 2*pi:
            break
    return temp, puntos, color

def encuentra_puntos(im, elipses, matriz, ptos):
    """Encuentra el punto medio de los dos punto aleatorios, asi como
    el punto de interseccion y la pendiente
    """
    puntos_linea, ptos = puntos(elipses, ptos)
    pixeles = im.load()
    lineas = []
    largo_linea = 60
    draw = ImageDraw.Draw(im)
    for punto_linea in puntos_linea:
        s = []
        k = []
        for punto in punto_linea:
            x,y,angulo = gradiente_sobel(punto, pixeles)
            x1 = x - largo_linea*cos(angulo)
            y1 = y - largo_linea*sin(angulo)
            x2 = x + largo_linea*cos(angulo)
            y2 = y + largo_linea*sin(angulo)
            linea = x1, y1, x2, y2
            draw.line((x1,y1, x2, y2),fill="red")
            draw.ellipse((x-3, y-3, x+3,y+3), fill="green")
            s.append([x1,y1,x2,y2,x,y])
        x1, x2, x3, x4 = s[0][0], s[0][2], s[1][0], s[1][2]
        y1, y2, y3, y4 = s[0][1], s[0][3], s[1][1], s[1][3]
        Px_num = (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)
        Px_den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        Py_num = (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)
        Py_den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        ym = (s[0][5]+s[1][5])/2
        xm = (s[0][4]+s[1][4])/2
        try:
            Px = Px_num/Px_den
            Py = Py_num/Py_den
            #print "La interseccion esta en %s, %s" %(Px, Py)
            draw.ellipse((Px-3, Py-3, Px+3,Py+3), fill="blue")
            draw.ellipse((xm-2, ym-2, xm+2,ym+2), fill="yellow")
            draw.line((xm,ym, Px, Py),fill="red")
            pendiente = (Py-ym)/(Px-xm)
            #print "Pendiente %s" %pendiente
            matriz, im = alarga_linea(pendiente,xm, ym, matriz, im, Px, Py)
        except Exception, e: 
            #print str(e)
            pass
    return matriz, im, ptos

def main():
    """funcion principal
    """
    num = 2
    largo = 500
    ancho = 700
    im = crea_imagen(ancho, largo)
    x, y = im.size
    area_total = largo*ancho
    diagonal = sqrt((x-0)**2 + (y-0)**2)
    im = dibuja_elipse(num,im)
    temp = im.copy()
    im.save("original.png")
    im = filtros.hacer_gris(im)
    mascara = [[0,1,0],[1,-4,1],[0,1,0]]
    lap = filtros.convolucion(im, mascara)
    lap.save("lap.png")
    c = 0
    cir = 0
    im1, colores, elipses =encuentra_figuras(lap)
    #matriz = [[0 for i in range(y)] for j in range(x)]
    for figura in elipses:
        matriz_1 = numpy.zeros(x*y).reshape((x,y))
        #print matriz_1
        tem = []
        dic = {}
        tem.append(figura)
        ptos = []
        for i in range(1000):
            matriz_1, im, ptos = encuentra_puntos(im, tem, matriz_1, ptos)
        i,j = numpy.unravel_index(matriz_1.argmax(), matriz_1.shape)
        draw = ImageDraw.Draw(temp)
        #draw.ellipse((i-5, j-5, i+5,j+5), fill="blue")
        for pto in ptos:
            x_0 = pto[0]
            y_0 = pto[1]
            distancia = sqrt((x_0-i)**2 + (y_0-j)**2)
            dic[pto] = distancia
        key1,value = max(dic.iteritems(), key=lambda x:x[1])
        #draw.ellipse((key1[0]-5, key1[1]-5, key1[0]+5,key1[1]+5), fill="red")
        deltay = j-key1[1] 
        deltax = i-key1[0]
        angulo1 = abs(degrees(atan2(deltay, deltax))-180)
        key2,value = min(dic.iteritems(), key=lambda x:x[1])
        #draw.ellipse((key2[0]-5, key2[1]-5, key2[0]+5,key2[1]+5), fill="red")
        deltay = j-key2[1] 
        deltax = i-key2[0]
        angulo2 = abs(degrees(atan2(deltay, deltax))-180)
        diagonal_elipse = sqrt((key1[0]-key2[0])**2 + (key1[1]-key2[1])**2)
        p = (diagonal_elipse*100)/diagonal
        print "*****************************************************"
        if dic[key1] != dic[key2]:
            c = c + 1
            print "Elipse #%s" %c
        else:
            print "Circulo #%s" %cir
            cir = cir + 1
        print "Centro en (%s, %s)" %(i, j)
        print "Radio maximo es de %s con angulo de %s" %(dic[key1], angulo1)
        print "Radio minimo es de %s con angulo de %s" %(dic[key2], angulo2)
        print "Porcentaje diagonal %s" %p
        centro = (int(i), int(j))
        maxi = dic[key1]
        mini = dic[key2]
        if (maxi >= 315 and maxi <= 45) or (maxi >= 135 and maxi <= 225):
            a = mini
            b = maxi
        else:
            a = maxi
            b = mini
        temp, puntos, col = dibuja_ec_elipse(temp, centro, a, b)
        l=0
        for s in puntos:
            if s in ptos:
                l = l + 1
        if l > 5:
            print "si es elipse"
        temp.show()
        r = int(random.random()*250)
        g = int(random.random()*250)
        b = int(random.random()*250)
        nuevo_color = (r,g,b)
        #print centro
        imagen, cont, masa, k, area_eli = bfs2(temp, centro, nuevo_color, col)
        print area_eli
        print area_total
        p = float((area_eli*100))/area_total
        print "Porcentaje area %s" %p
        print "*****************************************************"
        dib = ImageDraw.Draw(imagen)
        dib.ellipse((i-5, j-5, i+5,j+5), fill="blue")
        dib.text(centro, str(c), fill=(255,255,255))
        imagen.show()
main()
