import cv2 as cv
import numpy as np

def get_trackbar_values():
    def nothing(x):
        pass

    cv.namedWindow('Trackbars')
    cv.createTrackbar('Threshold1', 'Trackbars', 50, 255, nothing)
    cv.createTrackbar('Threshold2', 'Trackbars', 150, 255, nothing)
    cv.createTrackbar('Dilate_Kernel', 'Trackbars', 1, 5, nothing)

def detect_squares_in_frame(frame):
    # Obtém os valores dos trackbars
    threshold1 = cv.getTrackbarPos('Threshold1', 'Trackbars')
    threshold2 = cv.getTrackbarPos('Threshold2', 'Trackbars')
    dilate_kernel_size = cv.getTrackbarPos('Dilate_Kernel', 'Trackbars')
    
    # Convertendo para escala de cinza e aplicando desfoque
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (7, 7), 0)  # Aumentado o kernel para 7x7
    # Usando Canny com os limiares ajustáveis
    edges = cv.Canny(blurred, threshold1, threshold2)
    
    # Cria um kernel (elemento estruturante)
    if dilate_kernel_size > 0:
        kernel = np.ones((dilate_kernel_size, dilate_kernel_size), np.uint8)
        # Aplica a dilatação
        edges = cv.dilate(edges, kernel, iterations=1)
    
    cv.imshow('Edges', edges)

    # Encontrando os contornos
    contours, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Copia colorida do quadro para desenhar os contornos
    contour_frame = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

    for contour in contours:
        # Ignorar contornos muito pequenos (provavelmente ruído)
        if cv.contourArea(contour) < 200:
            continue

        # Aproximando o contorno a um polígono
        epsilon = 0.04 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        # Verificando se o polígono tem 4 vértices
        if len(approx) == 4:
            # Pegando as coordenadas do retângulo delimitador
            x, y, w, h = cv.boundingRect(approx)
            
            aspect_ratio = float(w) / h
            
            # Verificando se a relação de aspecto está próxima de 1 (indicando um quadrado)
            if 0.8 <= aspect_ratio <= 1.3:
                # Se for um quadrado, desenhe o contorno
                cv.drawContours(frame, [approx], 0, (0, 255, 0), 2)
                cv.drawContours(contour_frame, [approx], 0, (0, 255, 0), 2)
                
                # Posicionando o texto
                text_x = int(x + w/2)
                text_y = int(y - 10)
                
                # Desenhando o nome "Quadrado"
                cv.putText(frame, "Quadrado", (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                # Desenhando a reticula horizontal e vertical
                cv.line(frame, 
                        (int(x + w / 2) - 4, int(y + h / 2)), 
                        (int(x + w / 2) + 4, int(y + h / 2)), 
                        (0,255,0), 
                        1)
                cv.line(frame, 
                        (int(x + w / 2), int(y + h / 2) - 4), 
                        (int(x + w / 2), int(y + h / 2) + 4), 
                        (0,255,0), 
                        1)
                
    cv.imshow('Contours',contour_frame)
    return frame

def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return

    get_trackbar_values()
    print("Pressione 'q' para sair.")

    # Definir o tamanho da mira
    crosshair_size = 4
    # Definir a cor da mira
    crosshair_color = (0, 0, 255)
    # Definir a espessura da linha
    crosshair_thickness = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Obter as dimensões do quadro
        height, width, _ = frame.shape
        # Calcular o centro da imagem
        center_x = int(width / 2)
        center_y = int(height / 2)

         # Desenhar a linha horizontal da mira
        cv.line(frame, (center_x - crosshair_size, center_y), (center_x + crosshair_size, center_y), crosshair_color, crosshair_thickness)
        # Desenhar a linha vertical da mira
        cv.line(frame, (center_x, center_y - crosshair_size), (center_x, center_y + crosshair_size), crosshair_color, crosshair_thickness)

        processed_frame = detect_squares_in_frame(frame)
        cv.imshow('Detecao de Quadrados', processed_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()