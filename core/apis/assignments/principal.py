# student_assignments_resources.py

from flask import Blueprint, jsonify
from core.models.assignments import Assignment, AssignmentStateEnum
from core.apis.assignments.schema import AssignmentSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'])
def get_principal_assignments():
    # Get submitted and graded assignments
    submitted_assignments = Assignment.query.filter(Assignment.state == AssignmentStateEnum.SUBMITTED).all()
    graded_assignments = Assignment.query.filter(Assignment.state == AssignmentStateEnum.GRADED).all()

    
    all_assignments = submitted_assignments + graded_assignments


    schema = AssignmentSchema(many=True)
    result = schema.dump(all_assignments)

    return jsonify(result)
