from .models import CourseAvailability


def get_alert_message(course: CourseAvailability) -> str:
    if course.cupo <= 0:
        return ""

    if course.cupo == 1:
        prefix = "🚨 *¡Alerta Crítica de Disponibilidad!*"
    elif course.cupo <= 5:
        prefix = "⚠️ *¡Alerta de Baja Disponibilidad!*"
    else:
        prefix = "🎓 *Materia Disponible:*"

    return (
        f"{prefix}\n"
        f"📘 Materia: {course.materia}\n"
        f"👨‍🏫 Profesor: {course.profesor}\n"
        f"📌 NRC: {course.nrc}\n"
        f"✅ Cupos Disponibles: {course.cupo}\n"
        f"🔗 URL: {course.url}"
    )
