# Psuedo Code
"""
FUNCTION hanoi_solver(total_disks)
    // 1. Initialize the three rods
    // Rod A starts with disks from total_disks down to 1 (e.g., [3, 2, 1])
    rod_A = list containing numbers from total_disks down to 1
    rod_B = empty list
    rod_C = empty list
    
    // 2. Initialize a list or string to capture the history of states
    moves_history = empty list of strings
    
    // Helper function to format the current state of the rods
    FUNCTION capture_state()
        // Format the rods exactly as "[A] [B] [C]"
        state_string = string representation of rod_A + " " + 
                       string representation of rod_B + " " + 
                       string representation of rod_C
        append state_string to moves_history
    END FUNCTION

    // Capture the initial starting arrangement
    capture_state()

    // 3. Define the recursive helper function to move the disks
    FUNCTION move_disks(n, source, target, auxiliary)
        // Base case: If there are no disks to move, stop
        IF n == 0 THEN
            RETURN
        END IF

        // Step A: Move n-1 disks from source to auxiliary
        move_disks(n - 1, source, auxiliary, target)

        // Step B: Move the top disk from source to target
        disk = remove last element from source
        append disk to target
        
        // Capture the state immediately after the move
        capture_state()

        // Step C: Move the n-1 disks from auxiliary to target
        move_disks(n - 1, auxiliary, target, source)
    END FUNCTION

    // 4. Kick off the recursion
    // We want to move all 'total_disks' from rod_A to rod_C, using rod_B as auxiliary
    move_disks(total_disks, rod_A, rod_C, rod_B)

    // 5. Join the history list into a single string separated by newlines and return it
    RETURN join moves_history with newline characters
END FUNCTION
"""

def hanoi_solver(total_disks: int) -> str:
    rod_A = list(range(total_disks, 0, -1))
    rod_B = []
    rod_C = []

    moves_history = []

    def capture_state():
        state_string = f'{str(rod_A)} {str(rod_B)} {str(rod_C)}'
        moves_history.append(state_string)

    capture_state()

    def move_disks(n, source, target, aux):
        if n == 0:
            return

        move_disks(n - 1, source, aux, target)

        disk = source.pop()
        target.append(disk)

        capture_state()

        move_disks(n - 1, aux, target, source)
    
    move_disks(total_disks, rod_A, rod_C, rod_B)

    return '\n'.join(moves_history)

if __name__ == "__main__":
    output = hanoi_solver(3)
    print(output)
