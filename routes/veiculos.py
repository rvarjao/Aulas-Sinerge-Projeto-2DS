from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import clientes, veiculos

veiculos_bp = Blueprint("veiculos", __name__, url_prefix="/veiculos")


def _form(veiculo):
    # O formulário precisa da lista de clientes para o campo de seleção.
    return render_template(
        "veiculos/form.html", veiculo=veiculo, clientes=clientes.listar_clientes()
    )


def _ler_formulario():
    cliente_id = request.form.get("cliente_id", type=int)
    placa = request.form["placa"].strip().upper()
    modelo = request.form["modelo"].strip()
    cor = request.form["cor"].strip()
    return cliente_id, placa, modelo, cor


@veiculos_bp.route("/")
def listar():
    return render_template("veiculos/lista.html", veiculos=veiculos.listar_veiculos())


@veiculos_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        cliente_id, placa, modelo, cor = _ler_formulario()

        if not cliente_id or not placa or not modelo:
            flash("Informe cliente, placa e modelo.", "danger")
            return _form(request.form)

        if not veiculos.criar_veiculo(cliente_id, placa, modelo, cor):
            flash("Esta placa já está cadastrada.", "danger")
            return _form(request.form)

        flash("Veículo cadastrado com sucesso.", "success")
        return redirect(url_for("veiculos.listar"))

    return _form(None)


@veiculos_bp.route("/<int:veiculo_id>/editar", methods=["GET", "POST"])
def editar(veiculo_id):
    veiculo = veiculos.buscar_veiculo(veiculo_id)
    if veiculo is None:
        flash("Veículo não encontrado.", "danger")
        return redirect(url_for("veiculos.listar"))

    if request.method == "POST":
        cliente_id, placa, modelo, cor = _ler_formulario()

        if not cliente_id or not placa or not modelo:
            flash("Informe cliente, placa e modelo.", "danger")
            return _form(request.form)

        if not veiculos.atualizar_veiculo(veiculo_id, cliente_id, placa, modelo, cor):
            flash("Esta placa já pertence a outro veículo.", "danger")
            return _form(request.form)

        flash("Veículo atualizado com sucesso.", "success")
        return redirect(url_for("veiculos.listar"))

    return _form(veiculo)


@veiculos_bp.route("/<int:veiculo_id>/excluir", methods=["POST"])
def excluir(veiculo_id):
    if veiculos.excluir_veiculo(veiculo_id):
        flash("Veículo excluído.", "success")
    else:
        flash("Não é possível excluir: o veículo possui serviços realizados.", "danger")
    return redirect(url_for("veiculos.listar"))
