#!/usr/bin/env python
import click
from mlib import predict, retrain
import json
import pandas as pd


@click.group()
@click.version_option("1.0")
def cli():
    """Machine Learning Utility Belt"""


@cli.command("retrain")
@click.option("--tsize", default=0.3, help="Test Size")
def retraincli(tsize):
    """Retrain Model
    You may want to extend this with more options, such as setting model_name
    """

    click.echo(click.style(f"Retraining Model, tsize: {tsize}", bg="green", fg="black"))
    f1_value, model_name = retrain(tsize=tsize)
    click.echo(
        click.style(f"Retrained Model F1 score: {f1_value}", bg="blue", fg="black")
    )
    click.echo(click.style(f"Retrained Model Name: {model_name}", bg="red", fg="black"))


payload_default = """
[{"edad": 25,
  "montoSolicitado": 30000,
  "montoOtorgado": 23000,
  "genero": "Hombre",
  "quincenal": 1,
  "dependientesEconomicos": 3,
  "nivelEstudio": "Universidad",
  "fico": 569,
  "ingresosMensuales": 15000,
  "gastosMensuales": 4500,
  "emailScore": 0,
  "browser": "CHROME_MOBILE",
  "NUMTDC_AV": 0}]
  """


@cli.command("predict")
@click.option(
    "--perfil",
    default=payload_default,
    prompt="Users perfil",
    help="Pass the perfil of a user to predict if is a default",
)
def predictcli(perfil):
    """predict if is a default based on perfil"""
    data_to_predict = json.loads(perfil)
    data_to_predict = pd.DataFrame(data_to_predict)

    result = predict(data_to_predict)
    pred_class = result["Type_user"]
    if pred_class == "Moroso":
        click.echo(click.style(result, bg="red", fg="black"))
    else:
        click.echo(click.style(result, bg="green", fg="black"))


if __name__ == "__main__":
    cli()

# Example
# python cli.py predict --perfil '
# [{\"edad\": 25,
# \"montoSolicitado\": 30000,
# \"montoOtorgado\": 23000,
# \"genero\": \"Hombre\",
# \"quincenal\": 1,
# \"dependientesEconomicos\": 3,
# \"nivelEstudio\": \"Universidad\",
# \"fico\": 569,
# \"ingresosMensuales\": 15000,
# \"gastosMensuales\": 4500,
# \"emailScore\": 0,
# \"browser\": \"CHROME_MOBILE\",
# \"NUMTDC_AV\": 0}]'
#
# python cli.py predict --perfil '
# [{\"edad\": 30,
# \"montoSolicitado\": 20000,
# \"montoOtorgado\": 40000,
# \"genero\": \"Hombre\",
# \"quincenal\": 1,
# \"dependientesEconomicos\": 0,
# \"nivelEstudio\": \"Universidad\",
# \"fico\": 569,
# \"ingresosMensuales\": 25000,
# \"gastosMensuales\": 15000,
# \"emailScore\": 1,
# \"browser\": \"CHROME_MOBILE\",
# \"NUMTDC_AV\": 0}]'
