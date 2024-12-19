"""
Nome do Módulo: etl_sap_vehicle.py
Descrição: Este módulo contém as rotinas para importação de dados dos veiculos
Autor: Beatriz Amorim - Projjetta
Data: 2024-12-17
"""

import copy
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ...library.database import (
    DW_ENGINE as DWE
)

from .sap_api import (
    SapApiRequestMethod as SAM,
    SapApiConnection as SAC,
    SapApiPaginationRequest as SPR,
    sap_formatted_query_date as FQD
)

from .model.sap_model import SapBonanzaBase
from .model.vehicles import Vehicle,VehicleCollection

def run_pipeline(**kwargs):
    """ Executar a extração """

    load_full = kwargs.get("load_full", False)
    logger = kwargs.get("logger")

    load_base_date = FQD(datetime.now() - timedelta(days=(365 if load_full else 30))) # TODO: Ajustar AQUI!!!
    logger.debug(f"Load base date: {load_base_date} ...")


    logger.debug(f"Tabelas no metadata: {SapBonanzaBase.metadata.tables.keys()}")
    SapBonanzaBase.metadata.create_all(DWE.engine, checkfirst=True)


    sap_api_connection = SAC()
    sap_api_request = SPR(
        SAM.GET, 
        "SCGD_VEH",
        api_filter=f"(CreateDate ge '{load_base_date}' or UpdateDate ge '{load_base_date}')",
        api_select=(
                    "Code,"
                    "Name,"
                    "DocEntry,"
                    "Canceled,"
                    "Object,"
                    "LogInst,"
                    "UserSign,"
                    "Transfered,"
                    "CreateDate,"
                    "CreateTime,"
                    "UpdateDate,"
                    "UpdateTime,"
                    "DataSource,"
                    "U_CardName,"
                    "U_CardCode,"
                    "U_Potencia,"
                    "U_Cilindra,"
                    "U_Cod_Unid,"
                    "U_Cod_Marc,"
                    "U_Des_Marc,"
                    "U_Cod_Mode,"
                    "U_Des_Mode,"
                    "U_Cod_Esti,"
                    "U_Des_Esti,"
                    "U_Ano_Vehi,"
                    "U_Num_VIN,"
                    "U_Num_Mot,"
                    "U_MarcaMot,"
                    "U_Cant_Pas,"
                    "U_Peso,"
                    "U_Combusti,"
                    "U_Precio,"
                    "U_Val_CIF,"
                    "U_ValVeh,"
                    "U_Activo,"
                    "U_VENRES,"
                    "U_Dispo,"
                    "U_ContratoV,"
                    "U_DocPedido"
                    )
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        vehicles = page.get("value", [])

        if len(vehicles) > 0:
            with Session(DWE.engine) as db_session:
                
                for vehicle in vehicles:
                    vehicles_data = {k: v for k, v in vehicle.items() if k not in "odata.etag"}
                    
                    # Inserindo o item na tabela 'Item'
                    item_obj = Vehicle(**vehicles_data)
                    db_session.merge(item_obj)

                    if 'SCGD_VEHITRAZACollection' in vehicle:  
                        collection = vehicle['SCGD_VEHITRAZACollection']
                        for vehicle in collection:
                            vehicle['Code'] = vehicle['Code'] 
                            vehicle_obj = VehicleCollection(**vehicle) 
                            db_session.merge(vehicle_obj)

                   
                db_session.commit()