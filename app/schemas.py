from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class SchoolBase(BaseModel):
    name: str
    email: Optional[str] = None
    address: Optional[str] = None


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    verification_status: Optional[str] = None


class SchoolResponse(SchoolBase):
    id: int
    verification_status: str
    verified_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class StudentBase(BaseModel):
    school_id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class StudentResponse(StudentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GuardianBase(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    relationship: Optional[str] = None


class GuardianCreate(GuardianBase):
    pass


class GuardianUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    relationship: Optional[str] = None


class GuardianResponse(GuardianBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AgentBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class AgentResponse(AgentBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ScholarshipItem(BaseModel):
    description: str
    amount: float


class ScholarshipBase(BaseModel):
    student_id: int
    items: List[ScholarshipItem]
    total_amount: float
    agent_id: Optional[int] = None


class ScholarshipCreate(ScholarshipBase):
    pass


class ScholarshipUpdate(BaseModel):
    items: Optional[List[ScholarshipItem]] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None


class ScholarshipResponse(BaseModel):
    id: int
    student_id: int
    agent_id: Optional[int]
    items: List[ScholarshipItem]
    total_amount: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    scholarship_id: Optional[int] = None
    donor_email: Optional[str] = None
    amount: float
    currency: Optional[str] = "USD"
    payment_provider: Optional[str] = "paystack"


class PaymentInitiate(PaymentBase):
    pass


class PaymentCreate(PaymentBase):
    provider_reference: Optional[str] = None
    status: Optional[str] = "pending"


class PaymentResponse(BaseModel):
    id: int
    scholarship_id: Optional[int]
    donor_email: Optional[str]
    amount: Decimal
    currency: str
    payment_provider: Optional[str]
    provider_reference: Optional[str]
    status: str
    verified_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentVerifyResponse(BaseModel):
    status: str
    amount: Decimal
    currency: str
    provider_reference: str