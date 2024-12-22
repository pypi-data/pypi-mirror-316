#!/usr/bin/env python3
import csv
import os
import yaml # type: ignore
import json
import argparse

def list_git_projects():
    folders = os.listdir(".")
    output = []
    for f in folders:
        path = os.path.join(".", f)
        git_path = os.path.join(path, ".git")
        if os.path.isdir(path) and os.path.isdir(git_path):
            output.append(f)
    return output

def load_csv(arquivo_csv) -> list[list[str]]:
    try:
        with open(arquivo_csv, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            sheet = list(reader)
            return sheet
    except FileNotFoundError:
        exit(f"Arquivo '{arquivo_csv}' não encontrado.")

# count how many characters are in common in the beginning of two strings
def calc_name_collision(one, two) -> int:
    count = 0
    for i in range(min(len(one), len(two))):
        if one[i] == two[i]:
            count += 1
        else:
            break
    return count

def load_activities2(folder: str) -> dict[str, str]:
    path = os.path.join(folder, "poo", ".tko", "history.csv")
    data: dict[str, str] = {}
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            for line in lines:
                parts = line.split(",")
                hash = parts[0]
                timestamp = parts[1]
                action = parts[2]
                task = parts[3]
                payload = parts[4]
                if action == "TEST" and payload != "COMP":
                    if task not in data:
                        data[task] = payload
                    elif int(data[task]) < int(payload):
                        data[task] = payload

    fdata: dict[str, str] = {}
    for key in data:
        fdata[key] = f"{data[key]}:0:0:0"

    return fdata

def load_activities(folder: str) -> dict[str, str]:
    path = os.path.join(folder, "poo", ".tko", "repository.yaml")
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            return data["tasks"]
    except FileNotFoundError:
        print(f"Arquivo '{path}' não encontrado.")

    return {}

def get_autonomy_ability(value: int) -> tuple[int, int]:
        opts = [(0, 0), (1, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3), (4, 3), (3, 4), (4, 4)]
        return opts[value]

def decode_task(value: str, count: int) -> str:
    parts = value.split(":")
    if len(parts) != 3 and len(parts) != 4:
        return value
    if len(parts) == 3:
        coverage = parts[2].rjust(3, "0")
        autonomy, ability = get_autonomy_ability(int(parts[0]))
    if len(parts) == 4:
        coverage = parts[0].rjust(3, "0")
        autonomy = int(parts[1])
        ability = int(parts[2])
    count_str = str(count).rjust(3, "0")
    autonomy_str = ["x", "E", "D", "C", "B", "A"][autonomy]
    ability_str = ["x", "e", "d", "c", "b", "a"][ability]
    return f"{coverage}%{autonomy_str}{ability_str}{count_str}"
    

def get_count(folder: str, task: str):
    path = os.path.join(folder, "poo", ".tko", "track", task)
    if os.path.isdir(path):
        files = [x for x in os.listdir(path) if x.endswith("json")]
        for f in files:
            with open(os.path.join(path, f), "r", encoding="utf-8") as file:
                data = json.load(file)
                return len(data["patches"])
    return 0


def load_username_row(cut: int, pad: int, folder: str, header: list[str], task_pad) -> list[str]:
    tasks = load_activities(folder)
    print(f"{folder}: {tasks}")
    line = ["-" * task_pad for _ in header]
    line[0] = folder[cut:].ljust(pad)
    for i in range(1, len(header)):
        h = header[i].strip()
        if h in tasks:
            count = get_count(folder, h)
            line[i] = decode_task(tasks[h], count)
    return line

def main():
    # Caminho do arquivo CSV
    parser = argparse.ArgumentParser(description="Coleta de dados de atividades de programação.")
    parser.add_argument("--csv", help="Caminho do arquivo CSV.")
    parser.add_argument("--cut", "-c", type=int, help="quantidade de caracteres para cortar do nome")
    args = parser.parse_args()

    if not args.csv:
        arquivo_csv = "collect.csv"
    else:
        arquivo_csv = args.csv

    task_pad = 9
    folders = list_git_projects()
    collision = 0
    if args.cut:
        collision = args.cut
    usernames = [f[collision:] for f in folders]
    max_len = max([len(u) for u in usernames])
    sheet = load_csv(arquivo_csv)

    # apagar todas as linhas menos a primeira
    sheet = sheet[:1]
    header = sheet[0]
    for i, f in enumerate(folders):
        line = load_username_row(collision, max_len, f, header, task_pad)
        sheet.append(line)

    # salvar os dados
    with open(arquivo_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sheet)

    print(f"Dados salvos no arquivo '{arquivo_csv}'.")
