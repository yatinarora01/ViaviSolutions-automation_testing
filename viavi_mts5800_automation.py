import socket

# Define the connection parameters
IP_ADDRESS = '10.91.11.51'  # Replace with your actual MTS-5800 IP address
PORT = 8002               # Use port 8000, 8001, or 8002 as required
TIMEOUT = 30        # Timeout for the socket connection in seconds

def send_scpi_command(command):
 
    try:
        print(f"Connecting to {IP_ADDRESS}:{PORT} with timeout {TIMEOUT} seconds")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)  # Set the timeout for the connection
            s.connect((IP_ADDRESS, PORT))  # Connect to the MTS-5800
            
            print("Connection established")
            
            # Send the *REM command to enable remote control
            s.sendall('*REM\n'.encode())
            # print("Sent *REM command")
            
            # Send the SCPI command
            s.sendall(f"{command}\n".encode())
            print(f"Sent command: {command}")
            
            # Receive the response
            response = s.recv(4096).decode().strip()
            print(f"Received response: {response}")
            return response
    
    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    
    # Now send other SCPI commands
    idn_response = send_scpi_command('*IDN?')
    print(f"Response to *IDN?: {idn_response}")

    err_response = send_scpi_command(':SYST:ERR?')
    print(f"Response to :SYST:ERR?: {err_response}")

    running_application = send_scpi_command(':SYST:APPL:CAPP?')
    print(f"Response to running application on ports: {running_application}")

# # Extract the specific application name (assuming it's the first one listed)
#     application_to_run = running_application.split(',')[0]  # Adjust as needed to select the correct application

# # Run the selected application
#     run_application = send_scpi_command(f':SYST:APPL:SEL {application_to_run}')
#     print(f"Response to running {application_to_run}: {run_application}")

    err_checkone  = send_scpi_command(':SYST:ERR?')
    print(f"Error 1 response : {err_checkone}")

    # create_sessionone = send_scpi_command(':SESS:CRE')
    # print(f"Session created ?: {create_sessionone}")

    # data_sens = send_scpi_command(':SESS:STAR Word file has a screen shot here showing :SENS:DATA?')
    # print(f"Session? : {data_sens}")

    # laser_on = send_scpi_command(':OUTPUT:OPTIC')
    # print(f"Laser on : {laser_on}")

#     payload_bert = send_scpi_command(':SOURCE:MAC:ETH:PAYLOAD BERT')
#     print(f"changed to : {payload_bert}")

#     err_checktwo = send_scpi_command(':SYST:ERR?')
#     print(f"Any Error? :{err_checktwo}")


    exit_one =send_scpi_command(':EXIT')
    print(f"Session Exit {exit_one}")

    err_checkthree = send_scpi_command(':SYST:ERR?')
    print(f"Any Error? :{err_checkthree}")


    # run_application = send_scpi_command()
    
