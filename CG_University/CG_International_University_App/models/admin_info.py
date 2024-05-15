from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()



@dataclass
class AdminInfoClass:
    id: int
    full_name: str
    contact_no: str
    email: str
    username: str
    password: str

    @staticmethod
    def from_dict(obj: Any) -> 'AdminInfoClass':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        full_name = from_str(obj.get("full_name"))
        contact_no = from_str(obj.get("contact_no"))
        email = from_str(obj.get("email"))
        username = from_str(obj.get("username"))
        password = from_str(obj.get("password"))
        return AdminInfoClass(id, full_name, contact_no, email, username, password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["full_name"] = from_str(self.full_name)
        result["contact_no"] = from_str(self.contact_no)
        result["email"] = from_str(self.email)
        result["username"] = from_str(self.username)
        result["password"] = from_str(self.password)
        return result


@dataclass
class Student:
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

    @staticmethod
    def from_dict(obj: Any) -> 'Student':
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
        return Student(enrollment_no, password, full_name, father_name, mother_name, gender, date_of_birth, category, email, mobile_number, address)

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
        return result

@dataclass
class StudentsDatum:
    student_enrollment_no: str
    student_provision: Optional[str] = None
    student_admit_card: Optional[str] = None
    student_affidevit: Optional[str] = None
    student_photo: Optional[str] = None
    student_migrations: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'StudentsDatum':
        assert isinstance(obj, dict)
        student_enrollment_no = from_str(obj.get("student_enrollment_no"))
        student_provision = from_union([from_none, from_str], obj.get("student_provision"))
        student_admit_card = from_union([from_none, from_str], obj.get("student_admit_card"))
        student_affidevit = from_union([from_none, from_str], obj.get("student_affidevit"))
        student_photo = from_union([from_none, from_str], obj.get("student_photo"))
        student_migrations = from_union([from_none, from_str], obj.get("student_migrations"))
        return StudentsDatum(student_enrollment_no, student_provision, student_admit_card, student_affidevit, student_photo, student_migrations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["student_enrollment_no"] = from_str(self.student_enrollment_no)
        result["student_provision"] = from_union([from_none, from_str], self.student_provision)
        result["student_admit_card"] = from_union([from_none, from_str], self.student_admit_card)
        result["student_affidevit"] = from_union([from_none, from_str], self.student_affidevit)
        result["student_photo"] = from_union([from_none, from_str], self.student_photo)
        result["student_migrations"] = from_union([from_none, from_str], self.student_migrations)
        return result




@dataclass
class StudentsMarksheet:
    id: int
    student_enrollment_no: Optional[str] = None
    session: Optional[str] = None
    semester: Optional[int] = None
    sgpa: Optional[str] = None
    status: Optional[str] = None
    result: Optional[str] = None
    file: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'StudentsMarksheet':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        student_enrollment_no = from_str(obj.get("student_enrollment_no"))
        session = from_str(obj.get("session"))
        semester = int(from_str(obj.get("semester")))
        sgpa = from_str(obj.get("sgpa"))
        status = from_str(obj.get("status"))
        result = from_str(obj.get("result"))
        file = from_str(obj.get("file"))
        return StudentsMarksheet(id, student_enrollment_no, session, semester, sgpa, status, result, file)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["student_enrollment_no"] = from_str(self.student_enrollment_no)
        result["session"] = from_str(self.session)
        result["semester"] = from_str(str(self.semester))
        result["sgpa"] = from_str(self.sgpa)
        result["status"] = from_str(self.status)
        result["result"] = from_str(self.result)
        result["file"] = from_str(self.file)
        return result



@dataclass
class AdminInfo:
    success: str
    admin_info: AdminInfoClass
    students: List[Student]
    students_data: Optional[List[StudentsDatum]]
    students_marksheets: Optional[List[StudentsMarksheet]]

    @staticmethod
    def from_dict(obj: Any) -> 'AdminInfo':
        assert isinstance(obj, dict)
        success = from_str(obj.get("success"))
        admin_info = AdminInfoClass.from_dict(obj.get("admin_info"))
        students = from_list(Student.from_dict, obj.get("students"))
        students_data = from_list(StudentsDatum.from_dict, obj.get("students_data")) if "students_data" in obj else None
        students_marksheets = from_list(StudentsMarksheet.from_dict, obj.get("students_marksheets")) if "students_marksheets" in obj else None
        return AdminInfo(success, admin_info, students, students_data, students_marksheets)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_str(self.success)
        result["admin_info"] = to_class(AdminInfoClass, self.admin_info)
        result["students"] = from_list(lambda x: to_class(Student, x), self.students)
        if self.students_data is not None:
            result["students_data"] = from_list(lambda x: to_class(StudentsDatum, x), self.students_data)
        if self.students_marksheets is not None:
            result["students_marksheets"] = from_list(lambda x: to_class(StudentsMarksheet, x), self.students_marksheets)
        return result


def admin_info_from_dict(s: Any) -> AdminInfo:
    return AdminInfo.from_dict(s)


def admin_info_to_dict(x: AdminInfo) -> Any:
    return to_class(AdminInfo, x)
