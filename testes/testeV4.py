import cv2 as cv
import numpy as np

def get_trackbar_values():
    def nothing(x):
        pass

def detect_squares_in_frame(frame, center_x, center_y):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0) # Um blur menor pode ser melhor aqui
    binary_image = cv.adaptiveThreshold(
        blurred, 
        255, 
        cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
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

    for contour in contours:
        # Ignorar contornos muito pequenos (provavelmente ruído)
        if cv.contourArea(contour) < 200:
            continue
        # Aproximando o contorno a um polígono
        epsilon = 0.04 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        # Verificando se o polígono tem 4 vértices
        if len(approx) == 4:
            
            # 1. Use minAreaRect para ser robusto à rotação
            # Ele retorna ((centro_x, centro_y), (largura, altura), angulo_de_rotacao)
            rect = cv.minAreaRect(approx)
            (x, y), (w, h), ang = rect

            # Garante que w seja sempre a maior dimensão para um aspect ratio consistente
            if w < h:
                w, h = h, w

            aspect_ratio = float(w) / h if h > 0 else 0

            # 2. Use a área do contorno para um critério de "solidez"
            contour_area = cv.contourArea(approx)
            rect_area = w * h

            # A área do contorno deve ser pelo menos 85% da área do retângulo mínimo
            # Isso elimina formas muito estranhas que não preenchem o retângulo
            solidity = contour_area / rect_area if rect_area > 0 else 0
    

            # Verificando se a relação de aspecto está próxima de 1 (indicando um quadrado)
            if (0.85 <= aspect_ratio <= 1.2) and (solidity > 0.85):
                found_square = True
                # Se for um quadrado, desenhe o contorno
                cv.drawContours(frame, [approx], 0, (0, 255, 0), 2)
                cv.drawContours(contour_frame, [approx], 0, (0, 255, 0), 2)
                
                # ### NOVO ### Calcular o centro do quadrado
                square_center_x = int(x + w / 2)
                square_center_y = int(y + h / 2)

                # ### NOVO ### Calcular o erro
                error_x = square_center_x - center_x
                error_y = square_center_y - center_y

                # Localizacao do texto
                text_x = int(x + w/2)
                text_y = int(y - 10)
                
                # Desenhando o nome "Quadrado"
                cv.putText(frame, "Quadrado", (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                # Desenhando a reticula horizontal e vertical
                cv.line(frame, 
                        (int(x + w / 2) - 10, int(y + h / 2)), 
                        (int(x + w / 2) + 10, int(y + h / 2)), 
                        (0,255,0), 
                        1)
                cv.line(frame, 
                        (int(x + w / 2), int(y + h / 2) - 4), 
                        (int(x + w / 2), int(y + h / 2) + 4), 
                        (0,255,0), 
                        1)
                
                # ### NOVO ### Desenhar linha do centro da tela ao centro do quadrado (vetor de erro)
                cv.line(frame, (center_x, center_y), (square_center_x, square_center_y), (255, 255, 0), 1)
                
                # Quebra o loop para processar apenas o primeiro quadrado detectado (o mais provável)
                break
    '''          
    # ### NOVO ### Exibir os valores de erro na tela
    text_error_x = f"Erro X: {error_x:04d} pixels"
    text_error_y = f"Erro Y: {error_y:04d} pixels"
    cv.putText(frame, text_error_x, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.7, (255, 0, 0), 2)
    cv.putText(frame, text_error_y, (10, 50), cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)
    '''
    cv.imshow('Contours',contour_frame)
    return frame, error_x,error_y,found_square

def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return

    get_trackbar_values()
    print("Pressione 'q' para sair.")

        # ### NOVO ### Variáveis para armazenar o último erro conhecido
    last_known_error_x = 0
    last_known_error_y = 0

    crosshair_size = 10
    crosshair_color = (0, 0, 255)
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

                # ### ALTERADO ### Captura os valores retornados pela função
        processed_frame, new_error_x, new_error_y, found = detect_squares_in_frame(frame, center_x, center_y)
        
        # ### NOVO ### Lógica para atualizar o erro apenas se o quadrado for encontrado
        if found:
            last_known_error_x = new_error_x
            last_known_error_y = new_error_y
            # Opcional: Mudar a cor do texto quando a detecção está ativa
            text_color = (0, 255, 0) # Verde
        else:
            # Opcional: Mudar a cor do texto quando a detecção é perdida
            text_color = (0, 0, 255) # Vermelho
         # ### ALTERADO ### Exibe sempre o ÚLTIMO erro conhecido, com a formatação
        text_error_x = f"Erro X: {last_known_error_x:04d} pixels"
        text_error_y = f"Erro Y: {last_known_error_y:04d} pixels"
        cv.putText(processed_frame, text_error_x, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        cv.putText(processed_frame, text_error_y, (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)


                # ### ALTERADO ### Captura os valores retornados pela função
        processed_frame, new_error_x, new_error_y, found = detect_squares_in_frame(frame, center_x, center_y)
        
        cv.imshow('Detecao de Quadrados', processed_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()