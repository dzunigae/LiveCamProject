import cv2
import socket
import struct

# Iniciar la cámara
cap = cv2.VideoCapture(0)

# Iniciar el socket UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Iniciar el codificador de video
fourcc = cv2.VideoWriter_fourcc(*"MJPG")

while True:
    # Capturar un frame
    ret, frame = cap.read()
    if not ret:
        break

    # Mostrar el frame en una ventana
    cv2.imshow("Streaming", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # Codificar el frame en formato JPEG
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
    if not result:
        break

    # Enviar el frame codificado a través del socket UDP
    sock.sendto(encoded_frame.tobytes(), (UDP_IP, UDP_PORT))

# Liberar la cámara y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
sock.close()