import re
import json

def load_input_from_file(file_path):
    """Função para carregar o conteúdo do arquivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as error:
        raise RuntimeError(f"Erro ao ler o arquivo: {error}")

def extract_events(input_text):
    """Função para extrair todos os eventos."""
    usecase_pattern = re.compile(
        r"usecase\s+(\w+)\s*{\s*name:\s*\"([^\"]+)\"\s*.*?description:\s*\"([^\"]+)\"\s*.*?performer:\s*(\w+)\s*.*?(event.*?})\s*}",
        re.DOTALL
    )
    event_pattern = re.compile(
        r"event\s+(\w+)\s*{\s*name:\s*\"([^\"]+)\"\s*.*?description:\s*\"([^\"]+)\"\s*.*?action:\s*\"([^\"]+)\"\s*}",
        re.DOTALL
    )

    events = []

    for usecase_match in usecase_pattern.finditer(input_text):
        events_block = usecase_match.group(5)

        for event_match in event_pattern.finditer(events_block):
            event_id = event_match.group(1)
            event_name = event_match.group(2)
            event_description = event_match.group(3)
            event_action = event_match.group(4).strip()

            events.append({
                "event_id": event_id,
                "name": event_name,
                "description": event_description,
                "action": event_action
            })

    return events

# Caminho para o arquivo de entrada

def get_events(file_path: str):
    input_text = load_input_from_file(file_path)
    events = extract_events(input_text)
    return events