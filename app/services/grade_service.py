class GradeService:
    @staticmethod
    def calculate_grade(total_marks, max_marks=100.0, pass_marks=40.0):
        if max_marks <= 0:
            percentage = 0.0
        else:
            percentage = round((total_marks / max_marks) * 100, 2)

        is_pass = total_marks >= pass_marks

        if not is_pass:
            grade = 'F'
        elif percentage >= 90:
            grade = 'A+'
        elif percentage >= 80:
            grade = 'A'
        elif percentage >= 70:
            grade = 'B'
        elif percentage >= 60:
            grade = 'C'
        elif percentage >= 50:
            grade = 'D'
        else:
            grade = 'E'

        return {
            'total_marks': total_marks,
            'percentage': percentage,
            'grade': grade,
            'is_pass': is_pass
        }
