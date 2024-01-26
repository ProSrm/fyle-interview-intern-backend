# student_assignments_resources.py

from flask import Blueprint, jsonify
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher
from core.apis.teachers.schema import TeacherSchema
from core.apis.assignments.schema import AssignmentSchema ,AssignmentGradeSchema
from core.apis import decorators
from core import db
from core.apis.responses import APIResponse

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

## getting submitted and graded assignments . . . 
@principal_assignments_resources.route('/assignments', methods=['GET'])
@decorators.authenticate_principal
def get_principal_assignments(p):
    submitted_assignments = Assignment.query.filter(Assignment.state == AssignmentStateEnum.SUBMITTED).all()
    graded_assignments = Assignment.query.filter(Assignment.state == AssignmentStateEnum.GRADED).all()
    all_assignments = submitted_assignments + graded_assignments
    schema = AssignmentSchema(many=True)
    result = schema.dump(all_assignments)

    return jsonify(result)

## fetching all teachers . . . 
@principal_assignments_resources.route('/teachers', methods=['GET'])
@decorators.authenticate_principal
def get_principal_teachers(p):
    teachers = Teacher.query.all()
    schema = TeacherSchema(many=True)
    result = schema.dump(teachers)

    return jsonify(result)
## api for grading student assignment directly via principal . 
@principal_assignments_resources.route('/assignments/grade', methods=['POST'])
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment_principal(p,incoming_payload):
    print("Incoming Payload:", incoming_payload)
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    print("Loaded Payload:", grade_assignment_payload)
    graded_assignment = Assignment.mark_grade(
    _id=grade_assignment_payload.id,
    grade=grade_assignment_payload.grade,
    auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
