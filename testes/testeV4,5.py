import cv2 as cv
import numpy as np

def get_trackbar_values():
    def nothing(x):
        pass

def detect_squares_in_frame(frame, center_x, center_y):
    # ETAPA DE PRÉ-PROCESSAMENTO ROBUSTO
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0) # Um blur menor pode ser melhor aqui
    binary_image = cv.adaptiveThreshold(
        blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv.THRESH_BINARY_INV, # Invertemos para que o quadrado fique branco sobre fundo preto
        21, 5   # C - ajuste fino
    )

    # Opcional: Usar fechamento morfológico para unir arestas quebradas
    #kernel = np.ones((5, 5), np.uint8)
    #binary_image = cv.morphologyEx(binary_image, cv.MORPH_CLOSE, kernel)

    # Agora, use findContours na imagem binária resultante
    contours, _ = cv.findContours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contour_frame = cv.cvtColor(binary_image, cv.COLOR_GRAY2BGR)

    found_square = False
    error_x = 0
    error_y = 0



    if contours:
        # Pega o maior contorno para evitar processar ruídos menores
        largest_contour = max(contours, key=cv.contourArea)
        
        if cv.contourArea(largest_contour) > 500: # Filtro de área mínima
            epsilon = 0.04 * cv.arcLength(largest_contour, True)
            approx = cv.approxPolyDP(largest_contour, epsilon, True)

        # Verificando se o polígono tem 4 vértices
            if len(approx) == 4:
                rect = cv.minAreaRect(approx)
                (x, y), (w, h), ang = rect

                # Garante que w seja sempre a maior dimensão para um aspect ratio consistente
                if w < h:w, h = h, w
                aspect_ratio = float(w) / h if h > 0 else 0
                contour_area = cv.contourArea(approx)
                rect_area = w * h
                solidity = contour_area / rect_area if rect_area > 0 else 0
        
                # A área do contorno deve ser pelo menos 85% da área do retângulo mínimo
                # Isso elimina formas muito estranhas que não preenchem o retângulo
                if (0.85 <= aspect_ratio <= 1.2) and (solidity > 0.85):
                    found_square = True
                    # Se for um quadrado, desenhe o contorno
                    #cv.drawContours(frame, [approx], 0, (0, 255, 0), 2)
                    #cv.drawContours(contour_frame, [approx], 0, (0, 255, 0), 2)
                    
                    square_center_x = int(x)
                    square_center_y = int(y)

                    # Calcular o erro
                    error_x = square_center_x - center_x
                    error_y = square_center_y - center_y

                    # DESENHAR O QUADRADO
                    box = cv.boxPoints(rect)
                    box = np.int32(box)
                    
                    try:
                        # Desenha na janela principal
                        cv.drawContours(frame, [box], 0, (0, 255, 0), 2)
                        
                        # Desenha na janela de debug
                        cv.drawContours(contour_frame, [box], 0, (0, 255, 0), 2)
                    except cv.error as e:
                        # Opcional: imprime um aviso no console para saber que um erro de desenho ocorreu
                        print(f"Aviso: erro ao desenhar contorno ignorado - {e}")

                    # DESENHAR A RETÍCULA
                    cv.line(frame, (square_center_x - 10, square_center_y), (square_center_x + 10, square_center_y), (0, 255, 0), 1)
                    cv.line(frame, (square_center_x, square_center_y - 5), (square_center_x, square_center_y + 5), (0, 255, 0), 1)

                    # DESENHA O TEXTO
                    text_x = square_center_x - 40 # Ajuste para centralizar o texto "Quadrado"
                    text_y = square_center_y - 70# Ajuste para posicionar acima do quadrado
                    cv.putText(frame, "Quadrado", (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                        
                    # Desenha a linha do vetor de erro
                    cv.line(frame, (center_x, center_y), (square_center_x, square_center_y), (255, 255, 0), 2)
               
    #cv.imshow('Contours',contour_frame)
    return frame, error_x,error_y,found_square

def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return

    print("Pressione 'q' para sair.")

    # Variáveis para armazenar o último erro conhecido
    last_known_error_x = 0
    last_known_error_y = 0
    # Parâmetros da retícula central
    crosshair_size = 10
    crosshair_color = (0, 0, 255)
    crosshair_thickness = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Obter as dimensões do quadro
        height, width, _ = frame.shape
        center_x = int(width / 2)
        center_y = int(height / 2)

        cv.line(frame, (center_x - crosshair_size, center_y), (center_x + crosshair_size, center_y), crosshair_color, crosshair_thickness)
        cv.line(frame, (center_x, center_y - crosshair_size), (center_x, center_y + crosshair_size), crosshair_color, crosshair_thickness)

        # Chamando a função de detecção apenas UMA VEZ por loop
        processed_frame, new_error_x, new_error_y, found = detect_squares_in_frame(frame, center_x, center_y)
        
        # Lógica para atualizar o erro apenas se o quadrado for encontrado
        if found:
            last_known_error_x = new_error_x
            last_known_error_y = new_error_y
            # Mudar a cor do texto quando a detecção está ativa
            text_color = (0, 255, 0) # Verde
        else:
            # Mudar a cor do texto quando a detecção é perdida
            text_color = (0, 0, 255) # Vermelho
        # Exibe sempre o ÚLTIMO erro conhecido, com a formatação
        text_error_x = f"Erro X: {last_known_error_x:04d} px"
        text_error_y = f"Erro Y: {last_known_error_y:04d} px"
        cv.putText(processed_frame, text_error_x, (20, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        cv.putText(processed_frame, text_error_y, (20, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        cv.putText(processed_frame, f"Erro Yaw: {''} deg", (230, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv.putText(processed_frame, f"Altitude: {''} cm", (430, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv.putText(processed_frame, "Status:", (220, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)


        cv.imshow('Detecao de Quadrados', processed_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()