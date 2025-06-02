import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os

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

    resultado_label.config(text=resultado, fg=cor)
    salvar_historico_paciente(nome, idade, sintomas, resultado)

# Função para salvar os dados em CSV separado por paciente
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

# Interface principal
root = tk.Tk()
root.title("Triagem de Saúde - Versão 4")
root.geometry("500x520")

# Título
title = tk.Label(root, text="Triagem de Sintomas", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Nome
tk.Label(root, text="Nome do paciente:", font=("Arial", 11)).pack(anchor="w", padx=20)
nome_entry = tk.Entry(root, width=40)
nome_entry.pack(padx=20, pady=5)

# Idade
tk.Label(root, text="Idade:", font=("Arial", 11)).pack(anchor="w", padx=20)
idade_entry = tk.Entry(root, width=10)
idade_entry.pack(padx=20, pady=5)

# Instrução
tk.Label(root, text="Marque os sintomas apresentados:", font=("Arial", 12)).pack(pady=10)

# Variáveis dos sintomas
tosse_var = tk.BooleanVar()
febre_var = tk.BooleanVar()
dor_var = tk.BooleanVar()
respiracao_var = tk.BooleanVar()

# Checkboxes
tk.Checkbutton(root, text="Tosse", variable=tosse_var, font=("Arial", 11)).pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Febre", variable=febre_var, font=("Arial", 11)).pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Dor no corpo", variable=dor_var, font=("Arial", 11)).pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Dificuldade para respirar", variable=respiracao_var, font=("Arial", 11)).pack(anchor="w", padx=20)

# Botão para análise
tk.Button(root, text="Analisar", command=analisar, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=15)

# Resultado
resultado_label = tk.Label(root, text="", font=("Arial", 12), fg="blue", wraplength=450)
resultado_label.pack(pady=10)

# Iniciar a interface
root.mainloop()
