import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt

# Função para analisar sintomas e recomendar ação
def analisar():
    nome = nome_entry.get()
    idade = idade_entry.get()

    if not nome or not idade:
        messagebox.showwarning("Campos obrigatórios", "Por favor, preencha o nome e a idade.")
        return

    sintomas = []
    if tosse_var.get(): sintomas.append("Tosse")
    if febre_var.get(): sintomas.append("Febre")
    if dor_var.get(): sintomas.append("Dor no corpo")
    if respiracao_var.get(): sintomas.append("Dificuldade para respirar")

    if "Dificuldade para respirar" in sintomas or ("Febre" in sintomas and "Tosse" in sintomas):
        resultado = "Risco alto: procure atendimento médico imediatamente."
        cor = "red"
    elif len(sintomas) >= 2:
        resultado = "Risco moderado: monitore os sintomas e, se persistirem, procure atendimento."
        cor = "orange"
    elif len(sintomas) == 1:
        resultado = "Risco leve: repouse e continue observando os sintomas."
        cor = "green"
    else:
        resultado = "Nenhum sintoma relevante informado."
        cor = "gray"

    salvar_historico_paciente(nome, idade, sintomas, resultado)
    total = contar_triagens(nome)

    resultado_label.config(text=resultado, fg=cor)
    contador_label.config(text=f"Triagens anteriores: {total}")

# Função para salvar os dados
def salvar_historico_paciente(nome, idade, sintomas, resultado):
    nome_formatado = nome.lower().replace(" ", "_")
    nome_arquivo = f"historico_{nome_formatado}.csv"

    cabecalho = ["Data/Hora", "Nome", "Idade", "Sintomas", "Resultado"]
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    novo_registro = [data, nome, idade, ", ".join(sintomas), resultado]

    criar_cabecalho = not os.path.exists(nome_arquivo)
    with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if criar_cabecalho:
            writer.writerow(cabecalho)
        writer.writerow(novo_registro)

# Contador de triagens
def contar_triagens(nome):
    nome_formatado = nome.lower().replace(" ", "_")
    nome_arquivo = f"historico_{nome_formatado}.csv"
    if not os.path.exists(nome_arquivo):
        return 0
    with open(nome_arquivo, mode="r", encoding="utf-8") as file:
        linhas = file.readlines()
        return len(linhas) - 1 if len(linhas) > 1 else 0

# Gráfico com matplotlib
def ver_grafico():
    nome = nome_entry.get()
    if not nome:
        messagebox.showwarning("Campo obrigatório", "Preencha o nome do paciente para gerar o gráfico.")
        return

    nome_formatado = nome.lower().replace(" ", "_")
    nome_arquivo = f"historico_{nome_formatado}.csv"

    if not os.path.exists(nome_arquivo):
        messagebox.showinfo("Histórico não encontrado", f"Nenhum histórico encontrado para {nome}.")
        return

    sintomas_freq = {"Tosse": 0, "Febre": 0, "Dor no corpo": 0, "Dificuldade para respirar": 0}
    with open(nome_arquivo, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for linha in reader:
            for sintoma in sintomas_freq:
                if sintoma in linha["Sintomas"]:
                    sintomas_freq[sintoma] += 1

    plt.figure(figsize=(7, 4))
    plt.bar(sintomas_freq.keys(), sintomas_freq.values(), color=['#3498db', '#f1c40f', '#e67e22', '#e74c3c'])
    plt.title(f"Frequência de sintomas - {nome}", fontsize=14)
    plt.xlabel("Sintomas")
    plt.ylabel("Ocorrências")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

# Interface principal
root = tk.Tk()
root.title("Triagem de Saúde - Versão 7")
root.configure(bg="#f2f2f2")
root.geometry("500x580")

# Título estilizado
title = tk.Label(root, text="Triagem de Sintomas", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#f2f2f2")
title.pack(pady=10)

# Campos de entrada
form_frame = tk.Frame(root, bg="#f2f2f2")
form_frame.pack(pady=5)

# Nome
tk.Label(form_frame, text="Nome do paciente:", font=("Arial", 11), bg="#f2f2f2").grid(row=0, column=0, sticky="w")
nome_entry = tk.Entry(form_frame, width=35)
nome_entry.grid(row=1, column=0, padx=5, pady=3)

# Idade
tk.Label(form_frame, text="Idade:", font=("Arial", 11), bg="#f2f2f2").grid(row=2, column=0, sticky="w")
idade_entry = tk.Entry(form_frame, width=10)
idade_entry.grid(row=3, column=0, padx=5, pady=3)

# Instrução e sintomas
tk.Label(root, text="Marque os sintomas apresentados:", font=("Arial", 12), bg="#f2f2f2").pack(pady=(15, 5))

check_frame = tk.Frame(root, bg="#f2f2f2")
check_frame.pack(pady=5)

# Variáveis dos sintomas
tosse_var = tk.BooleanVar()
febre_var = tk.BooleanVar()
dor_var = tk.BooleanVar()
respiracao_var = tk.BooleanVar()

# Checkboxes
tk.Checkbutton(check_frame, text="Tosse", variable=tosse_var, font=("Arial", 11), bg="#f2f2f2").pack(anchor="w")
tk.Checkbutton(check_frame, text="Febre", variable=febre_var, font=("Arial", 11), bg="#f2f2f2").pack(anchor="w")
tk.Checkbutton(check_frame, text="Dor no corpo", variable=dor_var, font=("Arial", 11), bg="#f2f2f2").pack(anchor="w")
tk.Checkbutton(check_frame, text="Dificuldade para respirar", variable=respiracao_var, font=("Arial", 11), bg="#f2f2f2").pack(anchor="w")

# Botões principais
btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Analisar", command=analisar, font=("Arial", 12), bg="#2ecc71", fg="white", padx=20).pack(pady=5)
tk.Button(btn_frame, text="Ver Gráfico", command=ver_grafico, font=("Arial", 12), bg="#3498db", fg="white", padx=20).pack()

# Resultado
resultado_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f2f2f2", wraplength=450)
resultado_label.pack(pady=10)

# Contador
contador_label = tk.Label(root, text="", font=("Arial", 11, "italic"), fg="#2c3e50", bg="#f2f2f2")
contador_label.pack()

# Iniciar a interface
root.mainloop()