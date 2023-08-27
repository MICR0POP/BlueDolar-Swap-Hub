#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import requests

class EnhancedCurrencyConverter(wx.Frame):
    def __init__(self, parent, title):
        super(EnhancedCurrencyConverter, self).__init__(parent, title=title, size=(600, 350))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Dropdown for source and target currencies
        self.currencies = ["Pesos Argentino", "Dólar Blue Argentino", "Dólar Estadounidense", "Pesos Mexicano", "Colón Costarricense", "Pesos Colombiano"]
        self.source_currency_dropdown = wx.Choice(panel, choices=self.currencies)
        self.target_currency_dropdown = wx.Choice(panel, choices=self.currencies)
        self.source_currency_dropdown.SetSelection(0)
        self.target_currency_dropdown.SetSelection(1)
        
        hbox_currency = wx.BoxSizer(wx.HORIZONTAL)
        hbox_currency.Add(self.source_currency_dropdown, flag=wx.RIGHT, border=10)
        
        self.swap_btn = wx.Button(panel, label="⇄")
        self.swap_btn.Bind(wx.EVT_BUTTON, self.swap_currencies)
        hbox_currency.Add(self.swap_btn, flag=wx.RIGHT, border=10)
        
        hbox_currency.Add(self.target_currency_dropdown)
        vbox.Add(hbox_currency, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Entry for amount
        hbox_amount = wx.BoxSizer(wx.HORIZONTAL)
        self.amount_label = wx.StaticText(panel, label="Monto:")
        self.amount_entry = wx.TextCtrl(panel, size=(200,-1))  # Increased the size of the TextCtrl
        self.paste_btn = wx.Button(panel, label="Pegar")
        self.paste_btn.Bind(wx.EVT_BUTTON, self.paste_from_clipboard)
        
        hbox_amount.Add(self.amount_label, flag=wx.RIGHT, border=10)
        hbox_amount.Add(self.amount_entry, flag=wx.RIGHT, border=10)
        hbox_amount.Add(self.paste_btn)
        
        vbox.Add(hbox_amount, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Conversion buttons
        self.btn_convert = wx.Button(panel, label="Convertir")
        self.btn_convert.Bind(wx.EVT_BUTTON, self.convert_currency)
        vbox.Add(self.btn_convert, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # List for history
        self.history_list = wx.ListBox(panel, size=(500, 125))
        vbox.Add(self.history_list, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Copy result button
        self.copy_btn = wx.Button(panel, label="Copiar resultado")
        self.copy_btn.Bind(wx.EVT_BUTTON, self.copy_result_to_clipboard)
        vbox.Add(self.copy_btn, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        # Button to clear history
        self.btn_clear_history = wx.Button(panel, label="Borrar Historial")
        self.btn_clear_history.Bind(wx.EVT_BUTTON, self.clear_history)
        vbox.Add(self.btn_clear_history, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        panel.SetSizer(vbox)

    
    def fetch_exchange_rate(self, from_currency, to_currency):
        currency_map = {
            "Pesos Argentino": "ars",
            "Dólar Blue Argentino": "ars_pa",
            "Dólar Estadounidense": "usd",
            "Pesos Mexicano": "mxn",
            "Colón Costarricense": "crc",
            "Pesos Colombiano": "clp"
        }
        from_code = currency_map[from_currency]
        to_code = currency_map[to_currency]
        
        # URL endpoint
        url = f"https://api.cuex.com/v1/exchanges/{from_code}/statistic?to_currency={to_code}"

        # Headers
        headers = {
            "authorization": "799c58e5fc2281c1149f2ade67f35f6c",
            "origin": "https://cuex.com",
            "referer": "https://cuex.com/"
        }

        # Make the API call
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json().get('data').get('latest_rate')
        else:
            return None

    def convert_currency(self, event):
        source_currency = self.source_currency_dropdown.GetStringSelection()
        target_currency = self.target_currency_dropdown.GetStringSelection()
        amount = float(self.amount_entry.GetValue())
        
        rate = self.fetch_exchange_rate(source_currency, target_currency)
        if rate:
            converted_value = amount * rate
            result = f"{amount} {source_currency} es igual a {converted_value:.2f} {target_currency}"
            self.history_list.Append(result)
            self.last_result = result
        else:
            wx.MessageBox("Error al obtener la tasa de cambio.", "Error", wx.ICON_ERROR)

    def swap_currencies(self, event):
        source_idx = self.source_currency_dropdown.GetSelection()
        target_idx = self.target_currency_dropdown.GetSelection()
        self.source_currency_dropdown.SetSelection(target_idx)
        self.target_currency_dropdown.SetSelection(source_idx)

    def copy_result_to_clipboard(self, event):
        wx.TheClipboard.Open()
        # Extraer solo el valor del resultado
        result_value = self.last_result.split("es igual a ")[1].split()[0]
        wx.TheClipboard.SetData(wx.TextDataObject(result_value))
        wx.TheClipboard.Close()


    def paste_from_clipboard(self, event):
        wx.TheClipboard.Open()
        clipboard_data = wx.TextDataObject()
        wx.TheClipboard.GetData(clipboard_data)
        wx.TheClipboard.Close()
        self.amount_entry.SetValue(clipboard_data.GetText())

    def clear_history(self, event):
        self.history_list.Clear()

if __name__ == "__main__":
    app = wx.App()
    EnhancedCurrencyConverter(None, title="BlueDolar Swap Hub - Micropop")
    app.MainLoop()
