# Reconhecimento Facial de Colaboradores

## Visão Geral

Esta aplicação realiza o reconhecimento facial de colaboradores. <br>

Possui duas rotas principais:<br>

- **/upload**: Rota para cadastro de colaboradores com suas respectivas fotos.<br>
- **/recognize**: Rota para reconhecimento de colaboradores a partir de uma foto enviada.<br><br>

## Estrutura do Projeto

.<br>
├── Dockerfile<br>
├── docker-compose.yml<br>
├── requirements.txt<br>
├── .gitignore<br>
├── README.md<br>
├── LICENSE<br>
├── app<br>
│ ├── main.py<br>
│ ├── routes<br>
│ │ ├── upload.py<br>
│ │ ├── recognize.py<br>
│ ├── utils<br>
│ │ └── db_connection.py<br>

## Requisitos Host

- **[Docker](https://www.docker.com/)**
- **[Docker Compose](https://docs.docker.com/compose/)**

## Dependências

As dependências da aplicação estão listadas no arquivo `requirements.txt`:

- **[Flask](https://flask.palletsprojects.com/)**
- **[PyMySQL](https://pypi.org/project/PyMySQL/)**
- **[face_recognition](https://pypi.org/project/face-recognition/)**
- **[numpy](https://numpy.org/)**
- **[opencv-python-headless](https://pypi.org/project/opencv-python-headless/)**
- **[Werkzeug](https://werkzeug.palletsprojects.com/)**

## Configuração

### Docker Compose

O `docker-compose.yml` está configurado para passar variáveis de ambiente ao container da aplicação.

Substitua as variáveis em "environment" pelos dados reais que serão utilizados.

```yaml
- DB_HOST= //Host do Banco de Dados
- DB_USER= //Usuário do Banco de Dados
- DB_PASSWORD= //Senha do Banco de Dados
- DB_NAME= //Nome da Base no Banco de Dados
- SIMILARITY_THRESHOLD= //Similaridade do rosto cadastrado com o verificado, no tipo float como 0.60
``` 

## Execução
Executar com Docker Compose através do comando:

```yaml
docker-compose up --build
``` 

A aplicação estará disponível em http://localhost:5000.

## Rotas da Aplicação
1. Rota de Registro (/upload)<br><br>
    Método: POST<br>
    Descrição: Cadastra um colaborador com uma foto<br>
    Parâmetros:<br>
      - name: Nome do colaborador (string);<br>
      - registration: Matrícula do colaborador (string);<br>
      - cpf: CPF do colaborador (string);<br>
      - file: Arquivo de imagem do colaborador (file).<br>

Exemplo de Requisição:
```yaml
curl -X POST http://localhost:5000/upload \
  -F 'name=John Doe' \
  -F 'registration=123456' \
  -F 'cpf=123.456.789-00' \
  -F 'file=@path/to/image.jpg'
``` 

2. Rota de Reconhecimento (/recognize)<br><br>
  Método: POST<br>
  Descrição: Reconhece um colaborador a partir de uma foto enviada.<br>
  Parâmetros:
    - file: Arquivo de imagem (file).<br>

Exemplo de Requisição:
```yaml
curl -X POST http://localhost:5000/recognize \
  -F 'file=@path/to/image.jpg'
``` 