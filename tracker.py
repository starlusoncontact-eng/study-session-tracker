import math

def show_welcome():
    print("Welcome to Study Session Tracker!")


def read_topic():
    while True:
        topic_question = input("What topic did you study today?").strip()
        if not topic_question:
            print("Error: topic cannot be empty")
        elif len(topic_question) > 50:
            print("Error: topic is too long")
        elif "|" in topic_question:
            print("Error: topic cannot contain |")
        else:
            return topic_question


def read_minutes():
    while True:
        try:
            minutes_question = float(input("How much time in minutes did you study?"))
            if not math.isfinite(minutes_question):
                print("Error: enter a valid number")
            elif minutes_question <= 0:
                print("Error: cannot be 0 or less")
            elif minutes_question > 1440:
                print("Error: cannot be more than 1440 minutes")
            else:
                return minutes_question
        except ValueError:
            print("Error: enter a valid number")


def read_note():
    while True:
        note_question = input("Short note (optional):").strip()
        if len(note_question) > 100:
            print("Error: note is too long")
        elif "|" in note_question:
            print("Error: note cannot contain |")
        else:
            return note_question


def create_session():
    topic_question = read_topic()
    minutes_question = read_minutes()
    note_question = read_note()

    session = {
        "topic": topic_question,
        "minutes": minutes_question,
        "note": note_question,
    }
    return session


def calculate_total_minutes(sessions):
    total = 0
    for session in sessions:
        total += session['minutes']
    return total


def show_statistics(sessions):

    if not sessions:
        print("No sessions recorded")
        return

    total_minutes = calculate_total_minutes(sessions)
    total_sessions = len(sessions)
    total_hours = total_minutes/60
    longest_minutes = sessions[0]['minutes']
    longest_topic = sessions[0]['topic']
    shortest_minutes = sessions[0]['minutes']
    shortest_topic = sessions[0]['topic']

    for session in sessions:
        if session['minutes'] > longest_minutes:
            longest_minutes = session['minutes']
            longest_topic = session['topic']    
            
        if session['minutes'] < shortest_minutes:
            shortest_minutes = session['minutes']
            shortest_topic = session['topic']
    print(f"Shortest of all sessions: {shortest_minutes:g}")
    print(f"Shortest of all topics: {shortest_topic}")
    print(f"Longest of all sessions: {longest_minutes:g}")
    print(f"Longest of all topics: {longest_topic}")
   
    average_minutes = total_minutes/total_sessions
    print(f"Average duration of sessions: {average_minutes:.1f}")
    print(f"Total minutes of all sessions: {total_minutes:g}")
    print(f"Total hours of all sessions: {total_hours:.2f}")
    print(f"Total amount of all sessions: {total_sessions}")


def show_sessions(sessions):
    if not sessions:
        print("No sessions recorded")
        return

    for number, session in enumerate(sessions, start = 1):
        print(f"Session {number}: {session['topic']}, {session['minutes']:g}")
        if session['note']:
            print(f"Session note: {session['note']}")


def search_sessions(sessions, keyword):
    found = False
    for session in sessions:
        if keyword.lower() in session['topic'].lower():
            found = True
            print(f"Result: {session['topic']} - {session['minutes']:g} minutes")
    if not found:
        print("No matching sessions found")


def edit_session(sessions):
    if not sessions:
        print("No sessions recorded")
        return
    show_sessions(sessions)
    
    try:
        session_number = int(input("Write a session number: "))
        if session_number < 1 or session_number > len(sessions):
            print("Error: session not found")
            return
    except ValueError:
        print("Error: enter a valid number")
        return

    session = sessions[session_number - 1]


    edit_choice = input("""1. Edit topic
2. Edit minutes
3. Edit note
Choose an option: """).strip()

    if edit_choice == '1':
        new_topic = read_topic()
        session['topic'] = new_topic
        print("Topic updated successfully")

    elif edit_choice =='2':
        new_minutes = read_minutes()
        session['minutes'] = new_minutes
        print("Minutes updated successfully")

    elif edit_choice == '3': 
        new_note = read_note()
        session['note'] = new_note
        print("Note updated successfully")   

    else:
        print("Error: choose a number from 1 to 3")
        return

    print(f"Result: {session['topic']}, {session['minutes']:g}, {session['note']}")
    save_sessions(sessions)
   
    
    


def delete_session(sessions):
    if not sessions:
        print("No sessions recorded")
        return
    show_sessions(sessions)

    try:
        session_number = int(input("Write a session number: "))
        if session_number < 1 or session_number > len(sessions):
            print("Error: session not found")
            return
    except ValueError:
        print("Error: enter a valid number")
        return

    while True:
        delete_question = input("Delete this session? (yes/no):").strip().lower()
        if delete_question == 'yes':
            sessions.pop(session_number - 1)
            save_sessions(sessions)
            print("Session deleted successfully")
            return
        elif delete_question == 'no':
            print("Deletion cancelled")
            return
        else:
            print("Error: enter yes or no")
        



def show_menu():
    print("""=== Main Menu ===
1. Add session
2. Show sessions
3. Search sessions
4. Show statistics
5. Exit
6. Edit session
7. Delete session""")


def save_sessions(sessions):
    with open("sessions.txt", "w", encoding="utf-8") as file:
        for session in sessions:
            file.write(f"{session['topic']}|{session['minutes']}|{session['note']}\n")

def load_sessions():
    sessions = []
    try:
        with open("sessions.txt", "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) != 3:
                    print("Error: invalid session data")
                    continue
                
                try:
                    minutes = float(parts[1])
                except ValueError:
                    print("Error: invalid session data")
                    continue

                if not math.isfinite(minutes) or minutes <= 0 or minutes > 1440:
                    print("Error: invalid session data")
                    continue

                if not parts[0] or len(parts[0]) > 50 or len(parts[2]) > 100:
                    print("Error: invalid session data")
                    continue

                session = {
                    "topic": parts[0],
                    "minutes": minutes,
                    "note": parts[2],
                }
                sessions.append(session)
    except FileNotFoundError:
        print("No saved sessions found")
    return sessions


sessions = load_sessions()
show_welcome()

while True:
    show_menu()
    choice = input("Choose the action:").strip()

    if choice == '5':
        break
    elif choice not in ['1', '2', '3', '4', '5', '6', '7']:
        print("Error: choose a number from 1 to 7")
    elif choice == '1':
        session = create_session()
        sessions.append(session)
        save_sessions(sessions)
        print("Session added successfully")
    elif choice == '2':
        show_sessions(sessions)
    elif choice == '4':
        show_statistics(sessions)
    elif choice == '3':
        while True:
            search_console = input("Write a word for search: ").strip()
            if not search_console:
                print("Error: cannot be empty")
                continue
            elif search_console.lower() == 'exit':
                break
            else:
                search_sessions(sessions, search_console)
    elif choice == '6':
        edit_session(sessions)
    elif choice == '7':
        delete_session(sessions)











    




