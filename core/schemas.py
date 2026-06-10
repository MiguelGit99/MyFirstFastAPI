from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class IssueStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"

class IssuePriority(str, Enum):
    LOW = "low"
    MEDIUM = "Medium"
    HIGH = "High"

class IssueCreate(BaseModel):
    title: str = Field(
        min_length=3, 
        max_length=100
    ) 
    description: str = Field(
        min_length=5, 
        max_length=1000
    )    
    priority: IssuePriority = IssuePriority.MEDIUM


class IssueUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None, 
        max_length=100
    ) 
    description: Optional[str] = Field(
        default=None,
        min_length=5, 
        max_length=1000
    )    
    priority: Optional[IssuePriority] = None
    status: Optional[IssueStatus] = None

class IssueOut(BaseModel):
    id: str
    title: str
    description: str 
    priority: IssuePriority
    status: IssueStatus
