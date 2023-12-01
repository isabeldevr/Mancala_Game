def leaderboard_append(name, points):
    """ Append a new record to the leaderboard
    Input: name (str) - the name of the player
           points (int) - the number of points the player has
    Output: None """
    file_path = "leaderboard.txt"
    name = ''.join([char for char in name if char != ' '])

    try:
        # Opening a file in write mode
        with open(file_path, 'a') as file:
            # Writing new content to the file
            file.write(f"{name} {points}\n")

    except Exception as e:
        print(f"Error appending to leaderboard: {e}")

def leaderboard_read():
    """ Read the leaderboard
    Input: None
    Output: records (list) - a list of records """
    file_path = "leaderboard.txt"
    try:
        # Creating an empty list to store the records
        records = []
        with open(file_path, 'r') as file:
            for line in file:
                # We split each line into name and points using whitespace as a separator
                name, points = line.strip().split()
                records.append((name, int(points)))
            return records

    except Exception as e:
        print(f"Error reading leaderboard: {e}")
        return []

def merge_sort(records) -> list:
    """ Sort a list of records using merge sort
    Input: records (list) - a list of records
    Output: sorted_records (list) - a sorted list of records """
    if len(records) <= 1:
        return records

    # Split the list in two
    mid = len(records) // 2
    left_half = records[:mid]
    right_half = records[mid:]

    # Recursively sort each half
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    # Merge the halves
    sorted_records = merge(left_half, right_half)
    return sorted_records

def merge(left, right) -> list:
    """ Merge two sorted lists
    Input: left (list) - the left half
           right (list) - the right half """
    merged = []
    i = j = 0

    # Compare the elements of the two halves
    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Add the remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def leaderboard_display(points) -> None:
    """ Display the leaderboard
    Input: points (int) - the number of points the player has
    Output: None """
    name = str(input("Enter your name: "))
    leaderboard_append(name, points)
    records = leaderboard_read()
    sorted_records = merge_sort(records)
    print("Leaderboard:")
    for i, record in enumerate(sorted_records):
        print(f"{i+1}. {record[0]}: {record[1]} points")
