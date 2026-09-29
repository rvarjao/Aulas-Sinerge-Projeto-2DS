from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import servicos_disponiveis as catalogo
from validators import converter_preco

catalogo_bp = Blueprint("catalogo", __name__, url_prefix="/catalogo")


def _ler_formulario():
    nome = request.form["nome"].strip()
    preco = converter_preco(request.form["preco"])
    descricao = request.form["descricao"].strip()
    return nome, preco, descricao


@catalogo_bp.route("/")
def listar():
    return render_template(
        "catalogo/lista.html", itens=catalogo.listar_servicos_disponiveis()
    )


@catalogo_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome, preco, descricao = _ler_formulario()

        if not nome or preco is None:
            flash("Informe o nome e um preço válido.", "danger")
            return render_template("catalogo/form.html", item=request.form)

        if not catalogo.criar_servico_disponivel(nome, preco, descricao):
            flash("Já existe um serviço com este nome.", "danger")
            return render_template("catalogo/form.html", item=request.form)

        flash("Serviço adicionado ao catálogo.", "success")
        return redirect(url_for("catalogo.listar"))

    return render_template("catalogo/form.html", item=None)


@catalogo_bp.route("/<int:item_id>/editar", methods=["GET", "POST"])
def editar(item_id):
    item = catalogo.buscar_servico_disponivel(item_id)
    if item is None:
        flash("Serviço não encontrado.", "danger")
        return redirect(url_for("catalogo.listar"))

    if request.method == "POST":
        nome, preco, descricao = _ler_formulario()

        if not nome or preco is None:
            flash("Informe o nome e um preço válido.", "danger")
            return render_template("catalogo/form.html", item=request.form)

        if not catalogo.atualizar_servico_disponivel(item_id, nome, preco, descricao):
            flash("Já existe um serviço com este nome.", "danger")
            return render_template("catalogo/form.html", item=request.form)

        flash("Serviço atualizado com sucesso.", "success")
        return redirect(url_for("catalogo.listar"))

    return render_template("catalogo/form.html", item=item)


@catalogo_bp.route("/<int:item_id>/excluir", methods=["POST"])
def excluir(item_id):
    if catalogo.excluir_servico_disponivel(item_id):
        flash("Serviço removido do catálogo.", "success")
    else:
        flash("Não é possível excluir: este serviço já foi realizado.", "danger")
    return redirect(url_for("catalogo.listar"))
