import tkinter as tk
from tkinter import ttk, messagebox
import math

try:
    import mpmath as mp
except ImportError:
    raise SystemExit("Installe mpmath avec : pip install mpmath")

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
except ImportError:
    raise SystemExit("Installe matplotlib avec : pip install matplotlib")


N = 7


class Prisme7FacesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur 3D — 7 côtés / 7 faces")
        self.root.geometry("1280x820")

        main = ttk.Frame(root, padding=10)
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 12))

        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(
            left,
            text="Générateur — 7 côtés / 7 faces",
            font=("Arial", 17, "bold")
        ).pack(anchor="w", pady=(0, 10))

        ttk.Label(
            left,
            text=(
                "Structure : prisme heptagonal ouvert\n"
                "7 côtés réguliers autour\n"
                "7 faces latérales\n"
                "aucune face de dessus/dessous"
            ),
            justify="left"
        ).pack(anchor="w", pady=(0, 12))

        ttk.Label(left, text="Rayon centre → sommet (cm)").pack(anchor="w")
        self.radius_var = tk.StringVar(value="10")
        ttk.Entry(left, textvariable=self.radius_var, width=16).pack(
            anchor="w", pady=(0, 8)
        )

        ttk.Label(left, text="Hauteur (cm)").pack(anchor="w")
        self.height_var = tk.StringVar(value="10")
        ttk.Entry(left, textvariable=self.height_var, width=16).pack(
            anchor="w", pady=(0, 8)
        )

        ttk.Label(left, text="Rotation de départ (°)").pack(anchor="w")
        self.rotation_var = tk.StringVar(value="0")
        ttk.Entry(left, textvariable=self.rotation_var, width=16).pack(
            anchor="w", pady=(0, 8)
        )

        ttk.Label(left, text="Précision décimale").pack(anchor="w")
        self.precision_var = tk.IntVar(value=30)
        ttk.Spinbox(
            left,
            from_=8,
            to=80,
            textvariable=self.precision_var,
            width=12
        ).pack(anchor="w", pady=(0, 10))

        ttk.Button(
            left,
            text="Générer / Recalculer",
            command=self.generate
        ).pack(fill="x", pady=4)

        ttk.Separator(left).pack(fill="x", pady=12)

        self.info = tk.Text(
            left,
            width=54,
            height=34,
            wrap="none"
        )
        self.info.pack(fill="both", expand=True)

        self.fig = plt.Figure(figsize=(7.7, 7.2), dpi=100)
        self.ax = self.fig.add_subplot(111, projection="3d")

        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.generate()

    def calculate(self):
        digits = int(self.precision_var.get())
        digits = max(8, min(80, digits))
        mp.mp.dps = digits + 15

        R = mp.mpf(self.radius_var.get())
        H = mp.mpf(self.height_var.get())
        start_deg = mp.mpf(self.rotation_var.get())

        if R <= 0 or H <= 0:
            raise ValueError("Le rayon et la hauteur doivent être supérieurs à 0.")

        angle_step_deg = mp.mpf(360) / N
        angle_step_rad = 2 * mp.pi / N
        half_step = mp.pi / N

        # Longueur exacte de chacun des 7 côtés.
        side_length = 2 * R * mp.sin(half_step)

        # Apothème : centre -> milieu d'un côté.
        apothem = R * mp.cos(half_step)

        bottom = []
        top = []

        for i in range(N):
            a_deg = start_deg + i * angle_step_deg
            a = mp.radians(a_deg)

            x = R * mp.cos(a)
            y = R * mp.sin(a)

            bottom.append((x, y, mp.mpf("0")))
            top.append((x, y, H))

        # 7 faces latérales exactement.
        faces = []
        for i in range(N):
            j = (i + 1) % N
            faces.append([
                bottom[i],
                bottom[j],
                top[j],
                top[i]
            ])

        perimeter = N * side_length
        lateral_area = perimeter * H
        base_area = mp.mpf("0.5") * perimeter * apothem

        return {
            "digits": digits,
            "R": R,
            "H": H,
            "start_deg": start_deg,
            "angle_step_deg": angle_step_deg,
            "angle_step_rad": angle_step_rad,
            "side_length": side_length,
            "apothem": apothem,
            "perimeter": perimeter,
            "lateral_area": lateral_area,
            "base_area": base_area,
            "bottom": bottom,
            "top": top,
            "faces": faces,
        }

    def generate(self):
        try:
            data = self.calculate()
        except Exception as exc:
            messagebox.showerror("Erreur", str(exc))
            return

        digits = data["digits"]
        fmt = lambda v: mp.nstr(v, digits)

        self.info.delete("1.0", tk.END)

        self.info.insert(
            tk.END,
            "STRUCTURE\n"
            "=========\n"
            "Nombre de côtés autour : 7\n"
            "Nombre de faces latérales : 7\n"
            "Face du dessus : absente\n"
            "Face du dessous : absente\n\n"
        )

        self.info.insert(
            tk.END,
            "MESURES EXACTES\n"
            "===============\n"
            f"360 / 7 = {fmt(data['angle_step_deg'])}°\n"
            f"Rayon centre → sommet = {fmt(data['R'])} cm\n"
            f"Apothème centre → côté = {fmt(data['apothem'])} cm\n"
            f"Longueur de chaque côté = {fmt(data['side_length'])} cm\n"
            f"Périmètre = {fmt(data['perimeter'])} cm\n"
            f"Hauteur = {fmt(data['H'])} cm\n"
            f"Aire d'une base théorique = {fmt(data['base_area'])} cm²\n"
            f"Aire latérale totale (7 faces) = {fmt(data['lateral_area'])} cm²\n"
            f"Aire d'une face latérale = {fmt(data['side_length'] * data['H'])} cm²\n\n"
        )

        self.info.insert(
            tk.END,
            "SOMMETS BAS\n"
            "===========\n"
        )
        for i, p in enumerate(data["bottom"], 1):
            self.info.insert(
                tk.END,
                f"B{i}: X={fmt(p[0])}  Y={fmt(p[1])}  Z={fmt(p[2])}\n"
            )

        self.info.insert(
            tk.END,
            "\nSOMMETS HAUT\n"
            "============\n"
        )
        for i, p in enumerate(data["top"], 1):
            self.info.insert(
                tk.END,
                f"H{i}: X={fmt(p[0])}  Y={fmt(p[1])}  Z={fmt(p[2])}\n"
            )

        self.info.insert(
            tk.END,
            "\nFACES\n"
            "=====\n"
        )
        for i in range(N):
            j = (i + 1) % N
            self.info.insert(
                tk.END,
                f"Face {i+1}: B{i+1} → B{j+1} → H{j+1} → H{i+1}\n"
            )

        # Dessin 3D
        self.ax.clear()

        faces_float = []
        for face in data["faces"]:
            faces_float.append([
                (float(p[0]), float(p[1]), float(p[2]))
                for p in face
            ])

        poly = Poly3DCollection(
            faces_float,
            alpha=0.35
        )
        self.ax.add_collection3d(poly)

        # Tracer toutes les arêtes.
        bottom = [(float(x), float(y), float(z)) for x, y, z in data["bottom"]]
        top = [(float(x), float(y), float(z)) for x, y, z in data["top"]]

        for ring in (bottom, top):
            for i in range(N):
                j = (i + 1) % N
                self.ax.plot(
                    [ring[i][0], ring[j][0]],
                    [ring[i][1], ring[j][1]],
                    [ring[i][2], ring[j][2]],
                    linewidth=1.5
                )

        for i in range(N):
            self.ax.plot(
                [bottom[i][0], top[i][0]],
                [bottom[i][1], top[i][1]],
                [bottom[i][2], top[i][2]],
                linewidth=1.5
            )

        # Sommets et numéros.
        for i, p in enumerate(bottom, 1):
            self.ax.scatter([p[0]], [p[1]], [p[2]], s=45)
            self.ax.text(p[0], p[1], p[2], f" B{i}")

        for i, p in enumerate(top, 1):
            self.ax.scatter([p[0]], [p[1]], [p[2]], s=45)
            self.ax.text(p[0], p[1], p[2], f" H{i}")

        # Centre géométrique.
        cz = float(data["H"]) / 2.0
        self.ax.scatter([0], [0], [cz], s=80)
        self.ax.text(0, 0, cz, " Centre")

        lim = float(data["R"]) * 1.25
        zmax = float(data["H"]) * 1.15

        self.ax.set_xlim(-lim, lim)
        self.ax.set_ylim(-lim, lim)
        self.ax.set_zlim(0, zmax)

        self.ax.set_xlabel("X (cm)")
        self.ax.set_ylabel("Y (cm)")
        self.ax.set_zlabel("Z (cm)")
        self.ax.set_box_aspect((1, 1, max(0.5, float(data["H"]) / (2.0 * float(data["R"])))))

        self.ax.set_title(
            "Prisme heptagonal ouvert — 7 côtés / 7 faces latérales"
        )

        self.canvas.draw_idle()


if __name__ == "__main__":
    root = tk.Tk()
    app = Prisme7FacesApp(root)
    root.mainloop()