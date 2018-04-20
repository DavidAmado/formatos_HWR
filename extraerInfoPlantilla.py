import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance, ImageFilter, ImageChops
from shapedetector import ShapeDetector
import os
from pdf2im import pdf_to_jpg
import sys



def extraerInfoPlantilla(path_pdf):
	
	dir_pdf2im = os.path.splitext(os.path.basename(path_pdf))[0]
	pdf_to_jpg(path_pdf,dir_pdf2im)
	print dir_pdf2im
	pag0(dir_pdf2im)


def pag0(dir_pdf2im):
	dirImgsRec=dir_pdf2im+"/pag0"
	os.mkdir(dirImgsRec)
	path=dir_pdf2im+"/pag0.jpg"
	img = Image.open(path).convert("RGB")
	imm = cv2.imread(path)


	tamX,tamY=img.size

	imgs=[img.crop((0,0,tamX*0.22,tamY*0.07)),
		img.crop((tamX-tamX*0.22,0,tamX,tamY*0.07)),
		img.crop((0,tamY-tamY*0.07,tamX*0.22,tamY)),
		img.crop((tamX-tamX*0.22,tamY-tamY*0.07,tamX,tamY))]

	imgs=[ImageChops.invert(i) for i in imgs]

	imgs=[np.array(i.getdata()).reshape(i.size[1], i.size[0], 3).astype(np.uint8) for i in imgs]	#conversion de imagen a np.array con el formato para que reconozca la imagen
	sd=ShapeDetector()
	posTriangulos=[]
	for im in imgs:													
		
		ratio = im.shape[0]

		imgA5 = cv2.pyrMeanShiftFiltering(im,70,71)
		imagen5 = cv2.cvtColor(imgA5,cv2.COLOR_BGR2GRAY)
		_,contours5,_ = cv2.findContours(imagen5,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		im5=im.copy()

		for cnt in contours5:
		
			M = cv2.moments(cnt)
			if M['m00'] != 0:
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])

				shape = sd.detect(cnt)
				cont = cnt.astype("float")
				cont *= ratio
				cont = cont.astype("int")
				center = (cx,cy)
				area = cv2.contourArea(cnt)
				if area > 2000 and shape=="triangle":
					posTriangulos+=[center]				

	print(posTriangulos)
	if(len(posTriangulos)==4):
		posTriangulos[1]=(posTriangulos[1][0]+int(tamX-tamX*0.22),posTriangulos[1][1])
		posTriangulos[2]=(posTriangulos[2][0],posTriangulos[2][1]+tamY-int(tamY*0.07))
		posTriangulos[3]=(posTriangulos[3][0]+tamX-int(tamX*0.22),posTriangulos[3][1]+tamY-int(tamY*0.07))


		for pos in posTriangulos:
			print("pos",pos)
			cv2.putText(imm, ".triangle".format(pos),pos,cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.3,(255,0,0,3))
			

		alto = posTriangulos[2][1]-posTriangulos[0][1]
		ancho = posTriangulos[1][0]-posTriangulos[0][0]

		p=(ix,iy)=(ancho*0.07753+posTriangulos[0][0],alto*2854/7000+posTriangulos[0][1])
		pos=[ix,iy]
		print p

		#------------------------------------------------------------------------------------------
		dx=7.952286282306163*ancho/100
		dy=0.0187*alto
		ax=7.703777335984095*ancho/100
		ay=0.01849*alto
		for j in range(29):
			for i in range(3):
				rec = img.crop((int(pos[0]),int(pos[1]),int(pos[0]+dx),int(pos[1]+dy)))
				pos[0]+=ax
				rec.save(dirImgsRec+"/imRec-C0-"+str(j)+"-"+str(i)+".jpg")

			pos[0]=ix
			pos[1]+=ay


		ix=ancho*0.4383697813121272+posTriangulos[0][0]
		pos=[ix,iy]
		for j in range(29):
			for i in range(3):
				rec = img.crop((int(pos[0]),int(pos[1]),int(pos[0]+dx),int(pos[1]+dy)))
				pos[0]+=ax
				rec.save(dirImgsRec+"/imRec-C1-"+str(j)+"-"+str(i)+".jpg")
			pos[0]=ix
			pos[1]+=ay


		ix = ancho*0.7982107355864811+posTriangulos[0][0]
		pos=[ix,iy]
		for j in range(28):
			for i in range(3):
				rec = img.crop((int(pos[0]),int(pos[1]),int(pos[0]+dx),int(pos[1]+dy)))
				pos[0]+=ax
				rec.save(dirImgsRec+"/imRec-C2-"+str(j)+"-"+str(i)+".jpg")
			pos[0]=ix
			pos[1]+=ay
	else:
		print("se presento un fallo en el archivo, # de triangulos:",len(posTriangulos))

for i in range(1,len(sys.argv)):
	extraerInfoPlantilla(sys.argv[i])

