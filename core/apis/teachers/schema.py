from core.models.teachers import Teacher
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher