"""
Nome do Módulo: etl_sap_agenda.py
Descrição: Este módulo contém as rotinas para importação de dados dos agenda
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
from .model.agenda import Agenda

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
        "SCGD_AGENDA",
        api_filter=f"(CreateDate ge '{load_base_date}' or UpdateDate ge '{load_base_date}')",
        api_select=(
                "DocNum,"
                "Period,"
                "Instance,"
                "Series,"
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
                "U_Agenda,"
                "U_EstadoLogico,"
                "U_IntervaloCitas,"
                "U_Abreviatura,"
                "U_CodAsesor,"
                "U_CodTecnico,"
                "U_RazonCita,"
                "U_ArticuloCita,"
                "U_VisibleWeb,"
                "U_CantCLunes,"
                "U_CantCMartes,"
                "U_CantCMiercoles,"
                "U_CantCJueves,"
                "U_CantCViernes,"
                "U_CantCSabado,"
                "U_CantCDomingo,"
                "U_Num_Art,"
                "U_Num_Razon,"
                "U_Cod_Sucursal,"
                "U_NameAsesor,"
                "U_NameTecnico,"
                "U_TmpServ,"
                "U_GenAva"
                )
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        agendas = page.get("value", [])

        if len(agendas) > 0:
            with Session(DWE.engine) as db_session:
                
                for agenda in agendas:
                    agenda_data = {k: v for k, v in agenda.items() if k not in "odata.etag"}
                    
                    # Inserindo a agenda na tabela 'Agenda'
                    agenda_obj = Agenda(**agenda_data)
                    db_session.merge(agenda_obj)

                db_session.commit()
