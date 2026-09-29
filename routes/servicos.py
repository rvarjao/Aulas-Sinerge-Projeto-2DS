from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import catalogo, servicos, veiculos
from validators import converter_preco

servicos_bp = Blueprint("servicos", __name__, url_prefix="/servicos")


def _form(servico):
    # O formulário precisa dos veículos e do catálogo para os campos de seleção.
    return render_template(
        "servicos/form.html",
        servico=servico,
        veiculos=veiculos.listar_veiculos(),
        catalogo=catalogo.listar_itens(),
        hoje=date.today().isoformat(),
    )


def _ler_formulario():
    """Retorna os dados validados ou None (já com flash de erro)."""
    veiculo_id = request.form.get("veiculo_id", type=int)
    item_id = request.form.get("catalogo_id", type=int)
    data = request.form["data"].strip()
    observacao = request.form["observacao"].strip()

    item = catalogo.buscar_item(item_id) if item_id else None
    if not veiculo_id or item is None or not data:
        flash("Informe veículo, serviço e data.", "danger")
        return None

    # Preço em branco: usa o preço atual do catálogo.
    texto_preco = request.form["preco"].strip()
    preco = converter_preco(texto_preco) if texto_preco else item["preco"]
    if preco is None:
        flash("Informe um preço válido.", "danger")
        return None

    return veiculo_id, item_id, preco, data, observacao


@servicos_bp.route("/")
def listar():
    itens = servicos.listar_servicos()
    total = sum(item["preco"] for item in itens)
    return render_template("servicos/lista.html", servicos=itens, total=total)


@servicos_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        dados = _ler_formulario()
        if dados is None:
            return _form(request.form)

        servicos.criar_servico(*dados)
        flash("Serviço registrado com sucesso.", "success")
        return redirect(url_for("servicos.listar"))

    return _form(None)


@servicos_bp.route("/<int:servico_id>/editar", methods=["GET", "POST"])
def editar(servico_id):
    servico = servicos.buscar_servico(servico_id)
    if servico is None:
        flash("Serviço não encontrado.", "danger")
        return redirect(url_for("servicos.listar"))

    if request.method == "POST":
        dados = _ler_formulario()
        if dados is None:
            return _form(request.form)

        servicos.atualizar_servico(servico_id, *dados)
        flash("Serviço atualizado com sucesso.", "success")
        return redirect(url_for("servicos.listar"))

    return _form(servico)


@servicos_bp.route("/<int:servico_id>/excluir", methods=["POST"])
def excluir(servico_id):
    servicos.excluir_servico(servico_id)
    flash("Serviço excluído.", "success")
    return redirect(url_for("servicos.listar"))
