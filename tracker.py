# Importamos las librerias
import dlib
import cv2
import get_points

# empezamos la captura de video
cap = cv2.VideoCapture(0)
print('Pulsa "P" para pausar el video y empezar el seguimiento')

def tracker(img, puntos):
    # obtenemos las cordenadas iniciales del objeto a rastrear
    # creamos el objeto de seguimiento
    tracker = dlib.correlation_tracker()

    # proporcionamos al rastreador la posicion original del objeto
    tracker.start_track(img, dlib.rectangle(*points[0]))
    while True:
        # leemso la imagen desde la captura o archivo
        ret, img = cap.read()
        if not ret:
            print('No se ha ejecutado la captura :-(')
            exit()

        # actualizamos el seguimiento del objeto
        tracker.update(img)

        # obtenemos la posicion del objeto y dibujamos un cuadro delimitador
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        print('Objeto trackeado en [{}, {}] \r'.format(pt1, pt2),)
        loc = (int(rect.left()), int(rect.top() - 20))
        txt = 'Objeto trackeado en [{}, {}]'.format(pt1, pt2)
        cv2.putText(img, txt, loc, cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Image', img)

        # sigue la ejecución hasta que se presione escape
        if cv2.waitKey(1) == 27:
            break

# ejecutamos el while
while True:
    # leemos los frames
    ret, frame = cap.read()

    # leemos del teclado
    t = cv2.waitKey(1)

    # si no hay captura entonces
    if not ret:
        print('No se pudo capturar la camara.')
        exit()

    # si se oprime P se cierra
    if (t == ord('p')):
        # las coordenadas del objeto a rastrear se almacenan en una lista llamada puntos
        points = get_points.run(frame)
        if not points:
            print('ERROR: No objeto de seguimiento.')
            exit()
        if points:
            tracker(img = frame, puntos = points)
        break

    # mostramos los frames
    cv2.imshow('IMAGEN', frame)

# ceramos la ventana
cv2.destroyAllWindows()
