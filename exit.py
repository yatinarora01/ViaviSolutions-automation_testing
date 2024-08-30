import socket
import time

# Function to send SCPI commands and receive responses
def send_scpi_command(command, sock):
    try:
        sock.sendall((command + '\n').encode())
        response = sock.recv(4096).decode().strip()
        return response
    except socket.timeout:
        return "Error: timed out"

# Connect to the MTS-5800 device
def connect_to_device(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((ip, port))
    return sock

# IP and port configuration
device_ip = "10.91.11.51"

# Common commands that should always execute on port 8002
common_commands = [
    "*REM VISIBLE FULL",
    "*IDN?",
    ":SESS:CRE",
    ":SESS:STAR",
]

# Mapping of commands to ports
command_port_mapping = {
    8000: [
        "*REM",
        "*IDN?",
        "MOD:FUNC:LIST? BOTH,BASE",
        "MOD:FUNC:PORT? BOTH,BASE,\"BERT\"",
    ],
    8001: [
        "*REM",
        "*IDN?",
        ":SYST:FUNC:PORT? BOTH,BASE,\"BERT\"",
    ],
    8002: []  # To be filled dynamically based on user selection
}

# Function to execute commands for a given port
def execute_commands_for_port(port):
    if port not in command_port_mapping:
        print(f"No commands configured for port {port}")
        return
    
    commands = command_port_mapping[port]
    
    # Establish connection to the port
    sock = connect_to_device(device_ip, port)
    print(f"Connected to port {port}")
    
    # Send each command and print the response
    for command in commands:
        response = send_scpi_command(command, sock)
        # Only show the response if it is not a timeout error
        if response != "Error: timed out":
            print(f"Response: {response}\n")
        
        # Pause after launching the application to allow it to settle down
        if ":SYST:APPL:LAUNch" in command:
            print("Application launched. Waiting 30 seconds for it to settle down...")
            time.sleep(30)
    
    # Close the connection to the port
    sock.close()
    print(f"Connection to port {port} closed\n")

# Function to handle direct and timed testing options for port 8002
def handle_port_8002_testing():
    while True:
        print("Select the testing option for port 8002:")
        print("1. Direct Testing")
        print("2. Timed Testing")
        user_choice = input("Enter the number of the option (or 'exit' to quit): ")

        if user_choice == "1":
            handle_direct_testing()

        elif user_choice == "2":
            handle_timed_testing()

        elif user_choice.lower() == "exit":
            print("Exiting program.")
            break

        else:
            print("Invalid selection. Please try again.")

# Function to turn on laser and start traffic
def turn_on_laser_and_traffic():
    return [
        ":OUTPUT:OPTIC ON",  # Turn on laser
        ":SOURCE:MAC:ETH:PAYLOAD BERT",  # Set Payload
        ":SOURCE:MAC:ETH:PAYLOAD?",  # Confirm Payload
        ":SOURCE:MAC:TRAFFIC ON",  # Start Traffic
        ":ABOR",
        ":INIT",
    ]

# Function to handle direct testing
def handle_direct_testing():
    print("Select the application for Direct Testing on port 8002:")
    print("1. TermEth10GL2Traffic")
    print("2. TermEth100GL2Traffic")
    app_choice = input("Enter the number of the application (or 'exit' to quit): ")

    if app_choice == "1":
        specific_commands = [
            ":SYST:APPL:LAUNch TermEth10GL2Traffic 2",
            ":SYST:APPL:SEL TermEth10GL2Traffic_102",
        ] + turn_on_laser_and_traffic()

    elif app_choice == "2":
        specific_commands = [
            ":SYST:APPL:LAUNch TermEth100GL2Traffic 1",
            ":SYST:APPL:SEL TermEth100GL2Traffic_101",
        ] + turn_on_laser_and_traffic()

    elif app_choice.lower() == "exit":
        print("Exiting Direct Testing.")
        return

    else:
        print("Invalid application selection. Exiting Direct Testing.")
        return

    # Set up for direct testing
    setup_commands = [":SENSE:TEST:ENABLE OFF"]

    # Always execute common commands first
    command_port_mapping[8002] = common_commands + specific_commands + setup_commands
    execute_commands_for_port(8002)
    save_test_results()

# Function to handle timed testing
def handle_timed_testing():
    print("Select the application for Timed Testing on port 8002:")
    print("1. TermEth10GL2Traffic")
    print("2. TermEth100GL2Traffic")
    app_choice = input("Enter the number of the application (or 'exit' to quit): ")

    if app_choice == "1":
        specific_commands = [
            ":SYST:APPL:LAUNch TermEth10GL2Traffic 2",
            ":SYST:APPL:SEL TermEth10GL2Traffic_102",
        ] + turn_on_laser_and_traffic()

    elif app_choice == "2":
        specific_commands = [
            ":SYST:APPL:LAUNch TermEth100GL2Traffic 1",
            ":SYST:APPL:SEL TermEth100GL2Traffic_101",
        ] + turn_on_laser_and_traffic()

    elif app_choice.lower() == "exit":
        print("Exiting Timed Testing.")
        return

    else:
        print("Invalid application selection. Exiting Timed Testing.")
        return

    # Set up for timed testing
    setup_commands = [
        ":SENSE:TEST:ENABLE ON",  # Enable timed testing
        ":SENSE:TEST:DURATION 100MIN",
    ]

    # Always execute common commands first
    command_port_mapping[8002] = common_commands + specific_commands + setup_commands
    execute_commands_for_port(8002)
    wait_for_test_completion()
    save_test_results()

# Function to wait for test completion by checking the status or using a time gap
def wait_for_test_completion():
    print("Waiting for timed test to complete...")
    test_duration = 140  # Assuming 100 minutes duration
    time.sleep(test_duration)  # Wait for the entire duration of the test

    # Alternatively, check test status via SCPI commands periodically
    # This is a placeholder approach and should be replaced with the actual method to check test status if available
    # sock = connect_to_device(device_ip, 8002)
    # while True:
    #     status = send_scpi_command(":SENSE:TEST:STATUS?", sock)
    #     if "COMPLETED" in status:
    #         break
    #     time.sleep(60)  # Check every minute
    # sock.close()

# Function to save test results and display file location
def save_test_results():
    print("Saving test results...")
    sock = connect_to_device(device_ip, 8002)
    
    # Send commands to save test results
    save_command = ":SYST:FILE:SAVE 'test_results'"
    response = send_scpi_command(save_command, sock)
    if response == "Error: timed out":
        print("Error: Saving test results timed out. Retrying...")
        response = send_scpi_command(save_command, sock)
    
    if response == "Error: timed out":
        print("Failed to save test results after retry.")
    else:
        # Retrieve and display the location of the saved file
        file_location_command = ":SYST:FILE:PATH? 'test_results'"
        file_location = send_scpi_command(file_location_command, sock)
        print(f"Test results saved at: {file_location}")
    
    # End session
    end_session(sock)
    sock.close()

# Function to end session
def end_session(sock):
    end_command = ":SESS:STOP"
    response = send_scpi_command(end_command, sock)
    print(f"Session ended: {response}")

# Function to exit an application
def exit_application():
    print("Which application would you like to exit?")
    print("1. TermEth10GL2Traffic")
    print("2. TermEth100GL2Traffic")
    exit_choice = input("Enter the number of the application to exit (or 'exit' to quit): ")

    if exit_choice == "1" or exit_choice == "2":
        command_port_mapping[8002] = common_commands + [":EXIT"]
        execute_commands_for_port(8002)
    elif exit_choice.lower() == "exit":
        print("Exiting program.")
    else:
        print("Invalid application selection. Exiting.")

# Main program loop
if __name__ == "__main__":
    while True:
        print("Select an option:")
        print("1. Run Tests")
        print("2. Exit Application")
        print("3. Quit")
        user_selection = input("Enter the number of the option: ")

        if user_selection == "1":
            handle_port_8002_testing()

        elif user_selection == "2":
            exit_application()

        elif user_selection == "3":
            print("Exiting program.")
            break

        else:
            print("Invalid selection. Please try again.")
