# Sistema de Pouso Autônomo de Drone (Visão Computacional)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

**Contexto:** Este projeto foi desenvolvido em coautoria com Fernanda Paoleschi (UPE) como case técnico e prático para o processo seletivo do **DeltaV Drones**, projeto de extensão focado em veículos aéreos autônomos da Escola Politécnica de Pernambuco (Poli/UPE).

---

## Demonstração do Sistema

https://github.com/user-attachments/assets/8276738a-6aa5-4191-8ade-fb76d31ec8ae

## Sobre o Projeto

Este repositório implementa o sistema de processamento visual para o pouso autônomo de um drone. Desenvolvido em Python com OpenCV, o sistema processa o feed de vídeo em tempo real, identifica um marcador no solo (alvo de pouso), calcula o vetor de erro (eixos X e Y) para centralização e estima a altitude (eixo Z) utilizando princípios de geometria de câmera. O controle do fluxo é gerenciado por uma máquina de estados finitos que simula as fases de um pouso seguro.

## Arquitetura e Pipeline de Visão

O pipeline de processamento de imagens foi estruturado para garantir robustez contra ruídos e variações de iluminação:
* **Pré-Processamento:** Conversão para tons de cinza, aplicação de `GaussianBlur` para suavização e `AdaptiveThreshold` para binarização dinâmica e resistente a sombras.
* **Detecção e Validação de Contornos:** Extração de polígonos e validação rigorosa do alvo utilizando cálculos estritos de *Aspect Ratio* (0.85 a 1.2) e *Solidity* (> 0.85), impedindo falsos positivos.
* **Máquina de Estados de Voo:** Controle autônomo do status da missão transitando entre as fases: `PROCURANDO ALVO` -> `CENTRALIZANDO` -> `INICIANDO DESCIDA` -> `APROX. FINAL` -> `POUSO REALIZADO`.

## Calibração e Matemática Aplicada

O cálculo de altitude (distância no eixo Z) não utiliza valores numéricos arbitrários. O repositório inclui um script dedicado de calibração que extrai a distância focal da lente da câmera a partir da seguinte equação:

$$F = \frac{P \times D}{W}$$

Onde `P` é a largura do alvo em pixels, `D` é a distância física configurada e `W` é a largura física do objeto. Com o sistema calibrado, a telemetria de altitude do drone é gerada em tempo real por:

$$D = \frac{W \times F}{P}$$

## A Pasta "Aprendizado"

Todo o embasamento teórico e as provas de conceito preliminares estão documentados na pasta `Aprendizado`. Ela contém os scripts de calibração de câmera, testes de filtros de imagem isolados e as anotações matemáticas que fundamentaram a construção do script principal da missão.

## Como Executar

1. Clone este repositório:
   `git clone https://github.com/BizzoK/VisCom-DroneAutonomo.git`
2. Instale as dependências listadas:
   `pip install opencv-python numpy`
3. Execute o script principal (é necessário possuir uma webcam conectada):
   `python missaoAutonoma.py`

> **Nota de Configuração de Ambiente:**
> O sistema `missaoAutonoma.py` está atualmente calibrado para um alvo de **30x30cm** utilizando a distância focal do hardware de desenvolvimento (`F = 476`). Para testar localmente com precisão:
> 1. Execute o script `calibracao.py` (localizado na pasta `Aprendizado`) utilizando o seu próprio alvo em uma distância conhecida.
> 2. Atualize as variáveis globais `KNOWN_WIDTH_CM` e `FOCAL_LENGTH_PIXELS` no topo do script principal com os valores obtidos na sua aferição.
