import cv2
from pyzbar.pyzbar import decode

url = "http://192.168.137.142:8080/video"
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Converta o frame para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar QR codes no frame
    decoded_objects = decode(gray)

    # Iterar sobre os QR codes detectados
    for obj in decoded_objects:
        # Extrair o valor do QR code
        data = obj.data.decode('utf-8')
        print(data)
        # Obter as coordenadas do QR code
        rect = obj.rect
        x, y, w, h = rect.left, rect.top, rect.width, rect.height

        # Desenhar um retângulo ao redor do QR code
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Exibir o valor do QR code na tela
        cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Exibir o frame com os QR codes detectados
    cv2.imshow('Video Feed', frame)

    # Checar se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
