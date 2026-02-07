from socket import *
import ssl
import base64

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.gmail.com"  #Fill in start - Using Gmail for bonus points #Fill in end
serverPort = 587  # Port for STARTTLS

# Your email credentials (you'll need to use an App Password for Gmail)
fromAddress = "18707113952xy@gmail.com"  # Replace with your Gmail address
toAddress = "xy_1895@outlook.com"  # Replace with recipient email
password = "fcdyjgotnzjvnlnt"  # Replace with your Gmail App Password

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort))


recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())

recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send STARTTLS command to initiate TLS encryption (required for Gmail)
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
recv_tls = clientSocket.recv(1024).decode()
print(recv_tls)

if recv_tls[:3] != '220':
    print('220 reply not received for STARTTLS.')
    
# Wrap the socket with SSL/TLS
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)
print("TLS connection established")

# Send EHLO again after STARTTLS
ehloCommand = 'EHLO Alice\r\n'
clientSocket.send(ehloCommand.encode())
recv_ehlo = clientSocket.recv(1024).decode()
print(recv_ehlo)

# Authenticate with the server (required for Gmail)
authCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
recv_auth = clientSocket.recv(1024).decode()
print(recv_auth)

# Send username (base64 encoded)
clientSocket.send((base64.b64encode(fromAddress.encode()) + b'\r\n'))
recv_user = clientSocket.recv(1024).decode()
print(recv_user)

# Send password (base64 encoded)
clientSocket.send((base64.b64encode(password.encode()) + b'\r\n'))
recv_pass = clientSocket.recv(1024).decode()
print(recv_pass)

if recv_pass[:3] != '235':
    print('Authentication failed.')

# Send MAIL FROM command and print server response.
mailFromCommand = f'MAIL FROM:<{fromAddress}>\r\n'
clientSocket.send(mailFromCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)

if recv2[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
# Fill in start
rcptToCommand = f'RCPT TO:<{toAddress}>\r\n'
clientSocket.send(rcptToCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)

if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)

if recv4[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
# Create email headers
subject = "Test Email from SMTP Client"
headers = f"From: {fromAddress}\r\n"
headers += f"To: {toAddress}\r\n"
headers += f"Subject: {subject}\r\n"
headers += "\r\n"  # Empty line separates headers from body

# Send headers and message body
clientSocket.send(headers.encode())
clientSocket.send(msg.encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)

if recv5[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)

if recv6[:3] != '221':
    print('221 reply not received from server.')
    
clientSocket.close()
print("\nEmail sent successfully!")