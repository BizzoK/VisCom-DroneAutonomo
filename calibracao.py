# --- SCRIPT DE CALIBRACAO ---
import cv2 as cv
import numpy as np

# --- CONFIGURAÇÕES ---
# 1. MUDE AQUI para a largura real do seu objeto em centímetros
KNOWN_WIDTH_CM = 30  
# 2. MUDE AQUI para a distância que você posicionou o objeto da câmera em centímetros
KNOWN_DISTANCE_CM = 42 
# --------------------

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    binary_image = cv.adaptiveThreshold(
        blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv.THRESH_BINARY_INV, 21, 5
    )
    
    contours, _ = cv.findContours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv.contourArea)
        if cv.contourArea(largest_contour) > 500:
            rect = cv.minAreaRect(largest_contour)
            (x, y), (w, h), ang = rect
            
            # Pega a maior dimensão do retângulo rotacionado como a largura em pixels
            pixel_width = max(w, h)
            
            box = cv.boxPoints(rect)
            box = box.astype(np.int32)
            cv.drawContours(frame, [box], 0, (0, 255, 0), 2)
            
            text = f"Largura em Pixels: {pixel_width:.2f}"
            cv.putText(frame, text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv.imshow("Calibracao", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
