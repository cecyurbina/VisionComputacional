#!/usr/bin/python
from Tkinter import *
from PIL import Image, ImageTk
import math
import sys
import filtros
import random
import ImageFont, ImageDraw
import Image

class Aplicacion:
    """clase que dibuja los botones
    """
    def __init__(self, master, imagen_path):
        self.nombre_imagen = imagen_path
        self.imagen_original = filtros.abrir_imagen(self.nombre_imagen)
        self.x, self.y = self.imagen_original.size
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.imagen_actual = self.imagen_original
        #se posicionan los botones
        self.colorear = Button(self.frame, text="Colorear", fg="blue", command=self.colorear)
        self.reset = Button(self.frame, text="reset", fg="blue", command=self.reiniciar)
        self.guarda = Button(self.frame, text="guardar", fg="blue", command=self.guardar)
        self.masa = Button(self.frame, text="centroMasa", fg="blue")
        self.colorear.grid(row=0, column=0,padx=15, pady=15)
        self.masa.grid(row=0, column=1,padx=15, pady=15)
        self.reset.grid(row=0, column=2,padx=15, pady=15)
        self.guarda.grid(row=0, column=3,padx=15, pady=15)
        #se abre la imagen                     
        foto = Image.open(imagen_path)
        foto = ImageTk.PhotoImage(foto)
        self.picture = Label(self.frame, image=foto)
        self.picture.image = foto
        self.picture.grid(row=1, column=0, columnspan=4,sticky=W+E+N+S, padx=5, pady=5)

    def actualizar_imagen(self):
        """redibuja la foto en la ventana
        """
        foto  = ImageTk.PhotoImage(self.imagen_actual)
        self.picture = Label(self.frame, image=foto)
        self.picture.image = foto
        self.picture.grid(row=1, column=0, columnspan=4,sticky=W+E+N+S, padx=5, pady=5)
        self.imagen_actual.save("imagen_nueva.png")

    def reiniciar(self):
        """
        funcion que regresa la foto al estado inicial
        """
        self.imagen_actual = self.imagen_original
        self.actualizar_imagen()

    def guardar(self):
        """guarda la imagen con el nombre
        imagen_nueva.png
        """
        self.imagen_actual.save("imagen_nueva.png")
        
    def colorear(self):
        """colorea la figura
        """
        self.imagen_actual, colores = encuentra_formas(self.imagen_actual)
        self.actualizar_imagen()
        im = Image.open("imagen_nueva.png")
        draw = ImageDraw.Draw(im)
        for i in range(len(colores)):
            if colores[i][2] > .1:
                draw.ellipse((colores[i][1][0]-2, colores[i][1][1]-2, colores[i][1][0]+2, colores[i][1][1]+2), fill=(0,0,0))
                draw.text((colores[i][1]), str(i), fill=(0,0,0))
                print "ID  %s    Porcentaje  %s" %(i, colores[i][2])
        self.imagen_actual = im
        self.actualizar_imagen()

        
def bfs(imagen, origen, color):
    """colorea todo el objeto recibe como parametros el 
    nuevo color con el que se pinta,la coordenada de inicio y
    la imagen, y regresa un arreglo con la masa y la imagen
    """
    cola = []
    cont = 0
    masa = []
    pixeles = imagen.load()
    alto, ancho = imagen.size
    cola.append(origen)
    original = pixeles[origen]
    todos_pixeles = []
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
                            todos_pixeles.append((pix_x, pix_y))
    imagen.save('algo', 'png')
    return imagen, cont, masa, todos_pixeles

def encuentra_formas(imagen):
    """cambia el color de cada objeto en
    la imagen llamando por cada uno a la 
    funcion bfs
    """
    alto, ancho = imagen.size
    pixeles = imagen.load()
    colores = []
    porcentaje = []
    contornos = []
    for i in range(alto):
        for j in range(ancho):
            if pixeles[i,j] == (255,255,255):
                r = int(random.random()*250)
                g = int(random.random()*250)
                b = int(random.random()*250)
                nuevo_color = (r,g,b)
                imagen, cont, masa, todos_pixeles = bfs(imagen, (i,j), nuevo_color)
                contornos.append(todos_pixeles)
                print "CAMBIA"
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
    print color_mayor
    imagen.save('antes.png', 'png')
    identifica_fondo(imagen, color_mayor)
    imagen.save('resultado.png', 'png')
    cont = []
    for i in range(len(contornos)):
        hull = filtros.aplicar_jarvi(contornos[i])
        cont.append(hull)
    print hull
    im = Image.open("resultado.png")
    draw = ImageDraw.Draw(im)
    for i in range(len(cont)):
        for j in range(len(cont[i])):
            try:
                linea = (cont[i][j][0],cont[i][j][1],cont[i][j+1][0],cont[i][j+1][1])
            except:
                break
            draw.ellipse((cont[i][j][0], cont[i][j][1], 10,10), fill=(255,255,255))
            draw.line(linea, fill="green", width=2)

    im.save("hull.png")
    return imagen, colores

def identifica_fondo(imagen, color_max): 
    #pintamos fondo de manera que obtenemos el color que predomina en la imagen
    pixeles = imagen.load()
    x, y = imagen.size
    for a in range(x):
        for b in range(y):
            if pixeles[a, b] == color_max:
                color = (210,210,210)
                imagen, masa, n, todos_pixeles = bfs(imagen, (a, b), color)
                return imagen

def main():
    """funcion principal
    """
    try:
        imagen_path = sys.argv[1]
        print imagen_path
        imagen = filtros.abrir_imagen(imagen_path)
        
    except:
        print "No seleccionaste una imagen"
        return
    #encuentra_formas(imagen)
    root = Tk()
    App = Aplicacion(root, imagen_path)
    root.title("Imagenes")
    root.mainloop()

if __name__ == "__main__":
    main()

