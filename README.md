# Sympla Scraper

Esse projeto é um web scraper que coleta informações de eventos no site da Sympla.

## Como funciona

O scraper coleta informações de eventos categorizados no site da Sympla e as armazena em um arquivo CSV. As informações coletadas são:

- Nome do evento
- Data do evento
- Local do evento
- Link para a página do evento
- Categoria do evento

## Como usar

Para usar o scraper sem a utilização de um arquivo executável, é necessário ter o Python instalado na máquina.

### Instalação dos requisitos

Para instalar as dependências do projeto, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

### Execução

Para executar o scraper, execute o seguinte comando:

```bash
python main.py
```

O scraper utiliza o arquivo `categorias.csv` para obter as categorias de eventos que serão coletadas. Caso deseja alterar as categorias, basta editar esse arquivo.

O arquivo CSV com as informações coletadas será salvo no arquivo `eventos.csv`.

## Utilização do arquivo executável

Para utilizar o arquivo executável, basta executar o arquivo executável gerado.

### Para Windows

O arquivo executável gerado para Windows está disponível na pasta `dist` do projeto, com o nome `windows_sympla.exe`. O arquivo `categorias.csv` deve estar na mesma pasta que o executável.

O arquivo executável para Windows foi gerado em um ambiente Windows 11.

### Para Linux

O arquivo executável gerado para Linux está disponível na pasta `dist` do projeto, com o nome `linux_sympla`. O arquivo `categorias.csv` deve estar na mesma pasta que o executável ou você pode rodar o executável em um terminal que esteja na mesma pasta que o arquivo `categorias.csv`.

O arquivo executável para Linux foi gerado em um ambiente Ubuntu 22.04.

### Troubleshooting

Caso o executável esteja abrindo e fechando rapidamente, quer dizer que a sua "tarefa" foi finalizada. Isso pode significar que as categorias mencionadas em `categorias.csv` são pequenas ou o arquivo não foi encontrado.

## Gerando um executável

Para gerar um arquivo executável, é necessário ter o PyInstaller instalado. Para instalá-lo, execute o seguinte comando:

```bash
pip install pyinstaller
```

Para gerar o executável, execute o seguinte comando:

```bash
pyinstaller main.py --onefile
```
