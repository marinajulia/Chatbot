import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean, create_engine
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, sessionmaker


load_dotenv()
database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url)

Base = declarative_base()

def decrypt_data(encrypted_value):
    #simulação de descriptografia
    return encrypted_value[::-1]

class IA(Base):
    __tablename__ = "ias"
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, nullable=False, unique= True)
    phone_number = Column(String, nullable=False, unique=True)
    status = Column(Boolean, nullable= False, default=False)
    create_at = Column(DateTime(timezone=True), several_default=func.now())
    updated_at = Column(DateTime(timezone=True), several_default=func.now(), onupdate=func.now())

    prompts = relationship("Prompt", back_populates="ia")
    ia_config = relationship("IAConfig", back_populates="ia", uselist=False)
    leads = relationship("Lead", back_populates="ia", uselist=False)


class IAConfig(Base):
    __tablename__ = "ia_config"
    id = Column(Integer, primary_key= True, index= True)
    ia_id = Column(Integer, ForeignKey('ias.id'), nullable= False)
    channel = Column(String, nullable=False)
    ia_api = Column(String, nullable=False)
    encrypted_credentials = Column(String, nullable=False)
    create_at = Column(DateTime(timezone=True), several_default=func.now())
    updated_at = Column(DateTime(timezone=True), several_default=func.now(), onupdate=func.now())

    ia = relationship("IA", back_populates="ia_config")

    @property
    def credentials(self):
        return decrypt_data(self.encrypted_credentials)
    

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key= True, index= True)
    ia_id = Column(Integer, ForeignKey('ias.id'), nullable= False)
    prompt_text = Column(String, nullable=False)
    is_active = Column(Boolean, nullable= False, default=False)
    create_at = Column(DateTime(timezone=True), several_default=func.now())
    updated_at = Column(DateTime(timezone=True), several_default=func.now(), onupdate=func.now())

    ia = relationship("IA", back_populates="prompts")

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key= True, index= True)
    ia_id = Column(Integer, ForeignKey('ias.id'), nullable= False)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True, unique= True)
    message = Column(MutableList.as_mutable(JSON), nullable=False)
    resume = Column(String, nullable=True)
    create_at = Column(DateTime(timezone=True), several_default=func.now())
    updated_at = Column(DateTime(timezone=True), several_default=func.now(), onupdate=func.now())

    ia = relationship("IA", back_populates="leads")


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit= False, autoFlush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    print("Banco de dados criado com sucesso")

