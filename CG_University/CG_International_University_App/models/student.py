from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser
from typing import Optional



T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

@dataclass
class StudentData:
    student_enrollment_no: Optional[str] = None
    student_provision: Optional[str] = None
    student_admit_card: Optional[str] = None
    student_affidevit: Optional[str] = None
    student_migrations: Optional[str] = None
    student_degree: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'StudentData':
        assert isinstance(obj, dict)
        return StudentData(
            student_enrollment_no=obj.get("student_enrollment_no"),
            student_provision=obj.get("student_provision"),
            student_admit_card=obj.get("student_admit_card"),
            student_affidevit=obj.get("student_affidevit"),
            student_migrations=obj.get("student_migrations"),
            student_degree=obj.get("student_degree")
        )

    def to_dict(self) -> dict:
        result = {}
        if self.student_enrollment_no is not None:
            result["student_enrollment_no"] = self.student_enrollment_no
        if self.student_provision is not None:
            result["student_provision"] = self.student_provision
        if self.student_admit_card is not None:
            result["student_admit_card"] = self.student_admit_card
        if self.student_affidevit is not None:
            result["student_affidevit"] = self.student_affidevit
        if self.student_migrations is not None:
            result["student_migrations"] = self.student_migrations
        if self.student_degree is not None:
            result["student_degree"] = self.student_degree
        return result


@dataclass
class StudentMarksheet:
    id: Optional[int] = None
    student_enrollment_no: Optional[str] = None
    session: Optional[str] = None
    semester: Optional[int] = None
    sgpa: Optional[str] = None
    status: Optional[str] = None
    result: Optional[str] = None
    file: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'StudentMarksheet':
        assert isinstance(obj, dict)
        return StudentMarksheet(
            id=obj.get("id"),
            student_enrollment_no=obj.get("student_enrollment_no"),
            session=obj.get("session"),
            semester=obj.get("semester"),
            sgpa=obj.get("sgpa"),
            status=obj.get("status"),
            result=obj.get("result"),
            file=obj.get("file")
        )

    def to_dict(self) -> dict:
        result = {}
        if self.id is not None:
            result["id"] = self.id
        if self.student_enrollment_no is not None:
            result["student_enrollment_no"] = self.student_enrollment_no
        if self.session is not None:
            result["session"] = self.session
        if self.semester is not None:
            result["semester"] = self.semester
        if self.sgpa is not None:
            result["sgpa"] = self.sgpa
        if self.status is not None:
            result["status"] = self.status
        if self.result is not None:
            result["result"] = self.result
        if self.file is not None:
            result["file"] = self.file
        return result


@dataclass
class StudentPersonalInfo:
    enrollment_no: str
    password: str
    full_name: str
    father_name: str
    mother_name: str
    gender: str
    date_of_birth: datetime
    category: str
    email: str
    mobile_number: str
    address: str
    profile_pic: Optional[str] = None
    
    
    @staticmethod
    def from_dict(obj: Any) -> 'StudentPersonalInfo':
        assert isinstance(obj, dict)
        enrollment_no = from_str(obj.get("enrollment_no"))
        password = from_str(obj.get("password"))
        full_name = from_str(obj.get("full_name"))
        father_name = from_str(obj.get("father_name"))
        mother_name = from_str(obj.get("mother_name"))
        gender = from_str(obj.get("gender"))
        date_of_birth = from_datetime(obj.get("date_of_birth"))
        category = from_str(obj.get("category"))
        email = from_str(obj.get("email"))
        mobile_number = from_str(obj.get("mobile_number"))
        address = from_str(obj.get("address"))
        profile_pic = from_str(obj.get("profile_pic"))
        
        return StudentPersonalInfo(enrollment_no, password, full_name, father_name, mother_name, gender, date_of_birth, category, email, mobile_number, address, profile_pic)

    def to_dict(self) -> dict:
        result: dict = {}
        result["enrollment_no"] = from_str(self.enrollment_no)
        result["password"] = from_str(self.password)
        result["full_name"] = from_str(self.full_name)
        result["father_name"] = from_str(self.father_name)
        result["mother_name"] = from_str(self.mother_name)
        result["gender"] = from_str(self.gender)
        result["date_of_birth"] = self.date_of_birth.isoformat()
        result["category"] = from_str(self.category)
        result["email"] = from_str(self.email)
        result["mobile_number"] = from_str(self.mobile_number)
        result["address"] = from_str(self.address)
        result["profile_pic"] = from_str(self.profile_pic)
        
        return result



@dataclass
class StudentInfo:
    student_data: Optional[StudentData] = None
    student_personal_info: StudentPersonalInfo = None
    student_marksheets: Optional[List[StudentMarksheet]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'StudentInfo':
        assert isinstance(obj, dict)
        return StudentInfo(
            student_data=StudentData.from_dict(obj.get("student_data")) if obj.get("student_data") else None,
            student_personal_info = StudentPersonalInfo.from_dict(obj.get("student_personal_info")),
            student_marksheets=[StudentMarksheet.from_dict(item) for item in obj.get("student_marksheets")] if obj.get("student_marksheets") else None
        )

    def to_dict(self) -> dict:
        result = {}
        if self.student_data is not None:
            result["student_data"] = self.student_data.to_dict()
        if self.student_personal_info is not None:
            result["student_personal_info"] = self.student_personal_info.to_dict()
        if self.student_marksheets is not None:
            result["student_marksheets"] = [item.to_dict() for item in self.student_marksheets]
        return result


@dataclass
class StudentInformation:
    success: Optional[str] = None
    student_info: Optional[StudentInfo] = None

    @staticmethod
    def from_dict(obj: Any) -> 'StudentInformation':
        assert isinstance(obj, dict)
        return StudentInformation(
            success=obj.get("success"),
            student_info=StudentInfo.from_dict(obj.get("student_info")) if obj.get("student_info") else None
        )

    def to_dict(self) -> dict:
        result = {}
        if self.success is not None:
            result["success"] = self.success
        if self.student_info is not None:
            result["student_info"] = self.student_info.to_dict()
        return result
