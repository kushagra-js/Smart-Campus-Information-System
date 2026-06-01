import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ── GLOBAL DATA STORES ───────────────────────────────────────
records     = []   # e.g. [{"name":"Alice","id":"S101","marks":88,...}]
student_ids = []   # e.g. ["S101", "S103", "S102"]

# MODULE 1 – STUDENT REGISTRATION & GRADE EVALUATION
def register_student():
    # Step 1: collect basic details from the user
    name  = input("Enter student name: ")
    sid   = input("Enter student ID  : ")
    marks = int(input("Enter marks (0-100): "))   # convert string → int

    # Step 2: assign grade using if-elif-else ladder
    # The conditions are checked top-to-bottom; first match wins
    if   90 <= marks <= 100: grade, remark = "A",  "Excellent"
    elif marks >= 75: grade, remark = "B", "Very Good"
    elif marks >= 60: grade, remark = "C",  "Good"
    elif marks >= 40: grade, remark = "D",  "Average"
    else:             grade, remark = "F",  "Fail – Needs Improvement"

    # Step 3: build a dictionary for this student and store it
    student = {
        "name"   : name,
        "id"     : sid,
        "marks"  : marks,
        "grade"  : grade,
        "courses": []        # empty list; filled later by Module 2
    }
    records.append(student)       # add dict to the global list
    student_ids.append(sid)       # also track the ID separately

    print(f"\n  ✔ {name} | Grade: {grade} | Remark: {remark}\n")


# =============================================================
# MODULE 2 – COURSE ENROLLMENT
# Concepts used: while loop, continue (skip), break (exit loop)
# =============================================================
def enroll_courses():
    sid = input("Enter student ID to enroll courses: ")

    # Search for the student in 'records' using a generator expression
    # next() returns the first match, or None if not found
    student = next((s for s in records if s["id"] == sid), None)

    if not student:
        print("  ✘ Student not found.\n")
        return   # exit the function early

    print("  Add up to 5 courses. Type 'done' to stop early.")

    # while loop runs until 5 courses are added
    while len(student["courses"]) < 5:
        course = input(f"  Course {len(student['courses']) + 1}: ")

        if course.lower() == "done":
            break        # 'break' exits the loop immediately

        if course == "":
            continue     # 'continue' skips blank input, loops again

        student["courses"].append(course)   # add valid course name

    print(f"  ✔ Enrolled in: {', '.join(student['courses'])}\n")


# =============================================================
# MODULE 3 – DISPLAY ALL STUDENT RECORDS
# Concepts used: list iteration (for loop), f-strings, dict access
# =============================================================
def display_records():
    if not records:          # check if the list is empty
        print("  No records found.\n")
        return

    # Print a formatted header row
    print(f"\n  {'ID':<10} {'Name':<15} {'Marks':<7} {'Grade':<6} {'Courses'}")
    print("  " + "-" * 60)

    # Loop through each student dictionary in the records list
    for s in records:
        # If no courses enrolled yet, show 'None'
        courses = ", ".join(s["courses"]) if s["courses"] else "None"
        # :<10 means left-align in a field of width 10 characters
        print(f"  {s['id']:<10} {s['name']:<15} {s['marks']:<7} {s['grade']:<6} {courses}")
    print()

# =============================================================
# EVENT PARTICIPATION ANALYSIS USING SETS
# =============================================================
def event_analysis():

    event_A = {"Alice", "Bob", "Charlie", "David"}
    event_B = {"Bob", "Charlie", "Eva"}

    print("\n=== Event Participation Analysis ===")

    print("Common Participants:")
    print(event_A & event_B)

    print("\nAll Participants:")
    print(event_A | event_B)

    print("\nOnly Event A Participants:")
    print(event_A - event_B)

    print()


# =============================================================
# MODULE 4 – SORTING & SEARCHING
# Sorting  → Bubble Sort algorithm  (O(n²) time complexity)
# Searching → Linear Search algorithm (O(n) time complexity)
# =============================================================
def sort_and_search():
    if not student_ids:
        print("  No IDs to process.\n")
        return

    ids = student_ids[:]    # copy the list so original stays unchanged
    n   = len(ids)

    # ── BUBBLE SORT ──────────────────────────────────────────
    # Outer loop: n-1 passes needed
    for i in range(n - 1):
        # Inner loop: compare adjacent pairs, shrinks each pass
        for j in range(n - i - 1):
            if ids[j] > ids[j + 1]:
                # Swap if left element is greater than right
                ids[j], ids[j + 1] = ids[j + 1], ids[j]

    print(f"  Sorted IDs: {ids}")

    # ── LINEAR SEARCH ────────────────────────────────────────
    # Checks each element one-by-one from left to right
    key   = input("  Enter ID to search: ")
    found = any(x == key for x in ids)   # returns True if key exists

    print(f"  {'Linear Search : Found: ' + key if found else '✘ Not found'}\n")

    # Binary Search
    low = 0
    high = len(ids) - 1
    binary_found = False

    while low <= high:
        mid = (low + high) // 2

        if ids[mid] == key:
            binary_found = True
            break

        elif ids[mid] < key:
            low = mid + 1

        else:
            high = mid - 1

    print("  Binary Search:",
          "Found" if binary_found else "Not Found")


# =============================================================
# MODULE 5 – FEE CALCULATION
# Concepts used: function with DEFAULT (optional) arguments
# If the caller doesn't pass hostel/transport, they default to 0
# =============================================================
def calculate_fee(tuition=50000, hostel=0, transport=0, misc=2000):
    # All parameters have default values → they are optional
    total = tuition + hostel + transport + misc

    print(f"\n  Tuition:   ₹{tuition}")
    print(f"  Hostel:    ₹{hostel}")
    print(f"  Transport: ₹{transport}")
    print(f"  Misc:      ₹{misc}")
    print(f"  {'─' * 20}")
    print(f"  Total Fee: ₹{total}\n")
    return total

def fee_menu():
    # Ask user only for the parts that vary; tuition & misc use defaults
    h = int(input("  Hostel fee    (0 if day scholar)     : "))
    t = int(input("  Transport fee (0 if not applicable)  : "))
    calculate_fee(hostel=h, transport=t)   # keyword arguments


# =============================================================
# MODULE 6 – FILE HANDLING
# Concepts used: open(), write mode ("w"), read mode ("r"), with block
# The 'with' statement auto-closes the file even if an error occurs
# =============================================================
def file_handling():
    fname = "student_records.txt"   # file will be created in same folder

    # ── WRITE ────────────────────────────────────────────────
    # "w" mode creates the file if it doesn't exist; overwrites if it exists
    with open(fname, "w") as f:
        f.write("SMART CAMPUS – STUDENT REPORT\n")
        f.write("=" * 40 + "\n")
        for s in records:
            # Write one line per student
            f.write(
                f"ID:{s['id']}  Name:{s['name']}  "
                f"Marks:{s['marks']}  Grade:{s['grade']}\n"
            )
    print(f"  ✔ Records written to '{fname}'")

    # ── READ ─────────────────────────────────────────────────
    # "r" mode opens the file for reading
    with open(fname, "r") as f:
        print("\n" + f.read())   # print entire file content to screen

        if records:

            total_students = len(records)

            average_marks = sum(
                s["marks"] for s in records
            ) / total_students

            top_student = max(
                records,
                key=lambda x: x["marks"]
            )

            print("\n=== REPORT ===")
            print("Total Students :", total_students)
            print("Average Marks  :", round(average_marks, 2))
            print(
                "Top Student    :",
                top_student["name"],
                "with",
                top_student["marks"],
                "marks"
            )


# =============================================================
# MODULE 7 – PERFORMANCE ANALYSIS
# Concepts used: CSV file I/O, Pandas DataFrame, NumPy mean,
#                Matplotlib bar chart, os.path.exists()
# =============================================================
CSV_FILE = "performance.csv"   # name of the data file

def create_sample_csv():
    """Creates a sample CSV automatically if the file is missing."""
    rows = [
        ["Name",    "Maths", "Science", "English"],
        ["Alice",   88,      92,        76],
        ["Bob",     72,      65,        80],
        ["Charlie", 95,      89,        91],
        ["Diana",   60,      70,        55],
        ["Ethan",   78,      83,        88],
    ]
    # newline="" prevents extra blank lines on Windows
    with open(CSV_FILE, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"  ✔ Sample CSV '{CSV_FILE}' created.")

def performance_analysis():
    # Auto-create the CSV if it doesn't already exist
    import os
    if not os.path.exists(CSV_FILE):
        create_sample_csv()

    # ── PANDAS: load CSV into a DataFrame (like an Excel table) ──
    df = pd.read_csv(CSV_FILE)
    print(f"\n{df}\n")   # display the table

    # ── NUMPY: calculate mean for each subject column ─────────
    subjects = ["Maths", "Science", "English"]
    means    = [np.mean(df[s]) for s in subjects]

    for subject, mean_val in zip(subjects, means):
        print(f"  Mean {subject}: {mean_val:.2f}")
    print("\n=== Additional Statistics ===")

    for subject in subjects:

        print(
            f"{subject} Median:",
            np.median(df[subject])
        )

        print(
            f"{subject} Std Dev:",
            round(np.std(df[subject]), 2)
        )

    print("\n=== Top Performers ===")

    for subject in subjects:

        topper = df.loc[
            df[subject].idxmax(),
            "Name"
        ]

        print(f"{subject}: {topper}")

    # Add an 'Average' column: mean across the 3 subjects per student
    df["Average"] = df[subjects].mean(axis=1)

    # ── MATPLOTLIB: draw a bar chart ──────────────────────────
    plt.figure(figsize=(7, 4))
    plt.bar(
        df["Name"], df["Average"],
        color=["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"]
    )
    plt.title("Student Average Performance")
    plt.xlabel("Student")
    plt.ylabel("Average Marks")
    plt.tight_layout()
    plt.savefig("performance_graph.png")   # save chart as an image file
    plt.show()                             # display chart (if GUI available)
    print("  ✔ Graph saved as 'performance_graph.png'\n")


# =============================================================
# MODULE 8 – MAIN DASHBOARD (Menu Driver)
# Concepts used: dictionary mapping choices → functions,
#                while True loop, conditional branching
# =============================================================
def main():
    # Map each menu number to a (label, function) pair
    # This avoids a long if-elif chain and is easy to extend
    menu = {
        "1": ("Registration",         register_student),
        "2": ("Course Enrollment",    enroll_courses),
        "3": ("Display Records",      display_records),
        "4": ("Event Analysis",       event_analysis),
        "5": ("Sort & Search",        sort_and_search),
        "6": ("Fee Calculation",      fee_menu),
        "7": ("File Handling",        file_handling),
        "8": ("Performance Analysis", performance_analysis),
        "9": ("Exit",                 None),
    }

    # Infinite loop: keeps showing the menu until user picks Exit
    while True:
        print("\n" + "=" * 42)
        print("   🎓  SMART CAMPUS INFORMATION SYSTEM")
        print("=" * 42)

        # Print all menu options dynamically from the dictionary
        for key, (label, _) in menu.items():
            print(f"   {key}. {label}")

        print("=" * 42)
        choice = input("  Select option: ").strip()

        if choice == "9":
            print("  Goodbye! 👋\n")
            break                        # exit the while loop → program ends

        elif choice in menu:
            menu[choice][1]()            # call the function linked to the choice

        else:
            print("  ✘ Invalid choice. Please enter 1–9.\n")


# ── ENTRY POINT ──────────────────────────────────────────────
# This block runs only when the file is executed directly
# (not when imported as a module into another script)
if __name__ == "__main__":
    main()