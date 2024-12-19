"""
Nome do Módulo: etl_sap_ordem_citas.py
Descrição: Este módulo contém as rotinas para importação de dados das ordens de citações
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
from .model.ordem_citas import OrdemCitas

def run_pipeline(**kwargs):
    """ Executar a extração """

    load_full = kwargs.get("load_full", False)
    logger = kwargs.get("logger")

    load_base_date = FQD(datetime.now() - timedelta(days=(365 if load_full else 30)))  # TODO: Ajustar AQUI!!!
    logger.debug(f"Load base date: {load_base_date} ...")

    logger.debug(f"Tabelas no metadata: {SapBonanzaBase.metadata.tables.keys()}")
    SapBonanzaBase.metadata.create_all(DWE.engine, checkfirst=True)

    sap_api_connection = SAC()
    sap_api_request = SPR(
        SAM.GET, 
        "SCGD_CIT",  
        api_filter=f"(CreateDate ge '{load_base_date}' or UpdateDate ge '{load_base_date}')",
        api_select=(
            "DocNum,"
            "Period,"
            "Instance,"
            "Series,"
            "Handwrtten,"
            "Status,"
            "RequestStatus,"
            "Creator,"
            "Remark,"
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
            "U_NumCita,"
            "U_Num_Cot,"
            "U_FechaCita,"
            "U_HoraCita,"
            "U_Cod_Sucursal,"
            "U_Cod_Agenda,"
            "U_Cod_Razon,"
            "U_Estado,"
            "U_Cod_Asesor,"
            "U_Cod_Tecnico,"
            "U_CardCode,"
            "U_Cod_Unid,"
            "U_CreadoPor,"
            "U_FhaSync,"
            "U_UsaArt,"
            "U_Num_Serie,"
            "U_Name_Asesor,"
            "U_Name_Tecnico,"
            "U_CardName,"
            "U_CpnNo,"
            "U_CpnName,"
            "U_Moneda,"
            "U_TipoC,"
            "U_Total_Doc,"
            "U_Total_Imp,"
            "U_Total_Lin,"
            "U_FhaCita_Fin,"
            "U_HoraCita_Fin,"
            "U_Num_Placa,"
            "U_Observ,"
            "U_FhaServ,"
            "U_HoraServ,"
            "U_FhaServ_Fin,"
            "U_HoraServ_Fin,"
            "U_CodVehi,"
            "U_NCliOT,"
            "U_CCliOT,"
            "U_MCancelacion,"
            "U_CCancelacion,"
            "U_Retiro,"
            "U_CRetiro,"
            "U_Entrega,"
            "U_CEntrega,"
            "U_Movilidad,"
            "U_CMovilidad,"
            "U_Contacto,"
            "U_Campana,"
            "U_Garantia,"
            "U_UsrAnonimo,"
            "U_CliTel,"
            "U_CliEmail,"
            "U_VehPlaca,"
            "U_UpdateBy,"
            "U_CContacto,"
            "U_Overbook,"
            "U_Towing,"
            "U_CliCel,"
            "U_Cod_Marc,"
            "U_Des_Marc,"
            "U_Cod_Esti,"
            "U_Des_Esti,"
            "U_Cod_Mode,"
            "U_Des_Mode,"
            "U_ComentariosGeneralesCIT_OT,"
            "U_TAdicional"
        )
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        ordem_citas = page.get("value", [])

        if len(ordem_citas) > 0:
            with Session(DWE.engine) as db_session:

                for ordem_cita in ordem_citas:
                    ordem_citas_data = {k: v for k, v in ordem_cita.items() if k not in "odata.etag"}
                    
                    # Inserindo o item na tabela 'OrdemCitas'
                    ordem_citas_obj = OrdemCitas(**ordem_citas_data)
                    db_session.merge(ordem_citas_obj)

                db_session.commit()
