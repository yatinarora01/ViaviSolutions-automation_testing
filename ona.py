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
device_ip = "10.91.11.80"

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
    8002: []
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

# Function to handle direct testing
def handle_direct_testing():
    print("Select the application for Direct Testing on port 8002:")
    print("1. TermEth400GL2TrafficwOtherRate")
    print("2. TermEth100GL2Traffic")
    app_choice = input("Enter the number of the application (or 'exit' to quit): ")

    if app_choice == "1":
        command_port_mapping[8002] = [
            "*REM VISIBLE FULL",
            "*IDN?",
            ":SENSE:TEST:ENABLE OFF",  # Disable timed testing
            ":SYST:APPL:LAUNch TermEth400GL2TrafficwOtherRate 2",
            ":SYST:APPL:SEL TermEth400GL2TrafficwOtherRate_102",
            ":SESS:CRE",
            ":SESS:STAR",
            ":OUTPUT:OPTIC",
            ":SOURCE:MAC:TRAFFIC",
            ":SOURCE:MAC:ETH:PAYLOAD BERT",
            ":SOURCE:MAC:ETH:PAYLOAD?",
            ":SENS:DATA? ECOUNT:PAYLOAD:BERT:TSE",
            ":SOURCE:PAYLOAD:BERT:TSE:TYPE?",
            ":SOURCE:PAYLOAD:BERT:INSERT:TSE",
            ":SENS:DATA? ECOUNT:PAYLOAD:BERT:TSE",
            ":SENS:DATA? ERATE:PAYLOAD:BERT:TSE",
            ":SESS:END",
            ":SYST:ERR?",
        ]

    elif app_choice == "2":
        command_port_mapping[8002] = [
            "*REM VISIBLE FULL",
            "*IDN?",
            ":SENSE:TEST:ENABLE OFF",  # Disable timed testing
            ":SYST:APPL:LAUNch TermEth100GL2Traffic 1",
            ":SYST:APPL:SEL TermEth100GL2Traffic_101",
            ":SESS:CRE",
            ":SESS:STAR",
            ":OUTPUT:OPTIC",
            ":SOURCE:MAC:TRAFFIC",
            ":SOURCE:MAC:ETH:PAYLOAD BERT",
            ":SOURCE:MAC:ETH:PAYLOAD?",
            ":SENS:DATA? ECOUNT:PAYLOAD:BERT:TSE",
            ":SOURCE:PAYLOAD:BERT:TSE:TYPE?",
            ":SOURCE:PAYLOAD:BERT:INSERT:TSE",
            ":SENS:DATA? ECOUNT:PAYLOAD:BERT:TSE",
            ":SENS:DATA? ERATE:PAYLOAD:BERT:TSE",
            ":SESS:END",
            ":SYST:ERR?",
        ]

    elif app_choice.lower() == "exit":
        print("Exiting Direct Testing.")
        return

    else:
        print("Invalid application selection. Exiting Direct Testing.")
        return

    execute_commands_for_port(8002)

# Function to handle timed testing
def handle_timed_testing():
    print("Select the application for Timed Testing on port 8002:")
    print("1. TermEth400GL2TrafficwOtherRate")
    print("2. TermEth100GL2Traffic")
    app_choice = input("Enter the number of the application (or 'exit' to quit): ")

    if app_choice == "1":
        command_port_mapping[8002] = [
            "*REM VISIBLE FULL",
            "*IDN?",
            ":SYST:APPL:LAUNch TermEth400GL2TrafficwOtherRate 2",
            ":SYST:APPL:SEL TermEth400GL2TrafficwOtherRate_102",
            ":SESS:CRE",
            ":SESS:STAR",
            ":OUTPUT:OPTIC",
            ":SOURCE:MAC:TRAFFIC",
            ":SOURCE:MAC:ETH:PAYLOAD BERT",
            ":SOURCE:MAC:ETH:PAYLOAD?",
            ":SENS:DATA? ECOUNT:PAYLOAD:BERT:TSE",
            ":SOURCE:PAYLOAD:BERT:TSE:TYPE?",
            ":SOURCE:PAYLOAD:BERT:INSERT:TSE",
            ":SENS:DATA? ECOUNT:PAYLOAD:BERT:TSE",
            ":SENS:DATA? ERATE:PAYLOAD:BERT:TSE",
            ":SENSE:TEST:ENABLE ON",  # Enable timed testing
            ":SENSE:TEST:DURATION 100MIN",
            ":SESS:END",
            ":SYST:ERR?",
        ]

    elif app_choice == "2":
        command_port_mapping[8002] = [
            "*REM VISIBLE FULL",
            "*IDN?",
            ":SYST:APPL:LAUNch TermEth100GL2Traffic 1",
            ":SYST:APPL:SEL TermEth100GL2Traffic_101",
            ":SESS:CRE",
            ":SESS:STAR",
            ":OUTPUT:OPTIC",
            ":SOURCE:MAC:TRAFFIC",
            ":SOURCE:MAC:ETH:PAYLOAD BERT",
            ":SOURCE:MAC:ETH:PAYLOAD?",
            ":SENS:DATA? ECOUNT:PAYLOAD:BERT:TSE",
            ":SOURCE:PAYLOAD:BERT:TSE:TYPE?",
            ":SOURCE:PAYLOAD:BERT:INSERT:TSE",
            ":SENS:DATA? ECOUNT:PAYLOAD:BERT:TSE",
            ":SENS:DATA? ERATE:PAYLOAD:BERT:TSE",
            ":SENSE:TEST:ENABLE ON",  # Enable timed testing
            ":SENSE:TEST:DURATION 100MIN",
            ":SESS:END",
            ":SYST:ERR?",
        ]

    elif app_choice.lower() == "exit":
        print("Exiting Timed Testing.")
        return

    else:
        print("Invalid application selection. Exiting Timed Testing.")
        return

    execute_commands_for_port(8002)

# Function to exit an application
def exit_application():
    print("Which application would you like to exit?")
    print("1. TermEth400GL2TrafficwOtherRate")
    print("2. TermEth100GL2Traffic")
    exit_choice = input("Enter the number of the application to exit (or 'exit' to quit): ")

    if exit_choice == "1" or exit_choice == "2":
        command_port_mapping[8002] = [":SESS:END", ":EXIT"]
        execute_commands_for_port(8002)

    elif exit_choice.lower() == "exit":
        print("Exiting program.")
    else:
        print("Invalid selection. Exiting program.")

# Execute commands for ports 8000 and 8001
execute_commands_for_port(8000)
execute_commands_for_port(8001)

# Run the port 8002 testing options
handle_port_8002_testing()

# Ask the user if they want to exit an application
exit_application()
