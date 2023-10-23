# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 06:54:54 2023

@author: VP
"""

from SENHA_API import API_KEY
from chat_context import GPT_prompt
from luxa_context import LUXA_prompt
import openai
import os
import sys
import logging
import PySimpleGUI as sg

# Salvando a chave da API por segurança
openai.api_key = f"{API_KEY}"
models = ["gpt-3.5-turbo"]
max_tokens_list = [320, 962, 1925, 3850]

logger = logging.getLogger()

def select_max_tokens(max_tokens):
    return max_tokens if max_tokens in max_tokens_list else ValueError(f"Tokens inválidos: {max_tokens}. Deve estar entre: {max_tokens_list}")

def make_window(theme):
    sg.theme(theme)
    # GUI layout.
    layout = [
        #[sg.Image(data="pitch.png")],
        [sg.Text("ChatPofexô",  expand_x=True, justification="center",
                 font=("Helvetica", 13), relief=sg.RELIEF_RIDGE)],
        [sg.TabGroup([[
            sg.Tab("OpenAi", [
                [sg.Radio("Quantidade máxima de tokens", "RADIO1", key="select_max_tokens"), sg.Combo(
                    max_tokens_list, default_value=max_tokens_list[0], key="-MAXTOKENS-", readonly=True)],
                [sg.Text("Digite abaixo:",
                         font=('_ 13'))],
                [sg.Pane([sg.Column([[sg.Multiline(key="prompt", size=(77, 20), expand_x=True, expand_y=True, enter_submits=True, focus=True)]]),
                          sg.Column([[sg.Multiline(size=(60, 15), key="-OUTPUT-", font=("Arial", 9), expand_x=True, expand_y=True, write_only=True,
                                                   reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]])], expand_x=True, expand_y=True)],
                [sg.Button("Responder", bind_return_key=True), sg.Button('Abrir arquivo'), sg.Button("Limpar chat"), sg.Button("Sair")]]),
            sg.Tab("Prof Luxa", [
                [sg.Radio("Quantidade máxima de tokens", "RADIO1", key="select_max_tokens"), sg.Combo(
                    max_tokens_list, default_value=max_tokens_list[0], key="-MAXTOKENS-", readonly=True)],
                [sg.Text("Fale com o professor Luxemburgo:",
                         font=('_ 13'))],
                [sg.Pane([sg.Column([[sg.Multiline(key="lprompt", size=(77, 20), expand_x=True, expand_y=True, enter_submits=True, focus=True)]]),
                          sg.Column([[sg.Multiline(size=(60, 15), key="-LOUTPUT-", font=("Arial", 9), expand_x=True, expand_y=True, write_only=True,
                                                   reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]])], expand_x=True, expand_y=True)],
                #[sg.Button("Resposta do Luxa", bind_return_key=True), sg.Button('Abrir arquivo'), sg.Button("Limpar chat"), sg.Button("Sair")]]),
                [sg.Button("Resposta do Luxa", bind_return_key=True), sg.Button('Abrir arquivo'), sg.Button("Limpar Luxa"), sg.Button("Sair")]]),
            sg.Tab("Tema", [
                [sg.Text("Escolha o tema:")],
                [sg.Listbox(values=sg.theme_list(), size=(
                    20, 12), key="-THEME LISTBOX-", enable_events=True)],
                [sg.Button("Escolha o tema")]]),
            sg.Tab("Sobre", [
                [sg.Text(
                    "Programa desenvolvido para fins acadêmicos por Victor Hugo e Eduardo.")],
                [sg.Text(
                    "Usa-se nesse programa as tecnologias:")],
                [sg.Text(
                    "-API da OpenAi")],
                [sg.Text(
                    "-OpenAiGUI do Github: https://github.com/MaxSSD/OpenAI-GUI")]
                ])
            ]], key="-TAB GROUP-", expand_x=True, expand_y=True),
         sg.Sizegrip()]]
    # Gui window and layout sizing.
    window = sg.Window('OpenAI GUI', layout, resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, finalize=True,
                       icon=r'D:\Downloads\Unicarioca - Victor\TCC - Victor\Python\TCC 2023.2\icons\L_logo_48x48.ico', )
    window.set_min_size(window.size)
    return window


def chatbot(u_message, tokens):
  # Respondendo, aguarde....
  sg.popup_quick_message('Respondendo, aguarde...')

  
  # Adicionando o contexto ao chat, para ter certeza que ele não sairá do assunto destinado
  api_message = [
      {"role": "system", "content": f"Esse é você: {GPT_prompt}"},
      {"role": "user", "content": u_message},
      {"role": "assistant", "content": "Eu entendo, falarei como um assistente de dados avançados de futebol."}
      ]
  
  # Criando a requisição da resposta
  chat = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=api_message,
      max_tokens=tokens)

  # Coletando a resposta
  result = chat['choices'][0]['message']['content']
  
  # Printando a resposta para o usuário
  print(result)
  logger.info(result)
  
  # Sempre salvando o resultado no histório
  with open('respostas.txt', 'a+') as f:
      f.write(result)

  sg.clipboard_set(result)

# Bot do professor Luxa
def luxabot(u_message, tokens):
  # Respondendo, aguarde....
  sg.popup_quick_message('Respondendo, aguarde...')
  
  # Adicionando o contexto ao chat, para ter certeza que ele não sairá do assunto destinado
  api_message = [
      {"role": "system", "content": f"Esse é você: {LUXA_prompt}"},
      {"role": "user", "content": u_message},
      {"role": "assistant", "content": "Eu entendo, falarei como o técnico Vanderlei Luxemburgo."}
      ]
  
  # Criando a requisição da resposta
  chat = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=api_message,
      max_tokens=tokens)

  # Coletando a resposta
  lresult = chat['choices'][0]['message']['content']
  
  # Printando a resposta para o usuário
  print(lresult)
  logger.info(lresult)
  
  # Sempre salvando o resultado no histório
  with open('respostas.txt', 'a+') as f:
      f.write(lresult)

  sg.clipboard_set(lresult)

# Interface para interagir com usuário
def main():
    window = make_window(sg.theme())
    # background_layout = [[sg.Image(r'icons\pitch.png')]]
    # window_background = sg.Window('Background',background_layout, no_titlebar=True, finalize=True, margins=(0,0),
    #                               element_padding=(0,0), right_click_menu=[[''],['Exit',]])
    # window_background['-C-'].expand(True, False, False)
    
    while True:
        event, values = window.read(timeout=None)
        if event == sg.WINDOW_CLOSED or event == 'Sair' or event == 'Exit':
            break
        if values is not None:
            max_tokens = values['-MAXTOKENS-'] if values['-MAXTOKENS-'] == 'Quantidade máxima de tokens' else values['-MAXTOKENS-']
        if event == 'Responder':
            prompt_in = values['prompt'].rstrip()
            window['prompt'].update(prompt_in)
            window['-OUTPUT-'].update('')
            window['-LOUTPUT-'].update('')
            chatbot(prompt_in, max_tokens)
        elif event == 'Resposta do Luxa':
            prompt_inn = values['lprompt'].rstrip()
            window['lprompt'].update(prompt_inn)
            window['-OUTPUT-'].update('')
            window['-LOUTPUT-'].update('')
            luxabot(prompt_inn, max_tokens)
        elif event == 'Abrir arquivo':
            os.startfile('respostas.txt', 'open')
        elif event == 'Limpar chat':
            window['prompt'].update('')
            window["-OUTPUT-"].update('')
            # window['lprompt'].update('')
            # window['-LOUTPUT-'].update('')
        elif event == 'Limpar Luxa':
            window['lprompt'].update('')
            window['-LOUTPUT-'].update('')
        elif event == "Escolha o tema":
            theme_chosen = values['-THEME LISTBOX-'][0]
            window.close()
            window = make_window(theme_chosen)
            sg.user_settings_set_entry('-theme-', theme_chosen)
            sg.popup(f"Chosen Theme: {str(theme_chosen)}", keep_on_top=True)

        if event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Version':
            sg.popup_scrolled(__file__, sg.get_versions(
            ), location=window.current_location(), keep_on_top=True, non_blocking=True)

    window.close()
    sys.exit(0)

# Chamando a função principal
if __name__ == "__main__":
  # background_image = "icons\pitch.png"
  main()
