import tkinter as tk
from tkinter import filedialog, messagebox

from app.hoop_engine import mediNote_hoop_engine, load_from_json, load_from_csv


def run_gui() -> None:
    def load_patient_file() -> None:
        file_path = filedialog.askopenfilename(
            title="Select Patient JSON/CSV",
            filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")],
        )
        if not file_path:
            return
        try:
            if file_path.lower().endswith(".json"):
                patient_data = load_from_json(file_path)
            else:
                patient_data = load_from_csv(file_path)
        except Exception as exc:  # pragma: no cover - GUI error
            messagebox.showerror("Error", f"Failed to load file:\n{exc}")
            return

        results = mediNote_hoop_engine(patient_data)
        output = ["ICD-10 Codes:"] + results["ICD10"] + ["", "Assessment & Plan:"]
        output += results["Assessment_Plan"]
        messagebox.showinfo("MediNote Results", "\n".join(output))

    root = tk.Tk()
    root.title("MediNote HOOP Engine")
    tk.Button(root, text="Load Patient Data", command=load_patient_file).pack(
        padx=40, pady=40
    )
    root.mainloop()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    run_gui()
