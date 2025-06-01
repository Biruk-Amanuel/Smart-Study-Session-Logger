import csv

study_log = {}

def load_from_file():
    try:
        with open("study_log.txt", "r") as f:
            current_date = ""
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if not line.startswith(" "):  
                    current_date = line
                    study_log[current_date] = []
                else:  
                    parts = line.strip().split(" - ")   
                    subject = parts[0]
                    duration_part, focus_part = parts[1].split(",")
                    duration = float(duration_part.replace(" hrs", ""))
                    focus = int(focus_part.replace("Focus: ", "").replace("/5", ""))
                    session = {
                        "subject": subject,
                        "duration": duration,
                        "focus": focus
                    }
                    study_log[current_date].append(session)
    except FileNotFoundError:
        print("No existing log found. Starting fresh.")

def log_session():
    date = input("Enter the date (DD-MM-YYYY): ").strip()
    subject = input("What subject did you study? ").strip().title()

    try:
        duration = float(input("How many hours did you study? "))
        focus = int(input("Rate your focus level (1-5): "))
        if not (1 <= focus <= 5):
            raise ValueError
    except ValueError:
        print("❌ Invalid input. Duration must be a number. Focus must be between 1 and 5.")
        return

    if date not in study_log:
        study_log[date] = []

    session = {
        "subject": subject,
        "duration": duration,
        "focus": focus
    }

    study_log[date].append(session)

    if duration >= 4 and focus >= 4:
        print("🚀 Incredible stamina and focus! Consider sharing your study tips with others.")
    elif duration >= 3 and focus >= 2:
        print("👏 Great endurance! Remember to stretch and hydrate.")
    elif duration >= 2 and focus >= 4:
        print("🔥 You're on fire! Keep going!")
    elif duration >= 2 and focus <= 2:
        print("😐 Long session, but focus was low. Try shorter, more focused sessions next time.")
    elif duration >= 1 and focus >= 3:
        print("✅ Good work! Maybe take a short break.")
    elif duration < 1 and focus >= 4:
        print("⚡ Short but super focused! Quality over quantity.")
    elif duration < 1 and focus < 3:
        print("😴 Maybe take a proper break and come back refreshed.")
    elif duration >= 3 and focus == 1:
        print("🛑 Long session with very low focus. Consider changing your study environment or taking a longer break.")
    elif 1 <= duration < 2 and focus == 5:
        print("🌟 Excellent focus in a moderate session! Keep up the great concentration.")
    elif duration >= 5:
        print("🏆 Marathon session! Make sure to rest and avoid burnout.")
    elif duration < 0.5 and focus >= 2:
        print("⏳ Quick session! Even small efforts add up over time.")
    else:
        print("🙂 Keep tracking your sessions and aim for steady improvement.")

def show_summary():
    print("\n=== Study Summary ===")
    total_hours = 0
    total_focus = 0
    session_count = 0
    subject_totals = {}

    for date, sessions in study_log.items():
        print(f"\n📅 {date}")
        for s in sessions:
            print(f" - {s['subject']}: {s['duration']} hrs (Focus: {s['focus']}/5)")
            total_hours += s['duration']
            total_focus += s['focus']
            session_count += 1

            subj = s['subject']
            if subj not in subject_totals:
                subject_totals[subj] = {'hours': 0, 'count': 0}
            subject_totals[subj]['hours'] += s['duration']
            subject_totals[subj]['count'] += 1

    if session_count > 0:
        avg_focus = round(total_focus / session_count, 2)
        print(f"\n📊 Total Study Hours: {total_hours}")
        print(f"📈 Average Focus Level: {avg_focus}/5")
        print("\n📚 Subject-wise Hours:")
        for subj, data in subject_totals.items():
            print(f" - {subj}: {data['hours']} hrs over {data['count']} session(s)")
    else:
        print("No sessions logged yet.")

def save_to_file():
    with open("study_log.txt", "w") as f:
        for date, sessions in study_log.items():
            f.write(f"{date}\n")
            for s in sessions:
                f.write(f"  {s['subject']} - {s['duration']} hrs, Focus: {s['focus']}/5\n")
    print("📁 Log saved to 'study_log.txt'.")

def export_to_csv():
    with open("study_log.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Subject", "Duration (hrs)", "Focus (1-5)"])
        for date, sessions in study_log.items():
            for s in sessions:
                writer.writerow([date, s["subject"], s["duration"], s["focus"]])
    print("📄 Log exported to 'study_log.csv'.")
    
def filter_sessions():
    print("\n--- Filter Options ---")
    print("1. By subject")
    print("2. By date")
    print("3. By high focus sessions (4 or 5)")
    option = input("Choose filter type (1-3): ").strip()

    found = False
    if option == "1":
        keyword = input("Enter subject name: ").strip().title()
        for date, sessions in study_log.items():
            for s in sessions:
                if s['subject'] == keyword:
                    print(f"{date}: {s['subject']} - {s['duration']} hrs, Focus: {s['focus']}/5")
                    found = True

    elif option == "2":
        date = input("Enter date (DD-MM-YYYY): ").strip()
        if date in study_log:
            for s in study_log[date]:
                print(f"{date}: {s['subject']} - {s['duration']} hrs, Focus: {s['focus']}/5")
                found = True

    elif option == "3":
        for date, sessions in study_log.items():
            for s in sessions:
                if s['focus'] >= 4:
                    print(f"{date}: {s['subject']} - {s['duration']} hrs, Focus: {s['focus']}/5")
                    found = True

    if not found:
        print("No matching sessions found.")

def main():
    load_from_file()

    while True:
        print("\n=== Smart Study Session Logger ===")
        print("1. Log a new session")
        print("2. Show summary")
        print("3. Save log to file")
        print("4. Export log to CSV")
        print("5. Search/filter sessions")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            log_session()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            save_to_file()
        elif choice == "4":
            export_to_csv()
        elif choice == "5":
            filter_sessions()
        elif choice == "6":
            print("Goodbye and happy studying! 📚")
            break
        else:
            print("❌ Invalid option. Please try again.")

main()
