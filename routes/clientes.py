from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import clientes

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@clientes_bp.route("/")
def listar():
    return render_template("clientes/lista.html", clientes=clientes.listar_clientes())


@clientes_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        telefone = request.form["telefone"].strip()
        email = request.form["email"].strip().lower()

        if not nome:
            flash("Informe o nome do cliente.", "danger")
            return render_template("clientes/form.html", cliente=request.form)

        clientes.criar_cliente(nome, telefone, email)
        flash("Cliente cadastrado com sucesso.", "success")
        return redirect(url_for("clientes.listar"))

    return render_template("clientes/form.html", cliente=None)


@clientes_bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar(cliente_id):
    cliente = clientes.buscar_cliente(cliente_id)
    if cliente is None:
        flash("Cliente não encontrado.", "danger")
        return redirect(url_for("clientes.listar"))

    if request.method == "POST":
        nome = request.form["nome"].strip()
        telefone = request.form["telefone"].strip()
        email = request.form["email"].strip().lower()

        if not nome:
            flash("Informe o nome do cliente.", "danger")
            return render_template("clientes/form.html", cliente=request.form)

        clientes.atualizar_cliente(cliente_id, nome, telefone, email)
        flash("Cliente atualizado com sucesso.", "success")
        return redirect(url_for("clientes.listar"))

    return render_template("clientes/form.html", cliente=cliente)


@clientes_bp.route("/<int:cliente_id>/excluir", methods=["POST"])
def excluir(cliente_id):
    if clientes.excluir_cliente(cliente_id):
        flash("Cliente excluído.", "success")
    else:
        flash("Não é possível excluir: o cliente possui veículos cadastrados.", "danger")
    return redirect(url_for("clientes.listar"))
