# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 18:16:25 2022

@author: Peixe
"""

import cv2

path1 = 'Spray_length_routine/Image_calibracao.tif'
img1 = cv2.imread(path1)
path2 = 'Spray_length_routine/Image.6tla7g5f.000061.tif'
img2 = cv2.imread(path2)
ret,thresh = cv2.threshold(img2,3.85,255,cv2.THRESH_BINARY)

# iterating till the range
for i in range(0, 1):  # coordenadas em x e y de referencia
    elex = int((input(("Adicionar as coordenadas em x: "))))
    eley = int((input(("Adicionar as coordenadas em y: "))))
    list = [elex, eley]

class DrawLineWidget(object):
    def __init__(self):
        self.original_image = cv2.imread(path1)
        self.clone1 = self.original_image.copy()
        self.i=1
        self.d_pxx=10
        self.d_pxy=15
        self.original_image2 = thresh
        self.clone2 = self.original_image2.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # List to store start/end points
        self.image_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):

        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x, y)]


        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x, y))
            print('Starting: {}, Ending: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))


            # Draw line

            if self.i == 1:
                cv2.line(self.clone1, self.image_coordinates[0], self.image_coordinates[1], (36, 255, 12), 2)
                cv2.imshow("image", self.clone1)
                e = (self.image_coordinates[0][0])
                f = (self.image_coordinates[0][1])
                g = (self.image_coordinates[1][0])
                h = (self.image_coordinates[1][1])
                self.d_pxx = elex / (g-e)
                self.d_pxy = eley / (h-f)
                print(self.d_pxx)
                print(self.d_pxy)
                self.i = 2
            else:
                cv2.line(self.clone2, self.image_coordinates[0], self.image_coordinates[1], (36, 255, 12), 2)
                cv2.imshow("image", self.clone2)
                print('Distancia em x:',((self.image_coordinates[0][0] - self.image_coordinates[1][0]) * self.d_pxx),'mm')
                print('Distancia em y:',((self.image_coordinates[0][1] - self.image_coordinates[1][1])),'mm')
                print('Distancia total:',((((self.image_coordinates[0][0] - self.image_coordinates[1][0]) * self.d_pxx)**2+((self.image_coordinates[0][1] - self.image_coordinates[1][1]) * self.d_pxy)**2)**(0.5)),'mm')

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone1 = self.original_image.copy()
            self.i=1

    def show_image(self):
        if self.i == 1:
            return self.clone1
        else:
            return self.clone2

if __name__ == '__main__':
    draw_line_widget = DrawLineWidget()
    while True:
        cv2.imshow('image', draw_line_widget.show_image())
        key = cv2.waitKey(1)
        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)