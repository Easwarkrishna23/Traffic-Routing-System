import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure the use of the TkAgg backend
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate RSA keys and make them global
public_key = None
private_key = None

def generate_keys():
    global public_key, private_key
    key = RSA.generate(2048)  # Generate a pair of RSA keys
    private_key = key.export_key()  # Export private key
    public_key = key.publickey().export_key()  # Export public key

generate_keys()  # Call the function to generate the keys

# Function to calculate the shortest path using Dijkstra's algorithm
def calculate_shortest_path():
    source = source_entry.get().strip()  # Get the source entered by the user
    destination = destination_entry.get().strip()  # Get the destination entered by the user

    # Define the road network as a graph
    graph_data = [
        ('A', 'B', 4), ('A', 'C', 2), 
        ('B', 'C', 1), ('B', 'D', 5), 
        ('C', 'D', 8), ('C', 'E', 10), 
        ('D', 'E', 2)
    ]
    
    # Create the graph
    G = nx.DiGraph()
    G.add_weighted_edges_from(graph_data)  # Add the weighted edges (road distances)

    try:
        # Find the shortest path and distance using Dijkstra's algorithm
        path = nx.dijkstra_path(G, source=source, target=destination)
        distance = nx.dijkstra_path_length(G, source=source, target=destination)
        result_label.config(text=f"Shortest Path: {path}, Distance: {distance} units")

        # Draw the graph with matplotlib
        pos = nx.spring_layout(G)  # Define layout for nodes
        plt.figure(figsize=(8, 8))  # Define size of the figure
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=15, font_weight='bold', edge_color='gray')

        # Highlight the shortest path in red
        path_edges = list(zip(path, path[1:]))  # Get edges from the path
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=3)  # Highlight the shortest path

        # Show the graph
        plt.title("Traffic Network with Shortest Path")
        plt.show()  # Display the graph

    except nx.NetworkXNoPath:
        result_label.config(text="No path found between the source and destination.")  # If no path exists
    except nx.NodeNotFound:
        result_label.config(text="Invalid source or destination.")  # If nodes are not found

# Function to encrypt the message using the public key
def encrypt_message():
    global public_key
    message = message_entry.get().strip()  # Get the message entered by the user
    if not message:
        encrypted_label.config(text="Please enter a valid message.")
        return

    rsa_key = RSA.import_key(public_key)  # Import the public key
    cipher = PKCS1_OAEP.new(rsa_key)  # Initialize the cipher
    encrypted_msg = cipher.encrypt(message.encode())  # Encrypt the message
    encrypted_label.config(text=f"Encrypted Message: {encrypted_msg.hex()}")  # Display the encrypted message as hex

# Function to decrypt the message using the private key
def decrypt_message():
    global private_key
    encrypted_msg_hex = encrypted_label.cget("text").replace("Encrypted Message: ", "").strip()  # Get encrypted message in hex
    if not encrypted_msg_hex:
        decrypted_label.config(text="No message to decrypt.")
        return

    encrypted_msg = bytes.fromhex(encrypted_msg_hex)  # Convert hex back to bytes
    rsa_key = RSA.import_key(private_key)  # Import the private key
    cipher = PKCS1_OAEP.new(rsa_key)  # Initialize the cipher
    decrypted_msg = cipher.decrypt(encrypted_msg)  # Decrypt the message
    decrypted_label.config(text=f"Decrypted Message: {decrypted_msg.decode('utf-8')}")  # Display the decrypted message

# Create the main window for the GUI
window = tk.Tk()
window.title("Traffic Routing and Secure Communication")

# Traffic Routing Section
tk.Label(window, text="Traffic Routing System", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)
tk.Label(window, text="Source:").grid(row=1, column=0, sticky="e")
source_entry = tk.Entry(window)
source_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(window, text="Destination:").grid(row=2, column=0, sticky="e")
destination_entry = tk.Entry(window)
destination_entry.grid(row=2, column=1, padx=5, pady=5)

# Button to calculate the shortest route
tk.Button(window, text="Calculate Route", command=calculate_shortest_path).grid(row=3, column=1, pady=10)
result_label = tk.Label(window, text="")
result_label.grid(row=4, columnspan=2, pady=5)

# Encryption Section
tk.Label(window, text="Secure Communication", font=("Arial", 16)).grid(row=5, columnspan=2, pady=10)
tk.Label(window, text="Message:").grid(row=6, column=0, sticky="e")
message_entry = tk.Entry(window, width=40)
message_entry.grid(row=6, column=1, padx=5, pady=5)

# Button to encrypt the message
tk.Button(window, text="Encrypt Message", command=encrypt_message).grid(row=7, column=1, pady=5)
encrypted_label = tk.Label(window, text="", wraplength=400)
encrypted_label.grid(row=8, columnspan=2, pady=5)

# Button to decrypt the message
tk.Button(window, text="Decrypt Message", command=decrypt_message).grid(row=9, column=1, pady=5)
decrypted_label = tk.Label(window, text="", wraplength=400)
decrypted_label.grid(row=10, columnspan=2, pady=5)

# Start the Tkinter GUI loop
window.mainloop()
