# PenTool (Photoshop-like)

Uma aplicação interativa em Python que recria o comportamento da ferramenta **Pen Tool** do Photoshop, utilizando **OpenCV**, **NumPy** e **curvas de Bézier** para desenhar caminhos suaves e precisos.

<img src="https://miro.medium.com/v2/resize:fit:1400/1*PiweUx0iF8H4Y79mb6o_YQ.png" width="300" alt="Descrição da imagem" />

### Exemplo de Teste da ferramenta

!["gif"](assets/exemplo.gif)

---

## Funcionalidades

- Adição de **pontos de ancoragem** com o mouse
- Manipulação de **alças de controle** para curvas Bézier cúbicas
- Geração e renderização interativa da curva
- Aperte a Tecla **S** para mover o ponto de ancoragem independentemente do ponto de ancoragem simétrico

## Como Rodar o Projeto

### Pré-requisitos

- Python 3.8+
- pip
- Numpy<2
- opencv 4.5.4.58

### Instalação

```bash
git clone https://github.com/Yuri-Kranholdt/PenTool.git
cd PenTool
pip install -r requirements.txt
