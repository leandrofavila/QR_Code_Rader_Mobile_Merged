import cv2

# URL do feed de vídeo do celular
url = "http://192.168.137.142:8080/video"

# Captura de vídeo usando a URL
cap = cv2.VideoCapture(url)

# Loop para exibir o vídeo da câmera do celular
while True:
    ret, frame = cap.read()  # Lê um frame do feed de vídeo
    if not ret:
        break  # Sai do loop se não houver mais frames

    cv2.imshow('Video Feed', frame)  # Exibe o frame

    # Verifica se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o objeto de captura e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()
