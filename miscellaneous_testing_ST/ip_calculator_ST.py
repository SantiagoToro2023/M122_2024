import customtkinter as ctk
import ipaddress
import math

# Set appearance and color theme 🐧🔷
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


# Create App class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("IP-Berechner 1.0")

        # Enable fullscreen mode
        self.state("zoomed")

        # Title label
        self.titleLabel = ctk.CTkLabel(self, text="IP-Berechner", font=("default", 24))
        self.titleLabel.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Configure grid columns to make sure the entries expand
        self.grid_columnconfigure(0, weight=1, uniform="equal")  # Column 0 for labels
        self.grid_columnconfigure(1, weight=2, uniform="equal")  # Column 1 for entries

        # IP Address Entry
        self.ipEntryLabel = ctk.CTkLabel(self, text="IP:", font=("default", 20))
        self.ipEntryLabel.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ipEntry = ctk.CTkEntry(self, font=("default", 20), width=200)
        self.ipEntry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Subnet Mask Entry
        self.subnetEntryLabel = ctk.CTkLabel(self, text="Subnet:", font=("default", 20))
        self.subnetEntryLabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.subnetEntry = ctk.CTkEntry(self, font=("default", 20), width=200)
        self.subnetEntry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Number of Subnets Dropdown
        self.subnetCountLabel = ctk.CTkLabel(self, text="Subnets:", font=("default", 20))
        self.subnetCountLabel.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.subnetCountDropdown = ctk.CTkOptionMenu(self, values=[str(i) for i in range(1, 17)], font=("default", 20), width=75)
        self.subnetCountDropdown.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Calculate Button
        self.calculateButton = ctk.CTkButton(self, text="Calculate", font=("default", 20),
                                             command=self.calculate_ip_info)
        self.calculateButton.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Results Section
        self.networkLabel = ctk.CTkLabel(self, text="Network Address:", font=("default", 18))
        self.networkLabel.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.networkResult = ctk.CTkLabel(self, text="", font=("default", 18))
        self.networkResult.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.broadcastLabel = ctk.CTkLabel(self, text="Broadcast Address:", font=("default", 18))
        self.broadcastLabel.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.broadcastResult = ctk.CTkLabel(self, text="", font=("default", 18))
        self.broadcastResult.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.hostsLabel = ctk.CTkLabel(self, text="Number of Hosts:", font=("default", 18))
        self.hostsLabel.grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.hostsResult = ctk.CTkLabel(self, text="", font=("default", 18))
        self.hostsResult.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        # Subnet Info Section (Scrollable Frame)
        self.subnetInfoFrame = ctk.CTkScrollableFrame(self, height=300)  # Set the height to control the scrolling area
        self.subnetInfoFrame.grid(row=8, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        # Allow the frame to expand vertically
        self.grid_rowconfigure(8, weight=1)

    # Method to calculate IP information
    def calculate_ip_info(self):
        ip = self.ipEntry.get()
        subnet = self.subnetEntry.get()
        subnet_count = int(self.subnetCountDropdown.get())

        try:
            # Parse the IP network using the entered IP and subnet
            network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)

            # Display base network information
            self.networkResult.configure(text=str(network.network_address))
            self.broadcastResult.configure(text=str(network.broadcast_address))
            self.hostsResult.configure(text=str(network.num_addresses - 2))  # Subtracting network and broadcast

            # Calculate subnets
            new_prefix = network.prefixlen + math.ceil(math.log2(subnet_count))  # Calculate the new prefix length
            subnets = list(network.subnets(new_prefix=new_prefix))

            # Clear any previous results from the frame
            for widget in self.subnetInfoFrame.winfo_children():
                widget.destroy()

            # Display results for each subnet
            for i, subnet in enumerate(subnets):
                subnet_label = ctk.CTkLabel(self.subnetInfoFrame, text=f"Subnet {i + 1}:", font=("default", 18))
                subnet_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

                network_label = ctk.CTkLabel(self.subnetInfoFrame, text=f"Network: {subnet.network_address}", font=("default", 18))
                network_label.grid(row=i, column=1, padx=10, pady=5, sticky="w")

                broadcast_label = ctk.CTkLabel(self.subnetInfoFrame, text=f"Broadcast: {subnet.broadcast_address}", font=("default", 18))
                broadcast_label.grid(row=i, column=2, padx=10, pady=5, sticky="w")

                hosts_label = ctk.CTkLabel(self.subnetInfoFrame, text=f"Hosts: {subnet.num_addresses - 2}", font=("default", 18))
                hosts_label.grid(row=i, column=3, padx=10, pady=5, sticky="w")

        except ValueError as e:
            # Handle invalid IP or subnet input
            self.networkResult.configure(text="Invalid input")
            self.broadcastResult.configure(text="Invalid input")
            self.hostsResult.configure(text="Invalid input")


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
