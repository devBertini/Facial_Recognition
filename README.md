# Reconhecimento Facial de Colaboradores

## Visão Geral

Esta aplicação realiza o reconhecimento facial de colaboradores. 

Possui duas rotas principais:

**/upload**: Rota para cadastro de colaboradores com suas respectivas fotos.
**/recognize**: Rota para reconhecimento de colaboradores a partir de uma foto enviada.

## Estrutura do Projeto

.
├── Dockerfile<br>
├── docker-compose.yml
├── main.py
├── requirements.txt
├── routes
│ ├── init.py
│ ├── upload.py
│ ├── recognize.py
├── utils
│ └── db_connection.py
└── data
└── images

## Requisitos

- Python 3.8+
- Docker
- Docker Compose

## Dependências

As dependências da aplicação estão listadas no arquivo `requirements.txt`:

- Flask
- PyMySQL
- face_recognition
- numpy
- opencv-python-headless
- Werkzeug

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
Executar com Docker Compose

Construir e executar a aplicação:
```yaml
docker-compose up --build
``` 

A aplicação estará disponível em http://localhost:5000.

## Rotas da Aplicação
1. Rota de Upload (/upload)
    Método: POST.
    Descrição: Cadastra um colaborador com uma foto.
    Parâmetros:
        - name: Nome do colaborador (string);
        - registration: Matrícula do colaborador (string);
        - cpf: CPF do colaborador (string);
        - file: Arquivo de imagem do colaborador (file).

Exemplo de Requisição:
```yaml
curl -X POST http://localhost:5000/upload \
  -F 'name=John Doe' \
  -F 'registration=123456' \
  -F 'cpf=123.456.789-00' \
  -F 'file=@path/to/image.jpg'
``` 

2. Rota de Reconhecimento (/recognize)
  Método: POST.
  Descrição: Reconhece um colaborador a partir de uma foto enviada.
  Parâmetros:
    - file: Arquivo de imagem (file).

Exemplo de Requisição:
```yaml
curl -X POST http://localhost:5000/recognize \
  -F 'file=@path/to/image.jpg'
``` 