import cv2 as cv
def detect_squares_in_frame(frame):

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(blurred, 50, 150)
    contours, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
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
            
            # Calculando a relação de aspecto (largura/altura)
            aspect_ratio = float(w) / h
            
            # Verificando se a relação de aspecto está próxima de 1 (indicando um quadrado)
            if 0.9 <= aspect_ratio <= 1.1:
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