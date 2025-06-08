from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Result

bp = Blueprint('api', __name__)


@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})


@bp.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()

        if not data or not all(k in data for k in ("name", "score")):
            return jsonify({"error": "Invalid input. 'name' and 'score' required."}), 400

        new_entry = Result(name=data['name'], score=int(data['score']))
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"message": "Data submitted successfully"}), 201

    except ValueError:
        return jsonify({"error": "Invalid 'score'. Must be an integer."}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500


@bp.route('/results', methods=['GET'])
def results():
    try:
        entries = Result.query.all()
        output = [
            {
                "id": e.id,
                "name": e.name,
                "score": e.score,
                "timestamp": e.timestamp.isoformat()
            } for e in entries
        ]
        return jsonify(output)

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
