import re

def adjust_time(timestamp, offset_ms):
    # Convert timestamp to hours, minutes, seconds, and milliseconds
    hours, minutes, seconds, milliseconds = map(int, re.split(r'[:,]', timestamp))
    total_ms = (hours * 3600000 + minutes * 60000 + seconds * 1000 + milliseconds) + offset_ms

    if total_ms < 0:
        total_ms = 0  # Prevent negative times

    # Convert back to hours, minutes, seconds, milliseconds
    new_hours = total_ms // 3600000
    total_ms %= 3600000
    new_minutes = total_ms // 60000
    total_ms %= 60000
    new_seconds = total_ms // 1000
    new_milliseconds = total_ms % 1000

    return f"{new_hours:02}:{new_minutes:02}:{new_seconds:02},{new_milliseconds:03}"

def adjust_srt_file(file_name, seconds_offset):
    offset_ms = int(seconds_offset * 1000)  # Convert seconds to milliseconds

    try:
        with open(file_name, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate()  # Clear the file for writing updated content

            for line in lines:
                match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line)
                if match:
                    start_time, end_time = match.groups()
                    new_start = adjust_time(start_time, offset_ms)
                    new_end = adjust_time(end_time, offset_ms)
                    file.write(f"{new_start} --> {new_end}\n")
                else:
                    file.write(line)

        print(f"Subtitle times adjusted by {seconds_offset} seconds in '{file_name}'.")
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main execution
if __name__ == "__main__":
    file_name = input("Enter the name of the subtitle file (e.g., abc.srt): ").strip()
    try:
        time_offset = float(input("Enter time adjustment in seconds (use + or -): "))
        adjust_srt_file(file_name, time_offset)
    except ValueError:
        print("Invalid input! Please enter a number (e.g., +2.5 or -1.2).")
