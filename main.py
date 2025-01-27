from bs4 import BeautifulSoup
from unidecode import unidecode
from pathlib import Path
import requests
import re
import time
import pandas as pd

INPUT_FILE = "categorias.csv"
OUTPUT_FILE = "eventos.csv"

input_file_path = Path(INPUT_FILE)
output_file_path = Path(OUTPUT_FILE)
base_url = "https://www.sympla.com.br/eventos"

# As categorias são definidas estaticamente para facilitar a busca.
# Caso a categoria fosse dinâmica, o Beautiful Soup não seria a melhor opção,
# pois ele não executa JavaScript.
categories = {
    "Festas e Shows": "17-festas-e-shows",
    "Cursos e Workshops": "8-curso-e-workshops",
    "Congressos e Palestras": "4-congressos-e-palestras",
    "Esportes": "2-esportes",
    "Gastronomia": "1-gastronomia",
    "Arte, Cinema e Lazer": "10-arte-cinema-e-lazer",
    "Saúde e Bem-Estar": "9-saude-e-bem-estar",
    "Infantil": "15-infantil",
    "Religião e Espiritualidade": "13-religiao-e-espiritualidade",
    "Games e Geek": "12-games-e-geek",
    "Moda e Beleza": "11-moda-e-beleza",
    "Pride": "14-pride",
}

# Dicionário para facilitar a busca de categorias.
# Mesmo se o usuário digitar uma categoria com (ou sem) acentos, o programa irá
# reconhecer a categoria.
unidecode_categories = {unidecode(category.lower()): category for category in categories}

def check_category(category: str) -> bool:
    """
    Verifica se a categoria existe. 
    """
    unidecode_category = unidecode(category.lower())
    return unidecode_category in unidecode_categories


def check_all_categories(categories: list[str]) -> None:
    """
    Verifica se todas as categorias existem.
    """
    invalid_categories = []
    for category in categories:
        if not check_category(category):
            invalid_categories.append(category)
    
    if invalid_categories:
        raise ValueError(f"Categoria(s) não encontrada(s): {', '.join(invalid_categories)}")


def get_category_url(category: str) -> str:
    """
    Retorna a URL da categoria. 
    """
    return f"{base_url}?cl={categories[unidecode_categories[unidecode(category.lower())]]}"


def get_pages_quantity(soup: BeautifulSoup) -> int:
    """
    Retorna a quantidade de páginas de eventos.
    """
    soup_pages = soup.find("div", { "class": "zbqpbg3"}).find("p", { "class": "_1ejln952 _1ejln953"})
    end = re.search(r"\d+$", soup_pages.text).group()
    return int(end)


def get_event_info(soup: BeautifulSoup, category: str) -> list[dict]:
    """
    Retorna informações sobre os eventos.
    """
    events = []
    for event in soup.find_all("a", { "class": "sympla-card pn67h10 pn67h11"}):
        event_info = {
            "category": category,
            "title": event.find("h3", { "class": "pn67h18"}).text,
            "local": event.find("p", { "class": "pn67h1a"}).text,
            "date": event.find("div", { "class": "qtfy413 qtfy414"}).text,
            "link": event.get('href')
        }
        events.append(event_info)

    return events

def get_event_info_by_category(category: str) -> dict:
    """
    Retorna informações sobre os eventos de uma categoria.   
    """
    url = get_category_url(category)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    pages_quantity = get_pages_quantity(soup)
    events = get_event_info(soup, category)
    
    for page in range(2, pages_quantity + 1):
        print(f"Buscando eventos da página {page}/{pages_quantity} na categoria {category}...")
        response = requests.get(f"{url}&page={page}")
        soup = BeautifulSoup(response.text, "html.parser")
        events.extend(get_event_info(soup, category))
        time.sleep(0.5)
    
    return events


def get_event_info_by_categories(categories: list[str]) -> list[dict]:
    """
    Retorna informações sobre os eventos de várias categorias.
    """
    check_all_categories(categories)
    events = []
    for category in categories:
        print(f"Buscando eventos da categoria {category}...")
        events.extend(get_event_info_by_category(category))

    return events


def read_input_file(file_path: Path) -> list[str]:
    """
    Lê o arquivo de entrada no formato csv.
    """
    
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo {file_path} não encontrado.")
    
    df = pd.read_csv(file_path)
    return df["Categorias"].tolist()


def write_output_file(file_path: Path, data: list[dict]) -> None:
    """
    Escreve o arquivo de saída no formato csv.
    """
    df = pd.DataFrame(data, columns=["category", "title", "local", "date", "link"])
    df.to_csv(file_path, index=False)


if __name__ == "__main__":
    categories_list = read_input_file(input_file_path)

    print("Buscando eventos...")
    events = get_event_info_by_categories(categories_list)

    print("Eventos encontrados!")
    write_output_file(output_file_path, events)

    print(f"Arquivo {output_file_path} criado com sucesso!")