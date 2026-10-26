from terminal import run_command

print("\n--- Test 1: Safe command ---")
print(run_command(["echo", "Jay is working"]))

print("\n--- Test 2: Dangerous command ---")
print(run_command(["sudo", "rm", "text.txt"]))
