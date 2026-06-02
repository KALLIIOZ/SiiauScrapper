import time
from typing import Dict, List

from src.siiauscrapper.evaluator import get_alert_message
from src.siiauscrapper.fetcher import fetch_course_availability
from src.siiauscrapper.notifier import TelegramNotifier
from src.siiauscrapper.settings import DEFAULT_TELEGRAM_CHAT_IDS, MONITORING_CONFIG, POLL_INTERVAL_SECONDS


def normalize_chat_ids(monitor: Dict) -> List[int]:
    configured = monitor.get("chat_ids") or []
    return [int(value) for value in configured] if configured else DEFAULT_TELEGRAM_CHAT_IDS


def build_monitoring_plan() -> List[Dict]:
    return MONITORING_CONFIG.get("monitors", [])


def main() -> None:
    notifier = TelegramNotifier()
    monitoring_plan = build_monitoring_plan()
    previous_state: Dict[tuple, int] = {}

    print("Iniciando monitor de cupos SIIAU...")
    while True:
        for monitor in monitoring_plan:
            chat_ids = normalize_chat_ids(monitor)
            monitor_name = monitor.get("name", "default")
            urls = monitor.get("urls", [])

            if not chat_ids:
                print(f"Advertencia: el monitor '{monitor_name}' no tiene chat_ids configurados.")
                continue

            print(f"Procesando monitor '{monitor_name}' con {len(urls)} URL(s)...")
            for url in urls:
                try:
                    courses = fetch_course_availability(url, verify=True)
                except Exception as exc:
                    print(f"Error fetching {url}: {exc}")
                    continue

                for course in courses:
                    state_key = (monitor_name, course.nrc)
                    previous_cupo = previous_state.get(state_key)
                    if previous_cupo == course.cupo:
                        continue

                    previous_state[state_key] = course.cupo
                    alert_text = get_alert_message(course)
                    if not alert_text:
                        continue

                    notifier.send(alert_text, chat_ids)

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
