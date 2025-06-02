import tkinter as tk

# Função para analisar sintomas e recomendar ação
def analisar():
    sintomas = []
    if tosse_var.get(): sintomas.append("Tosse")
    if febre_var.get(): sintomas.append("Febre")
    if dor_var.get(): sintomas.append("Dor no corpo")
    if respiracao_var.get(): sintomas.append("Dificuldade para respirar")

    if "Dificuldade para respirar" in sintomas or ("Febre" in sintomas and "Tosse" in sintomas):
        resultado = "Risco alto: procure atendimento médico imediatamente."
    elif len(sintomas) >= 2:
        resultado = "Risco moderado: monitore os sintomas e, se persistirem, procure atendimento."
    elif len(sintomas) == 1:
        resultado = "Risco leve: repouse e continue observando os sintomas."
    else:
        resultado = "Nenhum sintoma relevante informado."

    resultado_label.config(text=resultado)

# Interface principal
root = tk.Tk()
root.title("Triagem de Saúde - Protótipo v1")
root.geometry("480x400")

# Título
title = tk.Label(root, text="Triagem de Sintomas", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Instrução
instrucao = tk.Label(root, text="Marque os sintomas apresentados:", font=("Arial", 12))
instrucao.pack(pady=5)

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
tk.Button(root, text="Analisar", command=analisar, font=("Arial", 12), bg="#007ACC", fg="white").pack(pady=15)

# Resultado
resultado_label = tk.Label(root, text="", font=("Arial", 12), fg="blue", wraplength=450)
resultado_label.pack(pady=10)

# Iniciar a interface
root.mainloop()
