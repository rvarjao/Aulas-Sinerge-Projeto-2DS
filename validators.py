def converter_preco(texto):
    """Converte '25,50' ou '25.50' em float. Retorna None se for inválido."""
    try:
        valor = float(texto.strip().replace(",", "."))
    except ValueError:
        return None
    return valor if valor >= 0 else None
