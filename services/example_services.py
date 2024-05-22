from models.example_models import db, User, Boss, EmployeeReview, WorkInformation, Company, Alba, TimeBlock, Timetable
from flask import session, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

def login_user(id, password):
    try:
        user = User.query.filter_by(id=id).first()
        if user and user.password == password:
            session['user_id'] = user.user_id
            boss_info = Boss.query.filter_by(user_id=user.user_id).first()
            bossno = boss_info.bossno if boss_info else None
            return jsonify({
                'message': 'Login successful',
                'isemployer': user.isemployer,
                'bossno': bossno,
                'user_id': user.user_id
            }), 200
        else:
            return jsonify({'message': 'Invalid login credentials'}), 401
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

def logout_user():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200



def fetch_workers_by_boss(bossno):
    if not bossno:
        return jsonify({'error': 'Boss number is required'}), 400

    try:
        bossno = int(bossno)  # 입력 값을 정수로 변환 (오류 처리가 필요한 경우 이 부분을 강화)
        workers = db.session.query(
            WorkInformation, Alba, EmployeeReview
        ).join(
            Alba, WorkInformation.albano == Alba.albano  # User 대신 Alba 사용
        ).outerjoin(
            EmployeeReview, WorkInformation.reviewno == EmployeeReview.reviewno
        ).filter(
            WorkInformation.bossno == bossno
        ).all()

        if not workers:
            return jsonify({"message": "No workers found"}), 200

        results = []
        for work_info, alba, review in workers:
            result = {
                "albano": alba.albano,
                "name": alba.name,
                "age": alba.age if alba.age else "Not provided",
                "start_day": work_info.startday.strftime('%Y-%m-%d') if work_info.startday else "Not provided",
                "salary": work_info.money,
                "absent": work_info.absent,
                "late": work_info.late,
                "review_content": review.content if review else "No review available"
            }
            results.append(result)

        return jsonify({"worker_list": results}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


def add_worker():
    try:
        data = request.get_json()
        new_worker = Alba(
            albano=data['albano'],
            name=data['name'],
            age=data['age']
        )
        db.session.add(new_worker)
        db.session.commit()
        return jsonify({'message': 'Worker added successfully'}), 201
    except KeyError:
        return jsonify({'error': 'Missing required data'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500


def delete_alba(albano):
    alba = Alba.query.filter_by(albano=albano).first()
    if alba is None:
        return jsonify({'message': 'Alba not found'}), 404

    db.session.delete(alba)
    db.session.commit()

    return jsonify({'message': 'Alba deleted successfully'}), 20


def get_user_profile(request):
    user_id = request.args.get('user_id')  # 사용자 ID를 요청의 파라미터에서 가져옵니다.
    user = User.query.get(user_id)  # 데이터베이스에서 해당 ID의 사용자를 조회합니다.
    
    # 사용자 객체가 존재하고, 사용자가 boss이며, boss가 속한 회사 정보가 존재하는 경우
    if user and user.boss and user.boss.company:
        return jsonify({
            "name": user.name,          # 사용자 이름
            "age": user.age,            # 사용자 나이
            "compno": user.boss.company.comno,  # 회사 번호
            "type": user.boss.company.type,     # 회사 타입
            "com_name": user.boss.company.com_name,  # 회사 이름 추가
            "com_loc": user.boss.company.com_loc      # 회사 위치 추가
        }), 200
    else:
        return jsonify({'message': 'User not found'}), 404  # 사용자가 존재하지 않는 경우

    

def get_schedule(bossno):
    if not bossno:
        return jsonify({'error': 'Boss number is required'}), 400

    try:
        bossno = int(bossno)
        schedule = db.session.query(
            WorkInformation, Alba, TimeBlock, Timetable
        ).join(
            Alba, WorkInformation.albano == Alba.albano
        ).outerjoin(
            TimeBlock, Alba.albano == TimeBlock.albano
        ).outerjoin(
            Timetable, WorkInformation.comno == Timetable.comno
        ).filter(
            WorkInformation.bossno == bossno
        ).all()

        if not schedule:
            return jsonify({"message": "No schedule found"}), 404

        results = []
        for work_info, alba, timeblock, timetable in schedule:
            result = {
                "albano": alba.albano,
                "name": alba.name,
                "timeblocks": [{'start_time': timeblock.start_time, 'duration': timeblock.duration}] if timeblock else [],
                "timetables": [{'weekday': timetable.weekday, 'comno': timetable.comno}] if timetable else []
            }
            results.append(result)

        return jsonify(results), 200
    except ValueError:
        return jsonify({'error': 'Invalid boss number format'}), 400
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

