import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import subprocess
import platform
import threading
from tkinter.simpledialog import askstring
import os


class UniversalInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Omni-Manager")
        self.root.geometry("500x400")

        self.os_type = self.detect_os()
        self.os_label = tk.Label(root, text=f"Operating System: {self.os_type}")
        self.os_label.pack(pady=10)

        self.update_var = tk.BooleanVar()
        self.upgrade_var = tk.BooleanVar()

        self.update_check = tk.Checkbutton(root, text="Update All", variable=self.update_var)
        self.upgrade_check = tk.Checkbutton(root, text="Upgrade All", variable=self.upgrade_var)

        if self.os_type != "Windows":
            self.update_check.pack(anchor="w", padx=20)
        self.upgrade_check.pack(anchor="w", padx=20)

        self.search_label = tk.Label(root, text="Enter Program Name(s):")
        self.search_label.pack(pady=10)

        self.program_entry = tk.Entry(root, width=40)
        self.program_entry.pack(pady=5)

        self.search_button = tk.Button(root, text="Search", command=self.search_program)
        self.search_button.pack(pady=10)

        self.install_button = tk.Button(root, text="Install", command=self.install_program)
        self.install_button.pack(pady=10)

        self.search_results = []
        self.current_page = 0
        self.selected_program = None

        self.install_progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        self.install_progress.pack(pady=5)
        self.install_progress.pack_forget()

        if self.os_type == "Mac":
            self.check_and_install_brew()

    def install_windows(self, program_name):
        package_manager = self.package_manager_var.get()
        install_command = None  

        if package_manager == "winget":
            install_command = ["winget", "install", program_name]
        elif package_manager == "chocolatey":
            install_command = ["choco", "install", program_name]
        else:
            messagebox.showerror("Error", "Unsupported package manager selected.")
            return
        if install_command:
            try:
                subprocess.run(install_command, check=True)
                messagebox.showinfo("Success", f"{program_name} installed successfully.")
            except subprocess.CalledProcessError:
                messagebox.showerror("Installation failed", f"Failed to install {program_name}.")
        else:
            messagebox.showerror("Error", "Failed to generate install command.")

    def search_linux(self, program_name):
        try:
            package_manager = self.detect_package_manager()
            if package_manager is None:
                return []

            search_command = []

            if package_manager == "apt":
                search_command = ["apt-cache", "search", program_name]
            elif package_manager == "dnf":
                search_command = ["dnf", "search", program_name]
            elif package_manager == "pacman":
                search_command = ["pacman", "-Ss", program_name]
            elif package_manager == "flatpak":
                search_command = ["flatpak", "search", program_name]
            elif package_manager == "zypper":
                search_command = ["zypper", "search", program_name]
            elif package_manager == "yum":
                search_command = ["yum", "search", program_name]
            elif package_manager == "snap":
                search_command = ["snap", "find", program_name]
            elif package_manager == "guix":
                search_command = ["guix", "search", program_name]
            else:
                raise ValueError("Unsupported package manager.")

            self.toggle_buttons(state=tk.DISABLED)
            result = subprocess.run(search_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.toggle_buttons(state=tk.NORMAL)

            if result.returncode == 0:
                output = result.stdout.splitlines()
                return self.parse_search_output(output)
            else:
                messagebox.showerror("Error", f"Search command failed with exit code {result.returncode}.")
                return []
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return []
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            return []

    def detect_package_manager(self):
        package_managers = {
            "apt": ["which", "apt"],
            "dnf": ["which", "dnf"],
            "pacman": ["which", "pacman"],
            "flatpak": ["which", "flatpak"],
            "zypper": ["which", "zypper"],
            "yum": ["which", "yum"],
            "snap": ["which", "snap"],
            "guix": ["which", "guix"],
        }

        for manager, command in package_managers.items():
            if subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
                return manager

        messagebox.showerror("Error", "No supported package manager found.")
        return None

    def parse_search_output(self, output):
        results = []
        for line in output:
            if line.strip():
                parts = line.split(" - ", 1)
                if len(parts) == 2:
                    results.append({"name": parts[0].strip(), "description": parts[1].strip()})
                else:
                    results.append({"name": parts[0].strip(), "description": ""})
        return results

    def __init__(self, root):
        self.root = root
        self.root.title("Omni-Manager")
        self.root.geometry("500x400")

        self.os_type = self.detect_os()
        self.os_label = tk.Label(root, text=f"Operating System: {self.os_type}")
        self.os_label.pack(pady=10)

        self.update_var = tk.BooleanVar()
        self.upgrade_var = tk.BooleanVar()
        
        self.update_check = tk.Checkbutton(root, text="Update All", variable=self.update_var)
        self.upgrade_check = tk.Checkbutton(root, text="Upgrade All", variable=self.upgrade_var)

        if self.os_type != "Windows":
            self.update_check.pack(anchor="w", padx=20)
        self.upgrade_check.pack(anchor="w", padx=20)

        self.search_label = tk.Label(root, text="Enter Program Name or ID:")
        self.search_label.pack(pady=10)
        
        self.program_entry = tk.Entry(root, width=40)
        self.program_entry.pack(pady=5)
        
        self.search_button = tk.Button(root, text="Search", command=self.search_program)
        self.search_button.pack(pady=10)

        self.install_button = tk.Button(root, text="Install", command=self.install_program)
        self.install_button.pack(pady=10)

        self.search_results = []
        self.current_page = 0
        self.selected_program = None

        self.install_progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        self.install_progress.pack(pady=5)
        self.install_progress.pack_forget()

        if self.os_type == "Windows":
            self.package_manager_var = tk.StringVar(value="winget")
            tk.Label(self.root, text="Select Package Manager:").pack(pady=10)
            self.package_manager_menu = ttk.OptionMenu(self.root, self.package_manager_var, "winget", "winget", "chocolatey")
            self.package_manager_menu.pack(pady=10)
        elif self.os_type == "Mac":
            self.check_and_install_brew()

    def toggle_buttons(self, state):
        self.search_button.config(state=state)
        self.install_button.config(state=state)

    def check_and_install_chocolatey(self):
        if subprocess.call(["choco", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
            command = (
                'powershell.exe -NoProfile -ExecutionPolicy Bypass '
                '-Command "Set-ExecutionPolicy Bypass -Scope Process -Force; '
                '[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; '
                'iex ((New-Object System.Net.WebClient).DownloadString(\'https://chocolatey.org/install.ps1\'))"'
            )
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            process.communicate()
            if process.returncode != 0:
                messagebox.showerror("Error", "Failed to install Chocolatey.")
            else:
                messagebox.showinfo("Success", "Chocolatey installed successfully.")

    def check_and_install_brew(self):
        if subprocess.call(["brew", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
            command = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            process.communicate()
            if process.returncode != 0:
                messagebox.showerror("Error", "Failed to install Homebrew.")
            else:
                messagebox.showinfo("Success", "Homebrew installed successfully.")

    def search_mac(self, program_name):
        try:
            search_command = ["brew", "search", "--desc", program_name]

            self.toggle_buttons(state=tk.DISABLED)
            result = subprocess.run(search_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.toggle_buttons(state=tk.NORMAL)

            if result.returncode == 0:
                output = result.stdout.splitlines()
                return self.parse_search_output(output)
            else:
                messagebox.showerror("Error", f"Search command failed with exit code {result.returncode}.")
                return []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search for {program_name}: {e}")
            return []

    def search_windows(self, program_name):
        package_manager = self.package_manager_var.get()

        if package_manager == "winget":
            search_command = ["winget", "search", program_name]
        elif package_manager == "chocolatey":
            search_command = ["choco", "search", program_name]
        else:
            messagebox.showerror("Error", "Unsupported package manager selected.")
            return []

        self.toggle_buttons(state=tk.DISABLED)
        try:
            result = subprocess.run(
                search_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True, 
                env=os.environ.copy(), 
                encoding='utf-8' 
            )
            self.toggle_buttons(state=tk.NORMAL)

            if result.returncode == 0 and result.stdout:
                output = result.stdout.splitlines()
                return self.parse_search_output(output)
            else:
                messagebox.showerror("Error", f"Search command failed with exit code {result.returncode}.\nCheck winget_debug_log.txt for details.")
                return []
        except Exception as e:
            self.toggle_buttons(state=tk.NORMAL)
            messagebox.showerror("Error", f"Failed to search for {program_name}: {e}")
            return []

    def detect_os(self):
        os_name = platform.system()
        if os_name == "Windows":
            return "Windows"
        elif os_name == "Linux":
            return "Linux"
        elif os_name == "Darwin":
            return "Mac"
        else:
            return "Unsupported"

    def search_program(self):
        program_name = self.program_entry.get().strip()
        if not program_name:
            messagebox.showerror("Error", "Please enter a program name.")
            return

        if self.os_type == "Linux":
            self.search_results = self.search_linux(program_name)
        elif self.os_type == "Mac":
            self.search_results = self.search_mac(program_name)
        elif self.os_type == "Windows":
            self.search_results = self.search_windows(program_name)
        else:
            messagebox.showerror("Error", "Unsupported operating system.")
            return

        if self.search_results:
            self.current_page = 0
            self.open_results_window()
        else:
            messagebox.showinfo("Search", "No results found.")

    def open_results_window(self):
        self.results_window = Toplevel(self.root)
        self.results_window.title("Search Results")
        self.results_window.geometry("500x400")

        self.results_listbox = tk.Listbox(self.results_window, width=80, height=10)
        self.results_listbox.pack(pady=10)

        self.prev_button = tk.Button(self.results_window, text="Previous Page", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_button = tk.Button(self.results_window, text="Next Page", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.select_button = tk.Button(self.results_window, text="Select", command=self.select_program)
        self.select_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.update_results_listbox()

    def update_results_listbox(self):
        self.results_listbox.delete(0, tk.END)
        start_index = self.current_page * 10
        end_index = start_index + 10
        results_to_display = self.search_results[start_index:end_index]

        for result in results_to_display:
            display_text = result["name"]
            if result["description"]:
                display_text += f": {result['description']}"
            self.results_listbox.insert(tk.END, display_text)

        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if end_index < len(self.search_results) else tk.DISABLED)

    def next_page(self):
        self.current_page += 1
        self.update_results_listbox()

    def prev_page(self):
        self.current_page -= 1
        self.update_results_listbox()

    def select_program(self):
        selected_index = self.results_listbox.curselection()
        if selected_index:
            selected_text = self.results_listbox.get(selected_index)

            program_name = selected_text.split()[0].split(":")[0]
            if self.os_type == "Windows" and self.package_manager_var.get() == "winget":
                columns = selected_text.split() 
                program_name = columns[-3] 

            self.selected_program = program_name
            self.program_entry.delete(0, tk.END)
            self.program_entry.insert(0, self.selected_program)
            self.results_window.destroy()


    def run_install_command_windows(self, install_command):
        command = [
            'powershell.exe',
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            'Start-Process',
            'powershell.exe',
            '-ArgumentList', f"'-NoProfile -ExecutionPolicy Bypass -Command \"{install_command}\"'",
            '-Verb', 'RunAs'
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"ERROR: {stderr.strip()}")
            return (False, stderr.strip())
        return (True, stdout.strip())

    def run_install_command(self, install_command, password=None, use_sudo=False):
        if use_sudo and password:
            command = f'echo {password} | sudo -S {install_command}'
        else:
            command = install_command

        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            for line in process.stdout:
                self.root.update_idletasks()

            process.wait()
            return process.returncode

    def install_program(self):
        programs = self.program_entry.get().strip().split()
        if not programs and not self.update_var.get() and not self.upgrade_var.get():
            messagebox.showerror("Error", "Please select a program to install, or choose update/upgrade.")
            return

        self.install_progress.pack()
        self.install_progress.start()

        self.toggle_buttons(state=tk.DISABLED)

        def install():
            password = None
            success = True
            try:
                commands = []
                if self.os_type == "Linux":
                    package_manager = self.detect_package_manager()
                    if package_manager:
                        if self.update_var.get():
                            commands.append((f"sudo -S {package_manager} update -y", True))
                        if self.upgrade_var.get():
                            commands.append((f"sudo -S {package_manager} upgrade -y", True))
                        if programs:
                            install_command = f"{package_manager} install -y {' '.join(programs)}"
                            commands.append((install_command, True))
                elif self.os_type == "Mac":
                    if self.update_var.get():
                        commands.append(("brew update", False))
                    if self.upgrade_var.get():
                        commands.append(("brew upgrade", False))
                    if programs:
                        install_command = f"brew install {' '.join(programs)}"
                        commands.append((install_command, False))
                elif self.os_type == "Windows":
                    package_manager = self.package_manager_var.get()
                    if package_manager == "winget":
                        if self.upgrade_var.get():
                            commands.append(("winget upgrade --all", False))
                        if programs:
                            install_command = f"winget install {' '.join(programs)} --accept-source-agreements --accept-package-agreements"
                            commands.append((install_command, False))
                    elif package_manager == "chocolatey":
                        if self.upgrade_var.get():
                            commands.append(("choco upgrade all -y", False))
                        if programs:
                            install_command = f"choco install {' '.join(programs)} -y"
                            commands.append((install_command, False))
                                    
                    for command, _ in commands:
                        command_success, output = self.run_install_command_windows(command)
                        if not command_success:
                            error_message = (
                                f"Unfortunately, the installation command failed.\n\n"
                                f"Command: {command}\n"
                                f"Error: {output}"
                            )
                            messagebox.showerror("Installation Failed", error_message)
                            success = False
                            break

                else:
                    messagebox.showerror("Error", "Unsupported operating system.")
                    return

                for command, use_sudo in commands:
                    if use_sudo and password is None:
                        password = self.prompt_for_password()
                    returncode = self.run_install_command(command, password=password, use_sudo=use_sudo)
                    if returncode != 0:
                        error_message = (
                            f"Unfortunately, the installation command failed.\n\n"
                            f"Command: {command}\n"
                            f"Exit Code: {returncode}."
                        )
                        messagebox.showerror("Installation Failed", error_message)
                        success = False
                        break

                if success and self.os_type != "Windows":
                    messagebox.showinfo("Success", "All commands executed successfully.")

            except Exception as e:
                messagebox.showerror("Error", f"Installation failed: {e}")
            finally:
                self.install_progress.stop()
                self.install_progress.pack_forget()
                self.toggle_buttons(state=tk.NORMAL)

        self.install_thread = threading.Thread(target=install)
        self.install_thread.start()
        self.root.after(100, self.check_install_thread)

    def check_install_thread(self):
        if self.install_thread.is_alive():
            self.root.after(100, self.check_install_thread)
        else:
            if hasattr(self, 'install_thread_success') and self.install_thread_success:
                messagebox.showinfo("Success", "All commands executed successfully.")
                del self.install_thread_success
            elif hasattr(self, 'install_thread_success'):
                del self.install_thread_success

    def install_thread_complete(self):
        self.install_thread_success = True

    def prompt_for_password(self):
        return askstring("Password", "Please enter your sudo password:", show="*")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalInstallerApp(root)
    root.mainloop()
