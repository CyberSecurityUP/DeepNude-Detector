from nudenet import NudeClassifier
import cv2
import os
import requests
from PIL import Image
import random
import string

class NudeDetector:
    def __init__(self):
        # Inicializa o classificador do NudeNet
        self.classifier = NudeClassifier()

    def generate_random_name(self, length=5):
        # Gera um nome aleatório de 'length' letras
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def download_image_from_url(self, url):
        # Gera um nome de arquivo aleatório para a imagem baixada
        random_name = self.generate_random_name()
        save_path = f"{random_name}.jpg"

        # Faz o download da imagem de uma URL e salva localmente
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as out_file:
                out_file.write(response.content)
            print(f"Imagem baixada com sucesso de {url} para {save_path}")
            return save_path
        else:
            print(f"Erro ao baixar a imagem de {url}")
            return None

    def detect(self, img_path, min_prob=0.84):
        # Realiza a detecção de nudes
        result = self.classifier.classify(img_path)

        # Filtra os resultados e separa as imagens impróprias e não impróprias
        detections = []
        for image, output in result.items():
            if output['unsafe'] >= min_prob:
                detections.append({
                    'image': image,
                    'unsafe_score': output['unsafe'],
                    'improper': True  # Flag para conteúdo impróprio
                })
            else:
                detections.append({
                    'image': image,
                    'unsafe_score': output['unsafe'],
                    'improper': False  # Flag para conteúdo não impróprio
                })
        return detections

    def censor(self, img_path, out_path=None, visualize=False):
        image = cv2.imread(img_path)
        results = self.detect(img_path)

        if not results:
            print("Nenhum conteúdo explícito encontrado.")
            return

        for result in results:
            unsafe_score = result['unsafe_score']
            if result['improper']:
                print(f"Conteúdo impróprio detectado com pontuação {unsafe_score:.2f}")
                # Blure a imagem para censurar
                image = cv2.GaussianBlur(image, (99, 99), 30)
            else:
                print(f"Conteúdo não impróprio detectado. Nota: {unsafe_score:.2f}")

        if visualize:
            # Converte a imagem de BGR (OpenCV) para RGB (Pillow)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            pil_image.show()

        if out_path:
            cv2.imwrite(out_path, image)
            print(f"Imagem censurada salva em {out_path}")

if __name__ == "__main__":
    detector = NudeDetector()

    try:
        while True:
            print("\nEscolha uma opção:")
            print("1. Analisar uma imagem local")
            print("2. Analisar uma imagem a partir de uma URL")

            option = input("Digite o número da opção desejada: ")

            if option == '1':
                img_path = input("Digite o caminho para a imagem local: ")
            elif option == '2':
                img_url = input("Digite a URL da imagem: ")
                img_path = detector.download_image_from_url(img_url)
                if not img_path:
                    continue  # Se o download falhar, volta ao início
            else:
                print("Opção inválida.")
                continue

            # Detecta nudez na imagem com min_prob de 0.84
            detections = detector.detect(img_path, min_prob=0.84)
            for detection in detections:
                if detection['improper']:
                    print(f"Conteúdo impróprio detectado com nota {detection['unsafe_score']:.2f}")
                else:
                    print(f"Conteúdo não impróprio detectado. Nota: {detection['unsafe_score']:.2f}")

            # Pergunta se o usuário deseja censurar a imagem
            censor_option = input("Deseja censurar a imagem? (s/n): ").lower()
            if censor_option == 's':
                # Gera um nome de arquivo censurado com o padrão
                random_name = detector.generate_random_name()
                censored_output_path = f"censored_{random_name}.jpg"
                detector.censor(img_path, out_path=censored_output_path, visualize=True)
            else:
                print("Censura não aplicada.")

    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário. Encerrando...")
