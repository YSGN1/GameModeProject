import tkinter as tk
from tkinter import ttk, messagebox, font
import subprocess
import ctypes
import sys
import os
import threading
import winreg

# Yönetici hakları kontrolü
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

# Yönetici hakları ile çalıştırma
def run_as_admin():
    if not is_admin():
        # Programın tam yolunu al
        script = os.path.abspath(sys.argv[0])
        # Eğer .py dosyası ise
        if script.endswith('.py'):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
        else:
            # Eğer exe dosyası ise
            ctypes.windll.shell32.ShellExecuteW(None, "runas", script, None, None, 1)
        sys.exit(0)

# GUID'ler
BALANCED = "381b4222-f694-41f0-9685-ff5bb260df2e"
HIGH_PERFORMANCE = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
ULTIMATE = "e9a42b02-d5df-448d-aa00-03f14749eb61"

# Windows Explorer'ı yeniden başlat
def restart_explorer():
    try:
        subprocess.run('taskkill /F /FI "USERNAME eq %USERNAME%" /IM explorer.exe', shell=True)
        subprocess.run('start explorer.exe', shell=True)
        return True
    except Exception as e:
        print(f"Explorer yeniden başlatılamadı: {e}")
        return False

# Güç planını değiştirme
def change_power_plan(plan_guid, plan_name, restart_exp=False):
    try:
        # Güç planını değiştirme komutu
        command = f"powercfg /S {plan_guid}"
        subprocess.run(command, shell=True, check=True)
        
        # Windows gezginini yeniden başlatma
        if restart_exp:
            restart_explorer()
            
        status_label.config(text=f"{plan_name} planı aktifleştirildi!", fg="#00FF00")
        return True
    except Exception as e:
        messagebox.showerror("Hata", f"Güç planı değiştirilirken bir hata oluştu:\n{str(e)}")
        status_label.config(text="İşlem başarısız oldu!", fg="#FF0000")
        return False

# TCP Optimizasyonu
def optimize_tcp():
    try:
        # Internet bağlantıları için TCP optimizasyonu
        subprocess.run("netsh int tcp set global autotuninglevel=normal", shell=True)
        subprocess.run("netsh int tcp set global congestionprovider=ctcp", shell=True)
        subprocess.run("netsh int tcp set global ecncapability=enabled", shell=True)
        
        # Registry optimizasyonları
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "DefaultTTL", 0, winreg.REG_DWORD, 64)
            winreg.SetValueEx(key, "Tcp1323Opts", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "TcpMaxDataRetransmissions", 0, winreg.REG_DWORD, 3)
            
        return True
    except Exception as e:
        print(f"TCP optimizasyonu yapılamadı: {e}")
        return False

# DNS önbelleğini temizleme
def flush_dns():
    try:
        subprocess.run("ipconfig /flushdns", shell=True)
        return True
    except Exception as e:
        print(f"DNS önbelleği temizlenemedi: {e}")
        return False

# Performans optimizasyonu
def optimize_performance():
    try:
        # Bellek optimizasyonu
        subprocess.run("rundll32.exe advapi32.dll,ProcessIdleTasks", shell=True)
        subprocess.run("powershell Clear-RecycleBin -Force -ErrorAction SilentlyContinue", shell=True)
        
        # Disk Temizleme
        subprocess.run("cleanmgr /sagerun:1", shell=True, start_new_session=True)
        
        # Gereksiz hizmetleri devre dışı bırak
        services_to_disable = [
            "DiagTrack",  # Bağlı Kullanıcı Deneyimleri ve Telemetri
            "SysMain",    # Superfetch
            "WSearch"     # Windows Search
        ]
        
        for service in services_to_disable:
            subprocess.run(f"sc config {service} start= disabled", shell=True)
            subprocess.run(f"sc stop {service}", shell=True)
            
        return True
    except Exception as e:
        print(f"Performans optimizasyonu yapılamadı: {e}")
        return False

# Windows'un görsel efektlerini devre dışı bırakma
def disable_visual_effects():
    try:
        # Performans ayarlarını optimize et
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
            
        # Animasyonları kapat
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop\WindowMetrics", 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "MinAnimate", 0, winreg.REG_SZ, "0")
            
        return True
    except Exception as e:
        print(f"Görsel efektler devre dışı bırakılamadı: {e}")
        return False

# Oyun modu optimizasyonu
def optimize_for_gaming():
    try:
        status_label.config(text="Oyun optimizasyonu yapılıyor...", fg="#FFFF00")
        
        # Güç planını "Ultimate Performance" olarak ayarla
        change_power_plan(ULTIMATE, "Ultimate Performance", restart_exp=True)
        
        # Game Mode'u etkinleştir
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "AllowAutoGameMode", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "AutoGameModeEnabled", 0, winreg.REG_DWORD, 1)
            
        # Windows Update'i devre dışı bırak (geçici)
        subprocess.run("sc stop wuauserv", shell=True)
        subprocess.run("sc config wuauserv start= disabled", shell=True)
        
        # Ağ optimizasyonu
        optimize_tcp()
        flush_dns()
        
        # Gereksiz hizmetleri kapat
        optimize_performance()
        
        # Görsel efektleri kapat
        disable_visual_effects()
        
        status_label.config(text="Oyun optimizasyonu tamamlandı! ✓", fg="#00FF00")
        return True
    except Exception as e:
        status_label.config(text=f"Oyun optimizasyonu yapılamadı!", fg="#FF0000")
        print(f"Oyun optimizasyonu yapılamadı: {e}")
        return False

# Ağ optimizasyonu
def optimize_network():
    try:
        status_label.config(text="Ağ optimizasyonu yapılıyor...", fg="#FFFF00")
        
        # DNS önbelleğini temizle
        flush_dns()
        
        # TCP/IP optimizasyonu
        optimize_tcp()
        
        # Ağ önbelleğini temizle
        subprocess.run("netsh winsock reset", shell=True)
        subprocess.run("netsh int ip reset", shell=True)
        
        status_label.config(text="Ağ optimizasyonu tamamlandı! ✓", fg="#00FF00")
        return True
    except Exception as e:
        status_label.config(text=f"Ağ optimizasyonu yapılamadı!", fg="#FF0000")
        print(f"Ağ optimizasyonu yapılamadı: {e}")
        return False

# İşlemci zamanlayıcısı optimizasyonu
def optimize_cpu_timer():
    try:
        # İşlemci zamanlayıcı çözünürlüğünü değiştir
        subprocess.run("bcdedit /set useplatformclock false", shell=True)
        subprocess.run("bcdedit /set disabledynamictick yes", shell=True)
        
        return True
    except Exception as e:
        print(f"CPU timer optimizasyonu yapılamadı: {e}")
        return False

# Tüm optimizasyonları bir arada yap
def optimize_all():
    try:
        status_label.config(text="Tam optimizasyon başlatıldı...", fg="#FFFF00")
        
        # Güç planını "Ultimate Performance" olarak ayarla
        if change_power_plan(ULTIMATE, "Ultimate Performance", restart_exp=True):
            status_update("Güç planı ayarlandı ✓")
        
        # Ağ optimizasyonu
        if optimize_network():
            status_update("Ağ optimizasyonu tamamlandı ✓")
        
        # Performans optimizasyonu
        if optimize_performance():
            status_update("Performans optimizasyonu tamamlandı ✓")
        
        # İşlemci optimizasyonu
        if optimize_cpu_timer():
            status_update("İşlemci optimizasyonu tamamlandı ✓")
        
        # Görsel efektleri kapat
        if disable_visual_effects():
            status_update("Görsel efektler optimizasyonu tamamlandı ✓")
        
        status_label.config(text="Tüm optimizasyonlar tamamlandı! ✓", fg="#00FF00")
        return True
    except Exception as e:
        status_label.config(text=f"Optimizasyon tamamlanamadı!", fg="#FF0000")
        print(f"Tam optimizasyon yapılamadı: {e}")
        return False

# Durum güncellemesi
def status_update(message):
    status_label.config(text=message, fg="#FFFF00")
    root.update()

# Arkaplan işlem başlatma
def run_in_background(function):
    thread = threading.Thread(target=function)
    thread.daemon = True
    thread.start()

# Ana uygulama fonksiyonu
def main():
    global root, status_label
    
    # Yönetici kontrolü
    if not is_admin():
        run_as_admin()
        return

    # Ana pencere
    root = tk.Tk()
    root.title("GameBooster - Performans Optimizasyonu")
    root.geometry("700x600")
    root.configure(bg="#1E1E1E")
    root.resizable(False, False)
    
    # İkon ayarla (opsiyonel)
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    # Özel font tanımları
    title_font = font.Font(family="Segoe UI", size=16, weight="bold")
    button_font = font.Font(family="Segoe UI", size=11, weight="bold")
    label_font = font.Font(family="Segoe UI", size=10)
    
    # Ana çerçeve
    main_frame = tk.Frame(root, bg="#1E1E1E", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    
    # Başlık
    header_frame = tk.Frame(main_frame, bg="#1E1E1E")
    header_frame.pack(fill="x", pady=(0, 20))
    
    title_label = tk.Label(
        header_frame, 
        text="GameBooster - Performans Optimizasyonu", 
        font=title_font, 
        fg="#00BFFF", 
        bg="#1E1E1E"
    )
    title_label.pack(pady=10)
    
    # Sekme kontrolü
    tab_control = ttk.Notebook(main_frame)
    
    # Stil ayarlamaları
    style = ttk.Style()
    style.theme_use('default')
    style.configure('TNotebook', background="#1E1E1E", borderwidth=0)
    style.configure('TNotebook.Tab', background="#2D2D2D", foreground="#FFFFFF", padding=[15, 5])
    style.map('TNotebook.Tab', background=[('selected', '#3D3D3D')], foreground=[('selected', '#00BFFF')])
    
    # Sekme 1: Güç Planları
    power_tab = ttk.Frame(tab_control, style='Tab.TFrame')
    tab_control.add(power_tab, text='  Güç Planları  ')
    
    # Sekme 2: Oyun Optimizasyonu
    game_tab = ttk.Frame(tab_control, style='Tab.TFrame')
    tab_control.add(game_tab, text='  Oyun Modu  ')
    
    # Sekme 3: Ağ Optimizasyonu
    network_tab = ttk.Frame(tab_control, style='Tab.TFrame')
    tab_control.add(network_tab, text='  Ağ Optimizasyonu  ')
    
    # Sekme 4: Tam Optimizasyon
    full_tab = ttk.Frame(tab_control, style='Tab.TFrame')
    tab_control.add(full_tab, text='  Tam Optimizasyon  ')
    
    tab_control.pack(expand=1, fill="both")
    
    style.configure('Tab.TFrame', background="#2D2D2D")
    
    # Güç Planları sekmesi içeriği
    power_frame = tk.Frame(power_tab, bg="#2D2D2D", padx=20, pady=20)
    power_frame.pack(fill="both", expand=True)
    
    power_label = tk.Label(
        power_frame, 
        text="Güç Planı Seçin", 
        font=button_font, 
        fg="white", 
        bg="#2D2D2D"
    )
    power_label.pack(pady=(10, 20))
    
    # Buton stili
    button_style = {
        "font": button_font,
        "borderwidth": 0,
        "highlightthickness": 0,
        "relief": "flat",
        "cursor": "hand2",
        "width": 25,
        "height": 2
    }
    
    # Balanced butonu
    btn_balanced = tk.Button(
        power_frame, 
        text="Balanced", 
        command=lambda: change_power_plan(BALANCED, "Balanced"), 
        bg="#3498db", 
        fg="white", 
        **button_style
    )
    btn_balanced.pack(pady=10)
    
    # High Performance butonu
    btn_high = tk.Button(
        power_frame, 
        text="High Performance", 
        command=lambda: change_power_plan(HIGH_PERFORMANCE, "High Performance", restart_exp=True), 
        bg="#e67e22", 
        fg="white", 
        **button_style
    )
    btn_high.pack(pady=10)
    
    # Ultimate Performance butonu
    btn_ultimate = tk.Button(
        power_frame, 
        text="Ultimate Performance", 
        command=lambda: change_power_plan(ULTIMATE, "Ultimate Performance", restart_exp=True), 
        bg="#e74c3c", 
        fg="white", 
        **button_style
    )
    btn_ultimate.pack(pady=10)
    
    # Oyun Modu sekmesi içeriği
    game_frame = tk.Frame(game_tab, bg="#2D2D2D", padx=20, pady=20)
    game_frame.pack(fill="both", expand=True)
    
    game_label = tk.Label(
        game_frame, 
        text="Oyun Optimizasyonu", 
        font=button_font, 
        fg="white", 
        bg="#2D2D2D"
    )
    game_label.pack(pady=(10, 20))
    
    game_description = tk.Label(
        game_frame, 
        text="Bu mod, sisteminizdeki gereksiz arka plan işlemlerini kapatır, \n"
             "güç planını maksimum performansa ayarlar ve Windows'un oyun \n"
             "performansını engelleyen özelliklerini devre dışı bırakır.",
        font=label_font, 
        fg="#CCCCCC", 
        bg="#2D2D2D",
        justify="left"
    )
    game_description.pack(pady=10)
    
    # Oyun Modu Başlat butonu
    btn_game_mode = tk.Button(
        game_frame, 
        text="Oyun Modu Optimizasyonunu Başlat", 
        command=lambda: run_in_background(optimize_for_gaming), 
        bg="#9b59b6", 
        fg="white", 
        **button_style
    )
    btn_game_mode.pack(pady=20)
    
    # Ağ Optimizasyonu sekmesi içeriği
    network_frame = tk.Frame(network_tab, bg="#2D2D2D", padx=20, pady=20)
    network_frame.pack(fill="both", expand=True)
    
    network_label = tk.Label(
        network_frame, 
        text="Ağ Optimizasyonu", 
        font=button_font, 
        fg="white", 
        bg="#2D2D2D"
    )
    network_label.pack(pady=(10, 20))
    
    network_description = tk.Label(
        network_frame, 
        text="TCP/IP ayarlarını optimize eder, DNS önbelleğini temizler ve \n"
             "Windows Soket katmanını sıfırlar. Bu işlem ağ performansını \n"
             "artırır ve ping süresini azaltmaya yardımcı olur.",
        font=label_font, 
        fg="#CCCCCC", 
        bg="#2D2D2D",
        justify="left"
    )
    network_description.pack(pady=10)
    
    # Ağ Optimizasyonu Başlat butonu
    btn_network = tk.Button(
        network_frame, 
        text="Ağ Optimizasyonunu Başlat", 
        command=lambda: run_in_background(optimize_network), 
        bg="#2ecc71", 
        fg="white", 
        **button_style
    )
    btn_network.pack(pady=20)
    
    # Tam Optimizasyon sekmesi içeriği
    full_frame = tk.Frame(full_tab, bg="#2D2D2D", padx=20, pady=20)
    full_frame.pack(fill="both", expand=True)
    
    full_label = tk.Label(
        full_frame, 
        text="Tam Sistem Optimizasyonu", 
        font=button_font, 
        fg="white", 
        bg="#2D2D2D"
    )
    full_label.pack(pady=(10, 20))
    
    full_description = tk.Label(
        full_frame, 
        text="Bu mod tüm optimizasyon işlemlerini bir arada yapar: \n"
             "• Güç planını Ultimate Performance'a ayarlar \n"
             "• Ağ ayarlarını optimize eder \n"
             "• İşletim sistemi performansını artırır \n"
             "• Windows görsel efektlerini kapatır \n"
             "• Windows Explorer'ı yeniden başlatır \n",
        font=label_font, 
        fg="#CCCCCC", 
        bg="#2D2D2D",
        justify="left"
    )
    full_description.pack(pady=10)
    
    # Tam Optimizasyon Başlat butonu
    btn_full = tk.Button(
        full_frame, 
        text="Tam Optimizasyonu Başlat", 
        command=lambda: run_in_background(optimize_all), 
        bg="#1abc9c", 
        fg="white", 
        **button_style
    )
    btn_full.pack(pady=20)
    
    # Durum etiketi
    status_frame = tk.Frame(main_frame, bg="#1E1E1E")
    status_frame.pack(fill="x", side="bottom", pady=10)
    
    status_label = tk.Label(
        status_frame, 
        text="Hazır", 
        font=label_font, 
        fg="#CCCCCC", 
        bg="#1E1E1E"
    )
    status_label.pack(pady=5)
    
    # Çıkış tuşu
    footer_frame = tk.Frame(main_frame, bg="#1E1E1E")
    footer_frame.pack(fill="x", side="bottom")
    
    exit_button = tk.Button(
        footer_frame, 
        text="Çıkış", 
        command=root.destroy, 
        bg="#7f8c8d", 
        fg="white", 
        font=label_font,
        width=10
    )
    exit_button.pack(side="right", pady=5)
    
    # Telif hakkı etiketi
    copyright_label = tk.Label(
        footer_frame, 
        text="© 2025 GameBooster", 
        font=("Segoe UI", 8), 
        fg="#666666", 
        bg="#1E1E1E"
    )
    copyright_label.pack(side="left", pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()