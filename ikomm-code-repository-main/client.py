import os
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import socket
import threading
import time
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import dns.resolver
import dns.message
import dns.query
import dns.exception

# Added for higher DPI setting
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

# Global variables
dns_resolution_listbox = None
message_listbox = None
messages_listbox = None
rtt_result = None
image_label = None
proj_messages_listbox = None

temp_values = []
humidity_values = []
pressure_values = []

combined_plot = None
scatter_plot = None
bar_plot = None
heatmap_plot = None


class EncodingSettings:
    """Class to manage encoding settings for UDP and TCP communication."""

    udp_encoding = "utf-8"
    tcp_encoding = "utf-8"

    @classmethod
    def update_udp_encoding(cls, selection):
        """
        Update the UDP encoding selection.

        :param selection: The selected encoding (e.g. "utf-8", "ascii")
        """
        cls.udp_encoding = selection

    @classmethod
    def update_tcp_encoding(cls, selection):
        """
        Update the TCP encoding selection.

        :param selection: The selected encoding (e.g. "utf-8", "ascii")
        """
        cls.tcp_encoding = selection


class UDPClient:
    """Class to handle UDP client operations."""

    @staticmethod
    def send_udp_message(entry, listbox):
        """
        Send a UDP message to the server.

        :param entry: The entry widget containing the message to send.
        :param listbox: The listbox widget to display received messages.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            message = entry.get()
            dst = ("localhost", 7073)
            start_time = time.time()
            sock.sendto(message.encode(EncodingSettings.udp_encoding), dst)
            data, _ = sock.recvfrom(1024)
            end_time = time.time()
            rtt = end_time - start_time
            received_message = f"UDP Received: {data.decode(EncodingSettings.udp_encoding)} (RTT: {rtt:.4f} seconds)"
            listbox.insert(tk.END, received_message)
            listbox.yview(tk.END)
        entry.delete(0, tk.END)


class TCPHandler:
    """Class to manage the TCP socket and send TCP packets"""
    tcp_socket = None

    @staticmethod
    def open_tcp_socket(listbox):
        """
        Open a TCP socket.

        :param listbox: The listbox widget to display messages.
        """
        try:
            TCPHandler.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCPHandler.tcp_socket.connect(("localhost", 8090))
            listbox.insert(tk.END, "--- TCP Socket Opened and Connected to Server ---")
        except Exception as e:
            listbox.insert(tk.END, f"Failed to connect: {e}")
        listbox.yview(tk.END)

    @staticmethod
    def send_tcp_message(entry, listbox):
        """
        Send a TCP message to the server.

        :param entry: The entry widget containing the message to send.
        :param listbox: The listbox widget to display received messages.
        """
        if TCPHandler.tcp_socket:
            message = entry.get()
            start_time = time.time()
            TCPHandler.tcp_socket.sendall(message.encode(EncodingSettings.tcp_encoding))
            data = TCPHandler.tcp_socket.recv(1024)
            # print(data.decode(EncodingSettings.tcp_encoding))
            end_time = time.time()
            rtt = end_time - start_time
            received_message = f"TCP Received: {data.decode(EncodingSettings.tcp_encoding)} (RTT: {rtt:.4f} seconds)"
            listbox.insert(tk.END, received_message)
            listbox.yview(tk.END)
        else:
            listbox.insert(tk.END, "TCP connection has not been opened!")
        entry.delete(0, tk.END)

    @staticmethod
    def close_tcp_socket(listbox):
        """
        Close the TCP socket.

        :param listbox: The listbox widget to display messages.
        """
        if TCPHandler.tcp_socket:
            TCPHandler.tcp_socket.close()
            TCPHandler.tcp_socket = None
            listbox.insert(tk.END, "--- TCP Socket Closed ---")
            listbox.yview(tk.END)


class DNSResolver:
    """Class to handle DNS resolution and tracing."""

    @staticmethod
    def resolve_domain_name(domain_name, retries=3, timeout=5):
        """
        Resolve a domain name to an IP address with tracing.

        :param domain_name: The domain name to resolve.
        :param retries: Number of retries for DNS resolution.
        :param timeout: Timeout for each DNS query.
        :return: A tuple containing the official name, aliases, IP addresses, and trace information.
        """
        trace = []
        for attempt in range(retries):
            try:
                resolver = dns.resolver.Resolver()
                resolver.timeout = timeout
                resolver.lifetime = timeout

                trace.append(f"Attempt {attempt + 1}: Using resolver nameservers: {resolver.nameservers}")
                response = resolver.resolve(domain_name, 'A')
                ip_addresses = [answer.address for answer in response]
                trace.append(f"Success: Resolved {domain_name} to {ip_addresses}")
                return domain_name, [], ip_addresses, trace

            except dns.exception.Timeout as e:
                trace.append(f"Attempt {attempt + 1}: Timeout occurred: {e}")
            except dns.resolver.NXDOMAIN as e:
                trace.append(f"Attempt {attempt + 1}: No such domain: {e}")
                break
            except dns.resolver.YXDOMAIN as e:
                trace.append(f"Attempt {attempt + 1}: YXDOMAIN error: {e}")
                break
            except dns.resolver.NoNameservers as e:
                trace.append(f"Attempt {attempt + 1}: No nameservers available: {e}")
                break
            except dns.resolver.NoAnswer as e:
                trace.append(f"Attempt {attempt + 1}: No answer received: {e}")
            except Exception as e:
                trace.append(f"Attempt {attempt + 1}: Other error: {e}")
            time.sleep(1)  # Wait before retrying

        return f"DNS lookup failed after {retries} attempts", trace

    @staticmethod
    def dns_request(entry, listbox):
        """
        Perform a DNS lookup for the domain name passed to the entry widget.

        :param entry: The entry widget containing the domain name.
        :param listbox: The listbox widget to display the DNS resolution result.
        """
        domain_name = entry.get()
        result = DNSResolver.resolve_domain_name(domain_name)
        listbox.delete(0, tk.END)
        if isinstance(result, tuple):
            try:
                official_name, aliases, ip_addresses, trace = result
            except ValueError as e:
                listbox.insert(tk.END, e)
                listbox.insert(tk.END, "Maybe check your internet connection!")
                return

            listbox.insert(tk.END, f"Domain: {domain_name}")
            listbox.insert(tk.END, f"Official Name: {official_name}")
            listbox.insert(tk.END, f"Aliases: {aliases}")
            listbox.insert(tk.END, f"IP Addresses: {ip_addresses}")
        else:
            listbox.insert(tk.END, result[0])
        listbox.insert(tk.END, "Trace:")
        for step in trace:
            listbox.insert(tk.END, "   " + step)


class RTTMeasurement:
    """Class to handle RTT (Round Trip Time) measurements."""

    @staticmethod
    def measure_rtt(entry, result_var):
        """
        Measure the RTT to a given host.

        :param entry: The entry widget containing the host name.
        :param result_var: The StringVar to display the RTT result.
        """
        host = entry.get()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((host, 80))
            except socket.gaierror as e:
                result_var.set("Maybe check your internet connection!")
                return
            start_time = time.time()
            sock.sendall(b'HEAD / HTTP/1.1\r\nHost: google.com\r\n\r\n')
            sock.recv(1024)
            end_time = time.time()
            result_var.set(f"RTT: {end_time - start_time} seconds")


class HTTPClient:
    """Class to handle HTTP client operations."""

    @staticmethod
    def send_http_request(entry, listbox, label):
        """
        Send an HTTP GET request to the server.

        :param entry: The entry widget containing the filename.
        :param listbox: The listbox widget to display messages.
        :param label: The label widget to display images.
        """
        filename = entry.get()
        request_line = f"GET http_files/{filename} HTTP/1.1\r\nHost: localhost\r\n\r\n"
        file_data = b""

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(("localhost", 8080))
                sock.sendall(request_line.encode("utf-8"))
                while True:
                    data = sock.recv(4096)
                    if not data:
                        break
                    file_data += data

            if b"HTTP/1.1 200 OK" in file_data:
                header_end = file_data.find(b"\r\n\r\n") + 4
                file_content = file_data[header_end:]
                file_path = os.path.join("http_files", filename)

                with open(file_path, "wb") as f:
                    f.write(file_content)

                if filename.endswith(".jpg"):
                    HTTPClient.display_image(file_path, label)
                else:
                    listbox.insert(tk.END, f"File received: {file_path}")
            else:
                listbox.insert(tk.END, "HTTP request failed")
        except Exception as e:
            listbox.insert(tk.END, f"HTTP request failed: {e}")
        listbox.yview(tk.END)
        entry.delete(0, tk.END)

    @staticmethod
    def display_image(file_path, label):
        """
        Display an image file in the provided label widget.

        :param file_path: The path to the image file.
        :param label: The label widget to display the image.
        """
        try:
            image = Image.open(file_path)
            image = image.resize((300, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(image)
            label.config(image=img)
            label.image = img
        except Exception as e:
            messages_listbox.insert(tk.END, f"Failed to display image: {e}")
            messages_listbox.yview(tk.END)


class DataTransmission:
    """Class to handle data transmission to and from a server."""
    push_active = False
    push_socket = None
    pull_active = False
    pull_socket = None

    @staticmethod
    def start_push_stream():
        """Start pushing data to the server continuously in a separate thread."""
        try:
            DataTransmission.push_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            DataTransmission.push_socket.connect(('localhost', 8001))
            proj_messages_listbox.insert(tk.END, "--- Push Stream Started and Connected to Server ---")
            DataTransmission.push_active = True
            threading.Thread(target=DataTransmission.push_data_stream, args=(proj_messages_listbox,)).start()
        except Exception as e:
            proj_messages_listbox.insert(tk.END, f"Failed to start push stream: {e}")
        proj_messages_listbox.yview(tk.END)

    @staticmethod
    def stop_push_stream():
        """Stop pushing data to the server."""
        DataTransmission.push_active = False
        if DataTransmission.push_socket:
            DataTransmission.push_socket.close()
            DataTransmission.push_socket = None
            proj_messages_listbox.insert(tk.END, "--- Push Stream Stopped and Connection Closed ---")
        proj_messages_listbox.yview(tk.END)

    @staticmethod
    def push_data_stream(listbox):
        """Push data to the server at regular intervals while push_active is True."""
        while DataTransmission.push_active:
            try:
                data_types = ["Temperature", "Humidity", "Pressure"]
                values = [np.round(random.uniform(0, 100), 2) for _ in data_types]
                message = ",".join([f"{data_type}: {value}" for data_type, value in zip(data_types, values)])
                DataTransmission.push_socket.sendall(message.encode('utf-8'))
                listbox.insert(tk.END, f"Pushed data: {', '.join(message.split(','))}")
            except Exception as e:
                listbox.insert(tk.END, f"Push error: {e}")
            listbox.yview(tk.END)
            time.sleep(1)  # Adjust the interval as needed

    @staticmethod
    def push_data_once(listbox):
        """
        Push random data to the server.

        :param listbox: The listbox widget to display messages.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', 8001))
                data_types = ["Temperature", "Humidity", "Pressure"]
                values = [np.round(random.uniform(0, 100), 2) for _ in data_types]
                message = ",".join([f"{data_type}: {value}" for data_type, value in zip(data_types, values)])
                sock.sendall(message.encode('utf-8'))
                listbox.insert(tk.END, f"Pushed data: {', '.join(message.split(','))}")
        except Exception as e:
            listbox.insert(tk.END, f"Push error: {e}")
        listbox.yview(tk.END)

    @staticmethod
    def start_pull_data():
        """Start pulling data from the server in a separate thread."""
        try:
            DataTransmission.pull_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            DataTransmission.pull_socket.connect(('localhost', 8002))
            proj_messages_listbox.insert(tk.END, "--- Pull Stream Started and Connected to Server ---")
            DataTransmission.pull_active = True
            threading.Thread(target=DataTransmission.pull_data_from_server, args=(proj_messages_listbox,)).start()
        except Exception as e:
            proj_messages_listbox.insert(tk.END, f"Failed to start pull stream: {e}")
        proj_messages_listbox.yview(tk.END)

    @staticmethod
    def stop_pull_data():
        """Stop pulling data from the server."""
        DataTransmission.pull_active = False
        if DataTransmission.pull_socket:
            DataTransmission.pull_socket.close()
            DataTransmission.pull_socket = None
            proj_messages_listbox.insert(tk.END, "--- Pull Stream Stopped and Connection Closed ---")
        proj_messages_listbox.yview(tk.END)

    @staticmethod
    def pull_data_from_server(listbox):
        """Pull data from the server at regular intervals while pull_active is True."""
        while DataTransmission.pull_active:
            try:
                message = "GET DATA"
                DataTransmission.pull_socket.sendall(message.encode('utf-8'))
                data = DataTransmission.pull_socket.recv(1024)
                DataTransmission.process_received_data(data.decode('utf-8'))
            except Exception as e:
                listbox.insert(tk.END, f"Pull error: {e}")
            listbox.yview(tk.END)
            time.sleep(1)  # Adjust the sleep time as needed

    @staticmethod
    def process_received_data(data):
        """
        Process data received from the server and update plots.

        :param data: The received data as a string.
        """
        try:
            data_pairs = data.split(',')
            for data_pair in data_pairs:
                data_type, value = data_pair.split(":")
                value = float(value)
                if data_type == "Temperature":
                    temp_values.append(value)
                elif data_type == "Humidity":
                    humidity_values.append(value)
                elif data_type == "Pressure":
                    pressure_values.append(value)
            DataTransmission.update_combined_plot()
            DataTransmission.update_heatmap()
            DataTransmission.update_barplot()
            DataTransmission.update_scatter_plot()
            data_print = ": ".join(", ".join(data.split(',')).split(":"))
            proj_messages_listbox.insert(tk.END, f"Pulled data: {data_print}")
        except Exception as e:
            proj_messages_listbox.insert(tk.END, f"Failed to process data: {e}")
        proj_messages_listbox.yview(tk.END)

    @staticmethod
    def update_combined_plot():
        """Update the combined plot with temperature, humidity, and pressure data."""
        if combined_plot is None:
            return
        combined_plot.clear()
        combined_plot.plot(temp_values, label="Temperature", color="red")
        combined_plot.plot(humidity_values, label="Humidity", color="blue")
        combined_plot.plot(pressure_values, label="Pressure", color="green")
        combined_plot.legend(loc='center left', bbox_to_anchor=(0.25, 1.17))
        combined_plot.figure.canvas.draw()

    @staticmethod
    def update_heatmap():
        """Update the heatmap with random data."""
        if heatmap_plot is None:
            return
        heatmap_plot.clear()
        heatmap_data = np.random.rand(10, 10)  # Generate random heatmap data
        sns.heatmap(heatmap_data, ax=heatmap_plot, cbar=False, cmap="YlGnBu")
        heatmap_plot.figure.canvas.draw()

    @staticmethod
    def update_barplot():
        """Update the bar plot with the latest temperature, humidity, and pressure data."""
        if bar_plot is None:
            return
        bar_plot.clear()
        categories = ['Temperature', 'Humidity', 'Pressure']
        values = [temp_values[-1] if temp_values else 0,
                  humidity_values[-1] if humidity_values else 0,
                  pressure_values[-1] if pressure_values else 0]
        bar_plot.bar(categories, values)
        bar_plot.figure.canvas.draw()

    @staticmethod
    def update_scatter_plot():
        """Update the scatter plot with temperature, humidity, and pressure data over time."""
        if scatter_plot is None:
            return
        scatter_plot.clear()
        scatter_plot.scatter(range(len(temp_values)), temp_values, label='Temperature', color='red')
        scatter_plot.scatter(range(len(humidity_values)), humidity_values, label='Humidity', color='blue')
        scatter_plot.scatter(range(len(pressure_values)), pressure_values, label='Pressure', color='green')
        scatter_plot.legend(loc='center left', bbox_to_anchor=(0.25, 1.17))
        scatter_plot.figure.canvas.draw()


class MainApp:
    """Main application class to set up and run the Tkinter UI."""

    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Internet Communication Project Course")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        self.style = {
            "font": ("Arial", 12),
            "padx": 5,
            "pady": 5
        }

        self.label_style = {
            "font": ("Arial", 12, "bold")
        }

        self.text_style = {
            "font": ("Arial", 11)
        }

        self.frame_style = {
            "bg": "#e0e0e0",
            "bd": 2,
            "relief": "sunken",
            "padx": 10,
            "pady": 10
        }

        self.tcp_entry_var = tk.StringVar()
        self.tcp_entry_var.trace_add("write", lambda *args: self.update_button_state())
        self.tcp_button = ttk.Button()

        self.udp_entry_var = tk.StringVar()
        self.udp_entry_var.trace_add("write", lambda *args: self.update_button_state())
        self.udp_button = ttk.Button()

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface by creating tabs and their respective frames and widgets."""
        # Create Notebook for Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=1, fill="both")

        # TCP and UDP Tab
        tcp_udp_tab = self.create_tcp_udp_tab(notebook)
        notebook.add(tcp_udp_tab, text="TCP/UDP")

        # DNS and RTT Tab
        dns_rtt_tab = self.create_dns_rtt_tab(notebook)
        notebook.add(dns_rtt_tab, text="DNS/RTT/HTTP")

        # New comprehensive window
        project_tab = self.create_project_tab(notebook)
        notebook.add(project_tab, text="Project")

        notebook.pack(expand=1, fill="both")

    def create_tcp_udp_tab(self, notebook):
        """
        Create the TCP/UDP tab with related frames and widgets.

        :param notebook: The parent notebook widget.
        :return: The created TCP/UDP tab frame.
        """
        tcp_udp_tab = ttk.Frame(notebook)

        # TCP Section
        tcp_frame = ttk.LabelFrame(tcp_udp_tab, text="TCP Client", padding="10")
        tcp_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        tcp_udp_tab.grid_columnconfigure(0, weight=1)
        tcp_udp_tab.grid_rowconfigure(0, weight=1)

        tcp_label = ttk.Label(tcp_frame, text="Message:", **self.label_style)
        tcp_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        tcp_entry = ttk.Entry(tcp_frame, width=50, textvariable=self.tcp_entry_var)
        tcp_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        tcp_entry.bind("<Return>", lambda event: TCPHandler.send_tcp_message(tcp_entry, messages_listbox))

        self.tcp_button = ttk.Button(tcp_frame, text="Send",
                                     command=lambda: TCPHandler.send_tcp_message(tcp_entry, messages_listbox),
                                     state=tk.DISABLED)
        self.tcp_button.grid(row=1, column=2, padx=5, pady=5)

        tcp_encoding_label = ttk.Label(tcp_frame, text="Encoding:", **self.label_style)
        tcp_encoding_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tcp_encoding_var = tk.StringVar(value="utf-8")
        tcp_encoding_menu = ttk.OptionMenu(tcp_frame, tcp_encoding_var, "utf-8", "ascii", "utf-8",
                                           command=EncodingSettings.update_tcp_encoding)
        tcp_encoding_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tcp_open_button = ttk.Button(tcp_frame, text="Open TCP Socket",
                                     command=lambda: TCPHandler.open_tcp_socket(messages_listbox))
        tcp_open_button.grid(row=3, column=1, padx=40, pady=15, sticky="w")
        tcp_close_button = ttk.Button(tcp_frame, text="Close TCP Socket",
                                      command=lambda: TCPHandler.close_tcp_socket(messages_listbox))
        tcp_close_button.grid(row=3, column=1, padx=40, pady=15, sticky="e")

        tcp_info_label = ttk.Label(tcp_frame,
                                   text="• Connection-oriented protocol\n• Ensures reliable data transfer\n"
                                        "• Error checking and flow control", wraplength=500, **self.text_style)
        tcp_info_label.grid(row=5, column=0, columnspan=3, padx=5, pady=50, sticky="ew")

        # UDP Section
        udp_frame = ttk.LabelFrame(tcp_udp_tab, text="UDP Client", padding="10")
        udp_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        tcp_udp_tab.grid_rowconfigure(1, weight=1)

        udp_label = ttk.Label(udp_frame, text="Message:", **self.label_style)
        udp_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        udp_entry = ttk.Entry(udp_frame, width=50, textvariable=self.udp_entry_var)
        udp_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        udp_entry.bind("<Return>", lambda event: UDPClient.send_udp_message(udp_entry, messages_listbox))

        self.udp_button = ttk.Button(udp_frame, text="Send",
                                     command=lambda: UDPClient.send_udp_message(udp_entry, messages_listbox),
                                     state=tk.DISABLED)
        self.udp_button.grid(row=1, column=2, padx=5, pady=5)

        udp_encoding_label = ttk.Label(udp_frame, text="Encoding:", **self.label_style)
        udp_encoding_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        udp_encoding_var = tk.StringVar(value="utf-8")
        udp_encoding_menu = ttk.OptionMenu(udp_frame, udp_encoding_var, "utf-8", "ascii", "utf-8",
                                           command=EncodingSettings.update_udp_encoding)
        udp_encoding_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        udp_info_label = ttk.Label(udp_frame,
                                   text="• Connectionless protocol\n• Faster but not reliable\n• No guarantee of data "
                                        "transfer", wraplength=500, **self.text_style)
        udp_info_label.grid(row=3, column=0, columnspan=3, padx=5, pady=50, sticky="ew")

        # Received Messages Section
        messages_frame = ttk.LabelFrame(tcp_udp_tab, text="Received Messages", padding="10")
        messages_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        messages_frame.grid_rowconfigure(0, weight=1)
        messages_frame.grid_columnconfigure(0, weight=1)

        tcp_udp_tab.grid_columnconfigure(1, weight=1)

        messages_scrollbar = ttk.Scrollbar(messages_frame, orient=tk.VERTICAL)
        global messages_listbox
        messages_listbox = tk.Listbox(messages_frame, font=self.style["font"], yscrollcommand=messages_scrollbar.set)
        messages_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        messages_scrollbar.config(command=messages_listbox.yview)
        messages_scrollbar.grid(row=0, column=1, sticky='ns')

        # Make all frames resizable
        for i in range(2):
            tcp_udp_tab.grid_rowconfigure(i, weight=1)
        tcp_udp_tab.grid_columnconfigure(1, weight=1)

        return tcp_udp_tab

    def update_button_state(self):
        """
        Update the state of the send buttons based on the content of the entry widgets.
        """
        if self.tcp_entry_var.get().strip():
            self.tcp_button.config(state=tk.NORMAL)
        else:
            self.tcp_button.config(state=tk.DISABLED)

        if self.udp_entry_var.get().strip():
            self.udp_button.config(state=tk.NORMAL)
        else:
            self.udp_button.config(state=tk.DISABLED)

    def create_dns_rtt_tab(self, notebook):
        """
        Create the DNS/RTT/HTTP tab with related frames and widgets.

        :param notebook: The parent notebook widget.
        :return: The created DNS/RTT/HTTP tab frame.
        """
        dns_rtt_tab = ttk.Frame(notebook)

        # DNS Section
        dns_frame = ttk.LabelFrame(dns_rtt_tab, text="DNS Lookup", padding="10")
        dns_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        dns_rtt_tab.grid_columnconfigure(0, weight=1)
        dns_rtt_tab.grid_rowconfigure(0, weight=1)

        dns_label = ttk.Label(dns_frame, text="Domain:", **self.label_style)
        dns_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        dns_entry = ttk.Entry(dns_frame, width=50)
        dns_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        dns_entry.bind("<Return>", lambda event: DNSResolver.dns_request(dns_entry, dns_resolution_listbox))
        dns_button = ttk.Button(dns_frame, text="Lookup",
                                command=lambda: DNSResolver.dns_request(dns_entry, dns_resolution_listbox))
        dns_button.grid(row=1, column=2, padx=5, pady=5)

        dns_info_label = ttk.Label(dns_frame,
                                   text="• Domain Name System (DNS) resolves human-readable domain names to IP "
                                        "addresses.\n• It translates website names (e.g., www.google.com) into "
                                        "numerical IP addresses that computers use to identify each other on the "
                                        "network.\n\n→ Put in an address (e.g. google.com, only .com addresses work)",
                                   wraplength=500, **self.text_style)
        dns_info_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        dns_resolution_scrollbar = ttk.Scrollbar(dns_frame, orient=tk.VERTICAL)
        global dns_resolution_listbox
        dns_resolution_listbox = tk.Listbox(dns_frame, font=self.style["font"],
                                            yscrollcommand=dns_resolution_scrollbar.set)
        dns_resolution_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        dns_resolution_scrollbar.config(command=dns_resolution_listbox.yview)
        dns_resolution_scrollbar.grid(row=2, column=3, sticky='ns')

        # RTT Section
        rtt_frame = ttk.LabelFrame(dns_rtt_tab, text="RTT Measurement", padding="10")
        rtt_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        dns_rtt_tab.grid_columnconfigure(1, weight=1)

        rtt_label = ttk.Label(rtt_frame, text="Host:", **self.label_style)
        rtt_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        rtt_entry = ttk.Entry(rtt_frame, width=50)
        rtt_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        rtt_entry.bind("<Return>", lambda event: RTTMeasurement.measure_rtt(rtt_entry, rtt_result))
        rtt_button = ttk.Button(rtt_frame, text="Measure",
                                command=lambda: RTTMeasurement.measure_rtt(rtt_entry, rtt_result))
        rtt_button.grid(row=1, column=2, padx=5, pady=5)

        rtt_info_label = ttk.Label(rtt_frame,
                                   text="• Round Trip Time (RTT) measures the time it takes for a signal to travel "
                                        "from the sender to the receiver and back.\n• It is an important metric for "
                                        "evaluating the latency and performance of a network connection.\n\n → Put in "
                                        "an address (e.g. google.com)", wraplength=500, **self.text_style)
        rtt_info_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        global rtt_result
        rtt_result = tk.StringVar()
        rtt_result_label = ttk.Label(rtt_frame, textvariable=rtt_result, **self.text_style)
        rtt_result_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # HTTP Section
        http_frame = ttk.LabelFrame(dns_rtt_tab, text="HTTP Client", padding="10")
        http_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        dns_rtt_tab.grid_rowconfigure(1, weight=1)

        http_command_label = ttk.Label(http_frame, text="GET /http_files/ ", **self.label_style)
        http_command_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        http_entry = ttk.Entry(http_frame, width=4, state="DISABLED")
        http_entry.insert(0, "lkn-bild.jpg")
        http_entry.config(state="disabled")
        http_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        http_entry.bind("<Return>", lambda event: HTTPClient.send_http_request(http_entry,
                                                                               messages_listbox, image_label))
        http_command_suffix_label = ttk.Label(http_frame, text=" HTTP/1.1", **self.label_style)
        http_command_suffix_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        http_button = ttk.Button(http_frame, text="Send",
                                 command=lambda: HTTPClient.send_http_request(http_entry,
                                                                              messages_listbox, image_label))
        http_button.grid(row=0, column=3, padx=5, pady=5)

        http_info_label = ttk.Label(http_frame, text="• HTTP is used for transmitting files over the web.\n• Use the"
                                                     " command format to request files from the server.",
                                    wraplength=500, **self.text_style)
        http_info_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        global image_label
        image_label = ttk.Label(http_frame)
        image_label.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Update grid configuration to ensure proper layout and resizing
        http_frame.grid_rowconfigure(2, weight=1)
        http_frame.grid_columnconfigure(1, weight=1)

        return dns_rtt_tab

    def create_project_tab(self, notebook):
        """
        Create the Project tab with related frames and widgets.

        :param notebook: The parent notebook widget.
        :return: The created Project tab frame.
        """
        project_tab = ttk.Frame(notebook)

        # Control Frame for Start/Stop
        control_frame = ttk.LabelFrame(project_tab, text="Control", padding="10")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        project_tab.grid_columnconfigure(0, weight=1)
        project_tab.grid_rowconfigure(0, weight=1)

        start_push_button = ttk.Button(control_frame, text="Start Push Stream",
                                       command=DataTransmission.start_push_stream)
        start_push_button.grid(row=0, column=0, padx=5, pady=5)

        stop_push_button = ttk.Button(control_frame, text="Stop Push Stream",
                                      command=DataTransmission.stop_push_stream)
        stop_push_button.grid(row=0, column=1, padx=5, pady=5)

        push_button = ttk.Button(control_frame, text="Push Data Once",
                                 command=lambda: DataTransmission.push_data_once(proj_messages_listbox))
        push_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        start_pull_button = ttk.Button(control_frame, text="Start Pull Transmission",
                                       command=DataTransmission.start_pull_data)
        start_pull_button.grid(row=2, column=0, padx=5, pady=25)

        stop_pull_button = ttk.Button(control_frame, text="Stop Pull Transmission",
                                      command=DataTransmission.stop_pull_data)
        stop_pull_button.grid(row=2, column=1, padx=5, pady=25)

        control_frame.grid_rowconfigure(0, weight=1)
        control_frame.grid_rowconfigure(1, weight=1)
        control_frame.grid_rowconfigure(2, weight=1)
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)

        # Plotting Frame
        plot_frame = ttk.LabelFrame(project_tab, text="Data Plots", padding="10")
        plot_frame.grid(row=0, column=1, columnspan=2, rowspan=2, padx=10, pady=10, sticky="nsew")

        fig = Figure(figsize=(8, 6), dpi=100)
        global combined_plot, scatter_plot, bar_plot, heatmap_plot
        combined_plot = fig.add_subplot(221)
        scatter_plot = fig.add_subplot(222)
        bar_plot = fig.add_subplot(223)
        heatmap_plot = fig.add_subplot(224)

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)

        # Messages Section
        proj_messages_frame = ttk.LabelFrame(project_tab, text="Sent Data", padding="10")
        proj_messages_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        proj_messages_scrollbar = ttk.Scrollbar(proj_messages_frame, orient=tk.VERTICAL)
        global proj_messages_listbox
        proj_messages_listbox = tk.Listbox(proj_messages_frame, font=self.style["font"],
                                           yscrollcommand=proj_messages_scrollbar.set)
        proj_messages_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        proj_messages_scrollbar.config(command=proj_messages_listbox.yview)
        proj_messages_scrollbar.grid(row=0, column=1, sticky='ns')

        proj_messages_frame.grid_rowconfigure(0, weight=1)
        proj_messages_frame.grid_columnconfigure(0, weight=1)

        # Make all frames resizable
        project_tab.grid_rowconfigure(0, weight=1)
        project_tab.grid_rowconfigure(1, weight=1)
        project_tab.grid_columnconfigure(0, weight=1)
        project_tab.grid_columnconfigure(1, weight=3)

        return project_tab


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
