from sqlalchemy import String, Column, DateTime, Float, Integer
from sqlalchemy.orm import relationship
from .sap_model import SapBonanzaBase as SBB

class Agenda(SBB):
    __tablename__ = 'sap_agenda'

    DocNum = Column('DocNum', Integer, primary_key=True)
    Period = Column('Period', Integer)
    Instance = Column('Instance', Integer)
    Series = Column('Series', Integer)
    Handwritten = Column('Handwritten', String)
    Status = Column('Status', String)
    RequestStatus = Column('RequestStatus', String)
    Creator = Column('Creator', String)
    Remark = Column('Remark', String, nullable=True)
    DocEntry = Column('DocEntry', Integer)
    Canceled = Column('Canceled', String)
    Object = Column('Object', String)
    LogInst = Column('LogInst', String, nullable=True)
    UserSign = Column('UserSign', Integer)
    Transfered = Column('Transfered', String)
    CreateDate = Column('CreateDate', DateTime)
    CreateTime = Column('CreateTime', String)
    UpdateDate = Column('UpdateDate', DateTime)
    UpdateTime = Column('UpdateTime', String)
    DataSource = Column('DataSource', String)
    U_Agenda = Column('U_Agenda', String)
    U_EstadoLogico = Column('U_EstadoLogico', String)
    U_IntervaloCitas = Column('U_IntervaloCitas', String)
    U_Abreviatura = Column('U_Abreviatura', String)
    U_CodAsesor = Column('U_CodAsesor', String)
    U_CodTecnico = Column('U_CodTecnico', String, nullable=True)
    U_RazonCita = Column('U_RazonCita', String)
    U_ArticuloCita = Column('U_ArticuloCita', String)
    U_VisibleWeb = Column('U_VisibleWeb', String, nullable=True)
    U_CantCLunes = Column('U_CantCLunes', Integer)
    U_CantCMartes = Column('U_CantCMartes', Integer)
    U_CantCMiercoles = Column('U_CantCMiercoles', Integer)
    U_CantCJueves = Column('U_CantCJueves', Integer)
    U_CantCViernes = Column('U_CantCViernes', Integer)
    U_CantCSabado = Column('U_CantCSabado', Integer)
    U_CantCDomingo = Column('U_CantCDomingo', Integer)
    U_Num_Art = Column('U_Num_Art', String)
    U_Num_Razon = Column('U_Num_Razon', String, nullable=True)
    U_Cod_Sucursal = Column('U_Cod_Sucursal', String)
    U_NameAsesor = Column('U_NameAsesor', String)
    U_NameTecnico = Column('U_NameTecnico', String, nullable=True)
    U_TmpServ = Column('U_TmpServ', String, nullable=True)
    U_GenAva = Column('U_GenAva', String)

    def __repr__(self):
        return f"<SAPDocument(DocNum='{self.DocNum}', Creator='{self.Creator}', Status='{self.Status}')>"
