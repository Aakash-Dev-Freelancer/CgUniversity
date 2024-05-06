from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


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
    student_enrollment_no: str
    student_provision: str
    student_admit_card: str
    student_affidevit: str
    student_photo: str
    student_migrations: str

    @staticmethod
    def from_dict(obj: Any) -> 'StudentData':
        assert isinstance(obj, dict)
        student_enrollment_no = from_str(obj.get("student_enrollment_no"))
        student_provision = from_str(obj.get("student_provision"))
        student_admit_card = from_str(obj.get("student_admit_card"))
        student_affidevit = from_str(obj.get("student_affidevit"))
        student_photo = from_str(obj.get("student_photo"))
        student_migrations = from_str(obj.get("student_migrations"))
        return StudentData(student_enrollment_no, student_provision, student_admit_card, student_affidevit, student_photo, student_migrations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["student_enrollment_no"] = from_str(self.student_enrollment_no)
        result["student_provision"] = from_str(self.student_provision)
        result["student_admit_card"] = from_str(self.student_admit_card)
        result["student_affidevit"] = from_str(self.student_affidevit)
        result["student_photo"] = from_str(self.student_photo)
        result["student_migrations"] = from_str(self.student_migrations)
        return result


@dataclass
class StudentMarksheet:
    id: int
    student_enrollment_no: str
    session: str
    semester: int
    sgpa: str
    status: str
    result: str
    file: str

    @staticmethod
    def from_dict(obj: Any) -> 'StudentMarksheet':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        student_enrollment_no = from_str(obj.get("student_enrollment_no"))
        session = from_str(obj.get("session"))
        semester = int(from_str(obj.get("semester")))
        sgpa = from_str(obj.get("sgpa"))
        status = from_str(obj.get("status"))
        result = from_str(obj.get("result"))
        file = from_str(obj.get("file"))
        return StudentMarksheet(id, student_enrollment_no, session, semester, sgpa, status, result, file)

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
class StudentPersonalInfo:
    enrollment_no: str
    password: int
    profile_pic: int
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
    def from_dict(obj: Any) -> 'StudentPersonalInfo':
        assert isinstance(obj, dict)
        enrollment_no = from_str(obj.get("enrollment_no"))
        password = int(from_str(obj.get("password")))
        profile_pic = int(from_str(obj.get("profile_pic")))
        full_name = from_str(obj.get("full_name"))
        father_name = from_str(obj.get("father_name"))
        mother_name = from_str(obj.get("mother_name"))
        gender = from_str(obj.get("gender"))
        date_of_birth = from_datetime(obj.get("date_of_birth"))
        category = from_str(obj.get("category"))
        email = from_str(obj.get("email"))
        mobile_number = from_str(obj.get("mobile_number"))
        address = from_str(obj.get("address"))
        return StudentPersonalInfo(enrollment_no, password, profile_pic, full_name, father_name, mother_name, gender, date_of_birth, category, email, mobile_number, address)

    def to_dict(self) -> dict:
        result: dict = {}
        result["enrollment_no"] = from_str(self.enrollment_no)
        result["password"] = from_str(str(self.password))
        result["profile_pic"] = from_str(str(self.profile_pic))
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
class StudentInfo:
    student_data: StudentData
    student_personal_info: StudentPersonalInfo
    student_marksheets: List[StudentMarksheet]

    @staticmethod
    def from_dict(obj: Any) -> 'StudentInfo':
        assert isinstance(obj, dict)
        student_data = StudentData.from_dict(obj.get("student_data"))
        student_personal_info = StudentPersonalInfo.from_dict(obj.get("student_personal_info"))
        student_marksheets = from_list(StudentMarksheet.from_dict, obj.get("student_marksheets"))
        return StudentInfo(student_data, student_personal_info, student_marksheets)

    def to_dict(self) -> dict:
        result: dict = {}
        result["student_data"] = to_class(StudentData, self.student_data)
        result["student_personal_info"] = to_class(StudentPersonalInfo, self.student_personal_info)
        result["student_marksheets"] = from_list(lambda x: to_class(StudentMarksheet, x), self.student_marksheets)
        return result


@dataclass
class StudentInformation:
    success: str
    student_info: StudentInfo

    @staticmethod
    def from_dict(obj: Any) -> 'StudentInformation':
        assert isinstance(obj, dict)
        success = from_str(obj.get("success"))
        student_info = StudentInfo.from_dict(obj.get("student_info"))
        return StudentInformation(success, student_info)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_str(self.success)
        result["student_info"] = to_class(StudentInfo, self.student_info)
        return result


def student_information_from_dict(s: Any) -> StudentInformation:
    return StudentInformation.from_dict(s)


def student_information_to_dict(x: StudentInformation) -> Any:
    return to_class(StudentInformation, x)
