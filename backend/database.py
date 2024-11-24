from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
DATABASE_URL = "sqlite:///./chatbot.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, index=True, nullable=False)  # Session grouping
    user_input = Column(String, index=True, nullable=True)  # Nullable for bot messages
    bot_response = Column(String, nullable=True)  # Nullable for user messages
    role = Column(String, index=True, nullable=True)  # Either 'user' or 'bot'

def init_db():
    Base.metadata.create_all(bind=engine)
