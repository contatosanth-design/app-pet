import streamlit as st
import pandas as pd
from datetime import datetime
import os
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA (MODO AMPLO E TEMA)
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide", page_icon="🐾")

# 2. ESTILO CSS ADAPTÁVEL (MODO CLARO E ESCURO)
st.markdown("""
    <style>
    /* Fontes e Tamanhos (Profissional Desktop) */
    html, body, [class*="css"] { 
        font-size: 0.90rem !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }
    
    /* COR DO TÍTULO PRINCIPAL (Neon Green para Modo Escuro, Verde Medicinal para Claro) */
    .main-title {
        color: #00E676; /* Neon Green - Funciona bem no Dark */
        font-size: 2.3rem !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 25px;
    }
    [data-theme="light"] .main-title { color: #2E7D32; } /* Verde Medicinal - Para
