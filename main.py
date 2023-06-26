#Bazan Turin Kenjhy Javier

#Lo que se busca contabilizar en este caso vienen a ser la serie de saltos lalterales
#cada que se cumpla una serie de 2 saltos, tanto derecha e izquierda
#se tomara como serie completa, es decir, valida
import math

import cv2
import mediapipe as mp

video = cv2.VideoCapture('saltolateral.mp4')
pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)
draw = mp.solutions.drawing_utils
contador = 0
check = True

while True:
    success, img = video.read()
    if not success:
        break
    # videoRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Pose.process(img)
    points = results.pose_landmarks
    draw.draw_landmarks(img, points, pose.POSE_CONNECTIONS)
    # https://developers.google.com/mediapipe/solutions/vision/pose_landmarker

    h, w, _ = img.shape

    if points:
        #pieDY = (points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].y)
        #pieDX = (points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].x)
        #pieIY = (points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].y)
        #pieIX = (points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].x)
        manoDY = (points.landmark[pose.PoseLandmark.RIGHT_INDEX].y)
        manoDX = (points.landmark[pose.PoseLandmark.RIGHT_INDEX].x)
        manoIY = (points.landmark[pose.PoseLandmark.LEFT_INDEX].y)
        manoIX = (points.landmark[pose.PoseLandmark.LEFT_INDEX].x)
        
        #definimos los nuevos puntos

        #nariz
        #narizY = (points.landmark[pose.PoseLandmark.NOSE].y)
        #narizX = (points.landmark[pose.PoseLandmark.NOSE].x)
        #hombro derecho
        hombroDY = (points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].y)
        hombroDX = (points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].x)
        #hombro izquierdp
        hombroIY = (points.landmark[pose.PoseLandmark.LEFT_SHOULDER].y)
        hombroIX = (points.landmark[pose.PoseLandmark.LEFT_SHOULDER].x)

        #dist_manos = math.hypot(manoDX - manoIX, manoDY - manoIY)
        #dist_pies = math.hypot(pieDX - pieIX, pieDY - pieIY)
        #defino la distancia de la nariz, tanto a la mano izquierda como derecha
        #dist_nariz_D = math.hypot(manoDX - narizX, manoDY - narizY)
        #dist_narizI = math.hypot(narizX - manoIX, narizY - manoIY)
        

        #defino la distancia de la mano derecha al hombro izquierdo
        manoD_hombroI = math.hypot(manoDX - hombroIX, manoDY - hombroIY)

        #defino la distancia de la mano izquierda al hombro derecha
        manoI_hombroD = math.hypot(hombroDX - manoIX, hombroDY - manoIY)

        #print(f'M_der:{dist_nariz_D} M_izq:{dist_narizI} H_1:{manoD_hombroI} H_2:{manoI_hombroD}')

        print(f'ManoD_HombroI:{manoD_hombroI} ManoI_HombroD:{manoI_hombroD}')

        #si la distancia del mano derecha al hombro izquierda es larga
        #y la distancia de la mano izquierda al hombro derecho es corta
        if check == True and manoI_hombroD <= 0.10 and manoD_hombroI >= 0.20:
            check = False
            contador += 1
        
        #si la distancia del la mano izquierda al hombro derecho es larga
        #y la distancia de la mano derecha al hombro izquierdo es corta
        if manoD_hombroI < 0.10 and manoI_hombroD > 0.20:
            check = True

        texto = f'CANT.: {contador}'
        cv2.rectangle(img, (20,240), (340,120), (255,0,0), -1)
        cv2.putText(img, texto, (40,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5)

    cv2.imshow('Resultado', img)
    cv2.waitKey(30)
    
