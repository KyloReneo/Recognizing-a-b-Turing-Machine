def ensure_tape_bounds():
    """
    Expands the tape to the left or right if the tapehead moves out of bounds.
    """
    global tape, tapehead
    if tapehead < 0:
        tape.insert(0, 'B')  # Extend tape on the left with a blank
        tapehead = 0
    elif tapehead >= len(tape):
        tape.append('B')     # Extend tape on the right with a blank

# The action functoin is for navigating through the tape and reading and writhing on it
def action(input_char, replace_with, move, new_state):
    """
    Performs one Turing Machine action:
    - If the current symbol under the tapehead matches `input_char`,
      it replaces it, moves the head, and sets the new state.
    """
    global tape, tapehead, state
    ensure_tape_bounds()
    if tape[tapehead] == input_char:
        tape[tapehead] = replace_with
        state = new_state
        if move == 'R':
            tapehead += 1
        elif move == 'L':
            tapehead -= 1
        ensure_tape_bounds()
        return True
    return False

# ----------- INITIALIZATION -----------

# Read user input (e.g., "aabb")
print("The goal for this Turing Machine is to accept strings in the form aⁿbⁿ (e.g., 'ab', 'aabb', 'aaabbb', etc.), where the number of 'a's is equal to the number of 'b's and all 'a's come before all 'b's.")
string = input("Enter a string (a^n b^n): ")

# Set up tape with blanks ('B') on both sides
tape = ['B'] + list(string) + ['B']
tapehead = 1  # Start after the initial blank
state = 0     # Initial state
accept = False
oldtapehead = -1  # Used to detect if the head stopped moving

# ----------- EXECUTION LOOP -----------

while oldtapehead != tapehead or state in [0, 1, 2, 3, 4]:
    oldtapehead = tapehead
    print(tape, "tapehead at", tapehead, "state", state)

    if state == 0:
        # State 0: Find first 'a' and mark it as 'X'
        # Then move right to look for a corresponding 'b'
        if action('a', 'X', 'R', 1):
            pass
        elif action('Y', 'Y', 'R', 0):
            pass  # Skip already processed 'b's
        elif action('B', 'B', 'R', 4):
            pass  # All 'a's matched, now verify only Y's remain
        else:
            break  # Unexpected symbol

    elif state == 1:
        # State 1: Move right to find the first unmatched 'b'
        if action('a', 'a', 'R', 1):  # Skip over remaining 'a's
            pass
        elif action('b', 'Y', 'L', 2):  # Found a 'b', mark it and move left
            pass
        elif action('Y', 'Y', 'R', 1):  # Skip already processed 'b's
            pass
        else:
            break

    elif state == 2:
        # State 2: Return left to the last 'X' (or beginning)
        if action('a', 'a', 'L', 2):
            pass
        elif action('Y', 'Y', 'L', 2):
            pass
        elif action('X', 'X', 'R', 0):  # Found the last 'X', loop back
            pass
        else:
            break

    elif state == 4:
        # State 4: All 'a's should be matched; scan for only 'Y's
        if action('Y', 'Y', 'R', 4):
            pass
        elif action('B', 'B', 'R', 5):  # End reached — ACCEPT
            pass
        else:
            break  # Unexpected symbol

    elif state == 5:
        # Final accepting state
        accept = True
        break

# ----------- FINAL RESULT -----------

if accept:
    print("✅ Accepted: Input matches a^n b^n and accepted on state= ", state)
else:
    print("❌ Rejected: Invalid format for a^n b^n and not accepted on state= ", state)
