from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DECIMAL, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    address = Column(Text)
    verification_status = Column(String(50), default="pending")
    verified_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    students = relationship("Student", back_populates="school")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    date_of_birth = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    school = relationship("School", back_populates="students")
    guardians = relationship("Guardian", back_populates="student")
    agent_students = relationship("AgentStudent", back_populates="student")
    scholarships = relationship("Scholarship", back_populates="student")


class Guardian(Base):
    __tablename__ = "guardians"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    relationship = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    student = relationship("Student", back_populates="guardians")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    phone = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    agent_students = relationship("AgentStudent", back_populates="agent")
    scholarships = relationship("Scholarship", back_populates="agent")


class AgentStudent(Base):
    __tablename__ = "agent_students"

    agent_id = Column(Integer, ForeignKey("agents.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)

    agent = relationship("Agent", back_populates="agent_students")
    student = relationship("Student", back_populates="agent_students")


class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    items = Column(JSON, nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())

    student = relationship("Student", back_populates="scholarships")
    agent = relationship("Agent", back_populates="scholarships")
    payments = relationship("Payment", back_populates="scholarship")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id"), nullable=True)
    donor_email = Column(String(255))
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(10), default="USD")
    payment_provider = Column(String(50))
    provider_reference = Column(String(255))
    status = Column(String(50), default="pending")
    verified_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    scholarship = relationship("Scholarship", back_populates="payments")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_type = Column(String(50))
    user_id = Column(Integer)
    notification_type = Column(String(100))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())