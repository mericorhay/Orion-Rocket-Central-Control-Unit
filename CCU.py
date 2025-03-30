import tkinter as tk
from tkinter import ttk
import serial
from math import radians, cos, sin

class RocketUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚀 Orion Roketi Yer Kontrol İstasyonu 🚀")
        self.geometry("900x600")
        self.configure(bg='#1D1F20')

        # Stil ayarları
        style = ttk.Style()
        style.configure('TFrame', background='#1D1F20')
        style.configure('TLabelframe', background='#1D1F20')
        style.configure('TLabel', background='#1D1F20', foreground="white")
        style.configure('TButton', background='#1D1F20', foreground="black", font=("Arial", 12))
        style.map('TButton', background=[('active', '#5A6166')])

        # Ana çerçeve
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Bağlantı durumu
        self.connection_status_label = ttk.Label(main_frame, text="Bağlantı: Bağlanmadı", font=("Arial", 14),
                                                 foreground="red")
        self.connection_status_label.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

        # Veri ekranı
        data_frame = ttk.LabelFrame(main_frame, text="Orion Roketi Verileri", padding=15)
        data_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        labels = ["X", "Y", "Z", "Hız", "Yükseklik", "Paraşüt 1", "Paraşüt 2"]
        self.labels = {label: ttk.Label(data_frame, text="0", font=("Arial", 12), foreground="white") for label in labels}
        for idx, label in enumerate(labels):
            ttk.Label(data_frame, text=f"{label}:", font=("Arial", 12, "bold")).grid(row=idx, column=0, sticky=tk.W, pady=5)
            self.labels[label].grid(row=idx, column=1, sticky=tk.W, pady=5)

        # Roket yön animasyonu
        animation_frame = ttk.LabelFrame(main_frame, text="Orion Roketi Yönü", padding=10)
        animation_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.canvas = tk.Canvas(animation_frame, width=300, height=300, highlightthickness=0)
        self.canvas.pack()

        self.rocket_center = (150, 150)
        self.rocket_length = 100
        self.angle = 0
        self.rocket = None
        self.update_tilt(self.angle)

        # Seri port
        self.serial_port = None

        # Düzen ayarları
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=3)

        # Paraşüt açma butonları
        parachute_frame = ttk.LabelFrame(main_frame, text="Paraşüt Açma", padding=10)
        parachute_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.parachute1_button = ttk.Button(parachute_frame, text="1. Paraşüt Aç", command=self.open_parachute1)
        self.parachute1_button.grid(row=0, column=0, padx=10, pady=10)

        self.parachute2_button = ttk.Button(parachute_frame, text="2. Paraşüt Aç", command=self.open_parachute2)
        self.parachute2_button.grid(row=0, column=1, padx=10, pady=10)

    def connect_serial(self):
        try:
            # LoRa modülünün bağlı olduğu portu ve baud rate'i ayarla
            self.serial_port = serial.Serial('COM3', 9600, timeout=1)  # COM3'ü kendi portunla değiştir
            self.update_connection_status(True)
            self.check_connection()
            print("LoRa bağlantısı kuruldu.")
        except serial.SerialException as e:
            print(f"Bağlantı hatası: {e}")
            self.update_connection_status(False)

    def update_connection_status(self, is_connected):
        status = "Bağlantı: Bağlı" if is_connected else "Bağlantı: Bağlanmadı"
        color = "green" if is_connected else "red"
        self.connection_status_label.config(text=status, foreground=color)

    def check_connection(self):
        if self.serial_port and self.serial_port.is_open:
            self.update_connection_status(True)
            self.read_data_from_serial()
        else:
            self.update_connection_status(False)
        self.after(2000, self.check_connection)  # 2 saniyede bir kontrol

    def read_data_from_serial(self):
        if self.serial_port and self.serial_port.in_waiting > 0:
            try:
                data = self.serial_port.readline().decode('utf-8').strip()
                print(f"LoRa'dan alınan veri: {data}")
                
                # Gelen veriyi virgülle ayır ve çözümle
                x, y, z, speed, height, parachute1, parachute2 = map(float, data.split(","))
                self.update_labels(x, y, z, speed, height, int(parachute1), int(parachute2))
                
                # X ve Y eksenine göre roketin yönünü güncelle (örnek olarak)
                self.angle = x  # X açısını roketin eğimi olarak kullanabilirsin
                self.update_tilt(self.angle)
            except (ValueError, UnicodeDecodeError) as e:
                print(f"Veri okuma hatası: {e} - Ham veri: {data}")

    def update_labels(self, x, y, z, speed, height, parachute1, parachute2):
        # Verileri arayüzde güncelle
        self.labels["X"].config(text=f"{x:.2f}")
        self.labels["Y"].config(text=f"{y:.2f}")
        self.labels["Z"].config(text=f"{z:.2f}")
        self.labels["Hız"].config(text=f"{speed:.2f}")
        self.labels["Yükseklik"].config(text=f"{height:.2f}")
        self.labels["Paraşüt 1"].config(text=f"{parachute1}")
        self.labels["Paraşüt 2"].config(text=f"{parachute2}")

    def update_tilt(self, angle):
        self.canvas.delete("all")
        angle_rad = radians(angle)
        x, y = self.rocket_center
        length = self.rocket_length
        nose, left, right = (x, y - length / 2), (x - 20, y + length / 2), (x + 20, y + length / 2)

        def rotate_point(px, py):
            return (x + (px - x) * cos(angle_rad) - (py - y) * sin(angle_rad),
                    y + (px - x) * sin(angle_rad) + (py - y) * cos(angle_rad))

        rotated_nose, rotated_left, rotated_right = [
            rotate_point(px, py) for px, py in [nose, left, right]
        ]

        self.rocket = self.canvas.create_polygon(rotated_nose, rotated_left, rotated_right, fill="#FF4500", outline="black")

    def open_parachute1(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write(b'P1\n')  # LoRa'ya "1. Paraşüt Aç" komutu
            print("1. Paraşüt açma komutu gönderildi.")
        else:
            print("LoRa bağlantısı yok.")

    def open_parachute2(self):
        if self.serial_port and self.serial_port.is_open:
 b           self.serial_port.write(b'P2\n')  # LoRa'ya "2. Paraşüt Aç" komutu
            print("2. Paraşüt açma komutu gönderildi.")
        else:
            print("LoRa bağlantısı yok.")

if __name__ == "__main__":
    app = RocketUI()
    app.connect_serial()
    app.mainloop()