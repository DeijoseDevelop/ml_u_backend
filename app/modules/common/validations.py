import re
from app.modules.common import exceptions
from .enums import AcademicProgram



def validate_user_data_with_picture(user_data, picture):
    if not user_data.get("name"):
        raise exceptions.UseCaseException(message="nombre es requerido")
    if not user_data.get("last_name"):
        raise exceptions.UseCaseException(message="Apellido es requerido")
    if not user_data.get("email"):
        raise exceptions.UseCaseException(message="Email es requerido")
    if not user_data.get("document_number"):
        raise exceptions.UseCaseException(message="Numero de documento es requerido")
    if not user_data.get("user_type"):
        raise exceptions.UseCaseException(message="Tipo de usuario es requerido")
    if not user_data.get("dependency"):
        raise exceptions.UseCaseException(message="Dependencia es requerido")
    if not user_data.get("academic_program"):
        raise exceptions.UseCaseException(message="Programa academico es requerido")
    if not picture:
        raise exceptions.UseCaseException(message="Imagen es requerida")
    validate_email(user_data.get("email"))
    validate_gender(user_data.get("gender"))
    validate_academic_program(user_data.get("academic_program"))
    validate_document_number(user_data.get("document_number"))

        
        
def validate_user_data(user_data):
    if not user_data.get("name"):
        raise exceptions.UseCaseException(message="nombre es requerido")
    if not user_data.get("last_name"):
        raise exceptions.UseCaseException(message="Apellido es requerido")
    if not user_data.get("email"):
        raise exceptions.UseCaseException(message="Email es requerido")
    if not user_data.get("document_number"):
        raise exceptions.UseCaseException(message="Numero de documento requerido")
    if not user_data.get("user_type"):
        raise exceptions.UseCaseException(message="tipo de usuario es requerido")
    if not user_data.get("password"):
        raise exceptions.UseCaseException(message="Password es requerido")
    validate_email(user_data.get("email"))
    validate_gender(user_data.get("gender"))
    validate_document_number(user_data.get("document_number"))




def validate_email(email: str):
    if not email.strip() or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise exceptions.UseCaseException(message="intrucir email valido")

def validate_gender(gender: str):
    allowed_genders = ["Masculino", "Femenino", "Otro"]
    if gender.strip() not in allowed_genders:
        raise exceptions.UseCaseException(message=f"Gender must be one of {allowed_genders}")

def validate_picture(picture):
    if picture.mimetype.strip() not in ["image/jpeg", "image/png"]:
        raise exceptions.UseCaseException(message="Picture must be a JPEG or PNG image")
    if picture.content_length > 5 * 1024 * 1024:  # 5 MB
        raise exceptions.UseCaseException(message="Picture size must not exceed 5 MB")


def validate_document_number(document_number: str):
    if not re.match(r"^\d{6,}$", document_number.strip()):
        raise exceptions.UseCaseException(message="Número de documento inválido.")


def validate_academic_program(academic_program: str):
    if academic_program.strip() not in [p.value for p in AcademicProgram]:
        raise exceptions.UseCaseException(message=f"Programa academico no valido")
    