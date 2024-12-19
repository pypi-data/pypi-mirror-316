from sqlalchemy import String, Column, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .sap_model import SapBonanzaBase as SBB

class Vehicle(SBB):
    __tablename__ = 'sap_vehicle'

    Code = Column('Code', String, primary_key=True)
    Name = Column('Name', String)
    DocEntry = Column('DocEntry', Integer)
    Canceled = Column('Canceled', String)
    Object = Column('Object', String)
    LogInst = Column('LogInst', String)
    UserSign = Column('UserSign', Integer)
    Transfered = Column('Transfered', String)
    CreateDate = Column('CreateDate', DateTime)
    CreateTime = Column('CreateTime', String)
    UpdateDate = Column('UpdateDate', DateTime)
    UpdateTime = Column('UpdateTime', String)
    DataSource = Column('DataSource', String)
    U_CardName = Column('U_CardName', String)
    U_CardCode = Column('U_CardCode', String)
    U_Potencia = Column('U_Potencia', Integer)
    U_Cilindra = Column('U_Cilindra', Integer)
    U_Cod_Unid = Column('U_Cod_Unid', String)
    U_Cod_Marc = Column('U_Cod_Marc', String)
    U_Des_Marc = Column('U_Des_Marc', String)
    U_Cod_Mode = Column('U_Cod_Mode', String)
    U_Des_Mode = Column('U_Des_Mode', String)
    U_Cod_Esti = Column('U_Cod_Esti', String)
    U_Des_Esti = Column('U_Des_Esti', String)
    U_Ano_Vehi = Column('U_Ano_Vehi', Integer)
    U_Num_VIN = Column('U_Num_VIN', String)
    U_Num_Mot = Column('U_Num_Mot', String)
    U_MarcaMot = Column('U_MarcaMot', String)
    U_Cant_Pas = Column('U_Cant_Pas', Integer)
    U_Peso = Column('U_Peso', Float)
    U_Km_Unid = Column('U_Km_Unid', Float)
    U_Combusti = Column('U_Combusti', String)
    U_Precio = Column('U_Precio', Float)
    U_Val_CIF = Column('U_Val_CIF', Float)
    U_ValVeh = Column('U_ValVeh', Float)
    U_Activo = Column('U_Activo', String)
    U_VENRES = Column('U_VENRES', String)
    U_Dispo = Column('U_Dispo', Integer)
    U_ContratoV = Column('U_ContratoV', Integer)
    U_DocPedido = Column('U_DocPedido', Integer)
    
    
    
    # Relacionamento com VehicleCollection
    vehicle_collections = relationship("VehicleCollection", back_populates="vehicle")

    def __repr__(self):
        return f"<Vehicle(code='{self.Code}', description='{self.U_Des_Marc} - {self.U_Des_Mode}')>"

class VehicleCollection(SBB):
    __tablename__ = 'sap_vehicle_collection'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column('Code', String, ForeignKey(f'{SBB.__table_args__.get("schema")}.sap_vehicle.Code'))
    LineId = Column('LineId', Integer)
    Object = Column('Object', String)
    LogInst = Column('LogInst', String)
    U_NumCV_V = Column('U_NumCV_V', String)
    U_FhaCV_V = Column('U_FhaCV_V', DateTime)
    U_CodVen_V = Column('U_CodVen_V', String)
    U_NumFac_V = Column('U_NumFac_V', String)
    U_TotCV_V = Column('U_TotCV_V', Float)
    U_FhaFac_V = Column('U_FhaFac_V', DateTime)
    U_ValVeh = Column('U_ValVeh', Float)
    U_ValVehS = Column('U_ValVehS', Float)
    U_Km_Ingreso = Column('U_Km_Ingreso', Float)
    U_Km_Venta = Column('U_Km_Venta', Float)

    # Relacionamento com Vehicle
    vehicle = relationship("Vehicle", back_populates="vehicle_collections")

    def __repr__(self):
        return f"<VehicleCollection(line_id='{self.LineId}', total_value='{self.U_TotCV_V}', vehicle_value='{self.U_ValVeh}')>"
