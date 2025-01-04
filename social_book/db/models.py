from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy_setup import Base

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    visibility = Column(Boolean, default=True)
    cost = Column(Float, nullable=True)
    year_published = Column(Integer, nullable=True)
    file_path = Column(String, nullable=False)
