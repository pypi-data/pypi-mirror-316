"""
Nome do Módulo: etl_sap_ordem_trabalho.py
Descrição: Este módulo contém as rotinas para importação de dados das ordens de trabalho
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
from .model.ordem_trabalho import OrdemTrabalho, OrdemTrabalhoCollection



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
        "SCGD_OT",  # Endpoint relacionado a Ordens de Trabalho
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
            "U_NoOT,"
            "U_NoUni,"
            "U_NoCon,"
            "U_Plac,"
            "U_Marc,"
            "U_Esti,"
            "U_NoVis,"
            "U_EstVis,"
            "U_VIN,"
            "U_TipOT,"
            "U_EstW,"
            "U_FCom,"
            "U_FApe,"
            "U_FFin,"
            "U_EstO,"
            "U_Ase,"
            "U_EncO,"
            "U_Obse,"
            "U_CodEst,"
            "U_CodMar,"
            "U_Cotiz,"
            "U_RCot,"
            "U_DocEntry,"
            "U_OTRef,"
            "U_NGas,"
            "U_Sucu,"
            "U_Mode,"
            "U_CEst,"
            "U_CMod,"
            "U_CMar,"
            "U_Ano,"
            "U_CodCli,"
            "U_NCli,"
            "U_CodCOT,"
            "U_NCliOT,"
            "U_Cor,"
            "U_Tel,"
            "U_MOReal,"
            "U_MOEsta,"
            "U_NoCita,"
            "U_FecVta,"
            "U_Color,"
            "U_FechPro,"
            "U_Repro,"
            "U_Esp_Re,"
            "U_DEstO,"
            "U_km,"
            "U_HCom,"
            "U_HApe,"
            "U_HFin,"
            "U_FCerr,"
            "U_FFact,"
            "U_FEntr,"
            "U_FRec,"
            "U_HRec,"
            "U_HMot,"
            "U_SCGD_ObservInterna,"
            "U_ObservCierre,"
            "U_ObservDiag,"
            "U_CreadoPor,"
            "U_IdEstOTTC,"
            "U_Attachment,"
            "U_Bahia,"
            "U_FechaCierre,"
            "U_HoraCierre,"
            "U_NUrea,"
            "U_ComentariosG,"
            "SCGD_CTRLCOLCollection"  # Considerando a relação com a coleção de controle
        )
    )

    requested_data = sap_api_request.request_paginate_data(
        sap_api_connection
    )

    for page in requested_data:
        ordens_trabalho = page.get("value", [])

        if len(ordens_trabalho) > 0:
            with Session(DWE.engine) as db_session:
                
                for ordem in ordens_trabalho:
                    ordem_data = {k: v for k, v in ordem.items() if k not in "odata.etag"}
                    
                    # Inserindo a ordem de trabalho
                    ordem_obj = OrdemTrabalho(**ordem_data)
                    db_session.merge(ordem_obj)

                    if 'SCGD_CTRLCOLCollection' in ordem:  
                        collection = ordem['SCGD_CTRLCOLCollection']
                        for item in collection:
                            item['Code'] = ordem['Code']  # Assegurando que o código da ordem de trabalho é mantido
                            collection_obj = OrdemTrabalhoCollection(**item) 
                            db_session.merge(collection_obj)

                db_session.commit()
