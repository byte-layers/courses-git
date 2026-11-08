#!/usr/bin/env python3
"""Génère les animations GIF des cours Git. Usage : python3 tools/make_gifs.py [--sheet fichier.png]
Dépend de Pillow et d'une police Helvetica (chemin macOS ci-dessous, à adapter ailleurs)."""
import math, sys
from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Helvetica.ttc"
K = 2
BG = (255, 255, 255)
PV, PV_L = (79, 91, 213), (220, 223, 247)
PK, PK_L = (192, 55, 143), (250, 224, 240)
GN, GN_L = (4, 108, 78), (214, 245, 231)
GY, GY_L = (82, 82, 106), (236, 236, 244)
RD, RD_L = (185, 28, 28), (254, 226, 226)
TX = (11, 11, 18)
STYLES = {"c": (PV_L, PV), "new": (PK_L, PK), "branch": (GN_L, GN), "head": (PK_L, PK), "remote": (GY_L, GY),
          "card": (GY_L, GY), "ok": (GN_L, GN), "bad": (RD_L, RD), "zone": ((248, 248, 252), (212, 212, 226))}
fonts = {}


def font(size):
    return fonts.setdefault(size, ImageFont.truetype(FONT, size * K))


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class Anim:
    def __init__(self, name, course, w=640, h=420):
        self.name, self.course, self.w, self.h = name, course, w, h
        self.s, self.keys = {}, []

    def node(self, id, kind, text, x, y, style=None, fro=None, **kw):
        self.s[id] = dict(kind=kind, text=text, x=x, y=y, style=style or ("c" if kind == "commit" else "branch"), a=1, fro=fro, **kw)

    def commit(self, id, text, x, y, style="c", fro=None):
        self.node(id, "commit", text, x, y, style, fro)

    def pill(self, id, text, x, y, style="branch", fro=None):
        self.node(id, "pill", text, x, y, style, fro)

    def card(self, id, text, x, y, style="card", fro=None):
        self.node(id, "card", text, x, y, style, fro)

    def zone(self, id, text, x, y, w, h):
        self.node(id, "zone", text, x, y, "zone", None, w=w, h=h)

    def edge(self, a, b, color=PV):
        self.s["E:%s:%s" % (a, b)] = dict(kind="edge", a_id=a, b_id=b, color=color, a=1)

    def move(self, id, x=None, y=None):
        if x is not None:
            self.s[id]["x"] = x
        if y is not None:
            self.s[id]["y"] = y

    def text(self, id, text):
        self.s[id]["text"] = text

    def rm(self, *ids):
        for i in ids:
            del self.s[i]

    def key(self, caption, hold=1500, color=GY, steps=9):
        self.keys.append(dict(state={k: dict(v) for k, v in self.s.items()}, caption=caption, hold=hold, color=color, steps=steps))

    def lerp(self, a, b, t):
        out = {}
        for i in set(a) | set(b):
            if i in a and i in b:
                n = dict(b[i])
                if n["kind"] != "edge":
                    n["x"] = a[i]["x"] + (b[i]["x"] - a[i]["x"]) * t
                    n["y"] = a[i]["y"] + (b[i]["y"] - a[i]["y"]) * t
                    if t < .5:
                        n["text"] = a[i]["text"]
            elif i in b:
                n = dict(b[i])
                n["a"] = t
                if n.get("fro"):
                    n["x"] = n["fro"][0] + (b[i]["x"] - n["fro"][0]) * t
                    n["y"] = n["fro"][1] + (b[i]["y"] - n["fro"][1]) * t
            else:
                n = dict(a[i])
                n["a"] = 1 - t
            out[i] = n
        return out

    def size(self, n, d):
        if n["kind"] == "commit":
            return 31 * K, 31 * K
        lines = n["text"].split("\n")
        f = font(17)
        tw = max(d.textlength(l, font=f) for l in lines)
        return tw / 2 + 16 * K, (11 * len(lines) + 5) * K

    def anchor(self, a, b, d):
        ax, ay, bx, by = a["x"] * K, a["y"] * K, b["x"] * K, b["y"] * K
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        def trim(n):
            hw, hh = self.size(n, d)
            if n["kind"] == "commit":
                return hw + 2 * K
            return min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9) * L + 2 * K
        ua, ub = trim(a), trim(b)
        return (ax + dx / L * ua, ay + dy / L * ua), (bx - dx / L * ub, by - dy / L * ub)

    def draw(self, st, caption, color):
        im = Image.new("RGB", (self.w * K, self.h * K), BG)
        d = ImageDraw.Draw(im)
        order = {"zone": 0, "edge": 1, "commit": 2, "card": 3, "pill": 4}
        for i, n in sorted(st.items(), key=lambda kv: (order[kv[1]["kind"]], kv[0])):
            al = max(0, min(1, n["a"]))
            if n["kind"] == "edge":
                if n["a_id"] not in st or n["b_id"] not in st:
                    continue
                al = min(al, st[n["a_id"]]["a"], st[n["b_id"]]["a"])
                p, q = self.anchor(st[n["a_id"]], st[n["b_id"]], d)
                c = mix(BG, n["color"], al)
                ang = math.atan2(q[1] - p[1], q[0] - p[0])
                d.line([p, q], fill=c, width=3 * K)
                L = 12 * K
                d.polygon([q, (q[0] - L * math.cos(ang - .45), q[1] - L * math.sin(ang - .45)),
                           (q[0] - L * math.cos(ang + .45), q[1] - L * math.sin(ang + .45))], fill=c)
                continue
            fill, line = STYLES[n["style"]]
            fill, line, tx = mix(BG, fill, al), mix(BG, line, al), mix(BG, TX, al)
            x, y = n["x"] * K, n["y"] * K
            if n["kind"] == "zone":
                hw, hh = n["w"] * K / 2, n["h"] * K / 2
                d.rounded_rectangle([x - hw, y - hh, x + hw, y + hh], radius=12 * K, fill=fill, outline=line, width=2 * K)
                d.text((x, y - hh + 20 * K), n["text"], font=font(16), fill=mix(BG, GY, al), anchor="mm")
            elif n["kind"] == "commit":
                r = 31 * K
                d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=line, width=3 * K)
                d.text((x, y), n["text"], font=font(20), fill=tx, anchor="mm")
            else:
                hw, hh = self.size(n, d)
                rad = hh if n["kind"] == "pill" else 7 * K
                d.rounded_rectangle([x - hw, y - hh, x + hw, y + hh], radius=int(rad), fill=fill, outline=line, width=2 * K)
                col = line if n["kind"] == "pill" else tx
                d.multiline_text((x, y), n["text"], font=font(17), fill=col, anchor="mm", align="center", spacing=5 * K)
        d.text((self.w * K / 2, (self.h - 24) * K), caption, font=font(17), fill=color, anchor="mm")
        return im.resize((self.w, self.h), Image.LANCZOS)

    def render(self):
        frames, times = [], []
        prev = None
        # Les animations à 4 étapes ou plus laissent plus de temps pour lire chaque étape.
        slow = len(self.keys) >= 4
        hold_factor, tween_ms = (1.7, 90) if slow else (1, 60)
        for k in self.keys:
            if prev is not None:
                for j in range(1, k["steps"] + 1):
                    t = j / k["steps"]
                    t = t * t * (3 - 2 * t)
                    frames.append(self.draw(self.lerp(prev, k["state"], t), k["caption"], k["color"]))
                    times.append(tween_ms)
            frames.append(self.draw(k["state"], k["caption"], k["color"]))
            times.append(int(k["hold"] * hold_factor))
            prev = k["state"]
        times[-1] += 1400
        out = [f.convert("P", palette=Image.ADAPTIVE, colors=96) for f in frames]
        path = "%s/.layers/assets/%s.gif" % (self.course, self.name)
        out[0].save(path, save_all=True, append_images=out[1:], duration=times, loop=0, optimize=True, disposal=2)
        return frames, path


def commit_and_branch():
    a = Anim("commit-et-branche", "git-first-commits", 560, 380)
    a.commit("C1", "C1", 190, 95)
    a.pill("main", "main", 375, 95)
    a.edge("main", "C1", GN)
    a.key("Avant : main désigne C1")
    a.commit("C2", "C2", 190, 245, fro=(190, 200))
    a.edge("C2", "C1")
    a.key("git commit crée C2, dont le parent est C1", color=PV)
    a.rm("E:main:C1")
    a.edge("main", "C2", GN)
    a.move("main", y=245)
    a.key("Après : main avance et désigne C2", color=GN, hold=1800)
    return a


def lifecycle():
    a = Anim("cycle-local", "git-first-commits")
    a.zone("z1", "Dossier de travail", 110, 190, 190, 340)
    a.zone("z2", "Zone de préparation", 320, 190, 190, 340)
    a.zone("z3", "Dépôt local (.git)", 530, 190, 190, 340)
    a.commit("C1", "C1", 530, 95)
    a.pill("main", "main", 530, 300)
    a.edge("main", "C1", GN)
    a.key("Un dépôt propre : tout est enregistré dans C1")
    a.card("runbook", "runbook.md", 110, 120, fro=(110, 90))
    a.card("index", "index.html", 110, 200, fro=(110, 170))
    a.key("Je modifie deux fichiers")
    a.move("runbook", x=320)
    a.move("index", x=320)
    a.key("git add runbook.md index.html", color=PV)
    a.move("index", x=110)
    a.key("git restore --staged index.html : ce fichier sort de la préparation", color=PK)
    a.rm("runbook", "E:main:C1")
    a.commit("C2", "C2", 530, 205, fro=(320, 120))
    a.edge("C2", "C1")
    a.edge("main", "C2", GN)
    a.key("git commit crée C2 avec runbook.md, et main avance", color=PV)
    a.key("index.html reste modifié dans le dossier, prêt pour un autre commit", color=GN, hold=1800)
    return a


def switch():
    a = Anim("switch-branche", "git-branches-merge")
    a.commit("C1", "C1", 130, 90)
    a.pill("main", "main", 300, 70)
    a.edge("main", "C1", GN)
    a.pill("HEAD", "HEAD", 400, 70, "head")
    a.card("file", "index.html\nStatut", 530, 150)
    a.key("Vous êtes sur main : HEAD la désigne")
    a.pill("db", "feature/db", 310, 130)
    a.edge("db", "C1", GN)
    a.key("git branch feature/db crée un second nom sur le même commit", color=PV)
    a.move("HEAD", x=425, y=130)
    a.key("git switch feature/db : HEAD change de branche", color=PK)
    a.commit("C2", "C2", 130, 235, fro=(130, 190))
    a.edge("C2", "C1")
    a.rm("E:db:C1")
    a.edge("db", "C2", GN)
    a.move("db", y=235)
    a.move("HEAD", y=235)
    a.text("file", "index.html\nStatut\nBase : OK")
    a.key("git commit : la branche avance, le fichier change", color=PV)
    a.move("HEAD", x=400, y=70)
    a.text("file", "index.html\nStatut")
    a.key("git switch main : vos fichiers reviennent à l'état de main", color=PK, hold=1800)
    return a


def fast_forward():
    a = Anim("merge-fast-forward", "git-branches-merge")
    a.commit("C1", "C1", 170, 90)
    a.commit("C2", "C2", 170, 240)
    a.edge("C2", "C1")
    a.pill("main", "main", 350, 90)
    a.edge("main", "C1", GN)
    a.pill("db", "feature/db", 360, 240)
    a.edge("db", "C2", GN)
    a.key("main n'a pas bougé depuis la création de feature/db")
    a.rm("E:main:C1")
    a.edge("main", "C2", GN)
    a.move("main", y=185)
    a.key("git merge feature/db : fast-forward, main avance simplement", color=PV, hold=1800)
    return a


def merge_commit():
    a = Anim("merge-commit", "git-branches-merge")
    a.commit("C1", "C1", 250, 65)
    a.commit("C2", "C2", 130, 165)
    a.commit("C3", "C3", 370, 165)
    a.edge("C2", "C1")
    a.edge("C3", "C1")
    a.pill("main", "main", 50, 165)
    a.edge("main", "C2", GN)
    a.pill("api", "feature/api", 510, 165)
    a.edge("api", "C3", GN)
    a.key("Les historiques ont divergé : chaque branche a son propre commit")
    a.commit("M", "M", 250, 280, "new", fro=(250, 240))
    a.edge("M", "C2", PK)
    a.edge("M", "C3", PK)
    a.rm("E:main:C2")
    a.edge("main", "M", GN)
    a.move("main", x=90, y=280)
    a.key("git merge feature/api crée M, un commit de merge à deux parents", color=PK, hold=1800)
    return a


def two_repos(a, ly=(90, 175, 260), sy=(90, 175, 260)):
    a.zone("zl", "Votre dépôt", 175, 190, 320, 340)
    a.zone("zs", "Serveur", 495, 190, 280, 340)


def push_fetch_pull():
    a = Anim("push-fetch-pull", "git-remotes")
    two_repos(a)
    a.commit("L1", "C1", 90, 90)
    a.commit("L2", "C2", 90, 190)
    a.edge("L2", "L1")
    a.pill("main", "main", 225, 190)
    a.edge("main", "L2", GN)
    a.pill("om", "origin/main", 240, 90, "remote")
    a.edge("om", "L1", GY)
    a.commit("S1", "C1", 440, 90)
    a.pill("sm", "main", 560, 90)
    a.edge("sm", "S1", GN)
    a.key("Votre commit C2 n'existe que sur votre machine")
    a.commit("S2", "C2", 440, 190, fro=(90, 190))
    a.edge("S2", "S1")
    a.rm("E:sm:S1", "E:om:L1")
    a.edge("sm", "S2", GN)
    a.move("sm", y=190)
    a.edge("om", "L2", GY)
    a.move("om", y=135)
    a.key("git push envoie C2, et origin/main se met à jour", color=PV)
    a.commit("S3", "C3", 440, 290, "new", fro=(440, 250))
    a.edge("S3", "S2")
    a.rm("E:sm:S2")
    a.edge("sm", "S3", GN)
    a.move("sm", y=290)
    a.key("Un collègue publie C3 sur le serveur : vous n'en savez rien", color=PK)
    a.commit("L3", "C3", 90, 290, "new", fro=(440, 290))
    a.edge("L3", "L2")
    a.rm("E:om:L2")
    a.edge("om", "L3", GY)
    a.move("om", y=255)
    a.key("git fetch télécharge C3 et déplace origin/main, main ne bouge pas", color=PV)
    a.rm("E:main:L2")
    a.edge("main", "L3", GN)
    a.move("main", y=325)
    a.key("git pull ajoute la fusion : main avance sur C3", color=GN, hold=1800)
    return a


def push_rejected():
    a = Anim("push-refuse", "git-remotes")
    two_repos(a)
    a.commit("L1", "C1", 150, 80)
    a.commit("L3", "C3", 75, 180, "new")
    a.edge("L3", "L1")
    a.pill("main", "main", 235, 180)
    a.edge("main", "L3", GN)
    a.commit("S1", "C1", 440, 80)
    a.commit("S2", "C2", 440, 180)
    a.edge("S2", "S1")
    a.pill("sm", "main", 560, 180)
    a.edge("sm", "S2", GN)
    a.key("Vous avez C3, le serveur a reçu C2 d'un collègue")
    a.pill("no", "refusé", 345, 180, "bad", fro=(200, 180))
    a.key("git push est refusé : il effacerait C2 du serveur", color=RD, hold=1900)
    a.rm("no")
    a.commit("L2", "C2", 225, 180, "c", fro=(440, 180))
    a.edge("L2", "L1")
    a.commit("M", "M", 150, 290, "new", fro=(150, 250))
    a.edge("M", "L3", PK)
    a.edge("M", "L2", PK)
    a.rm("E:main:L3")
    a.edge("main", "M", GN)
    a.move("main", x=260, y=290)
    a.key("git pull --no-rebase récupère C2 et crée un commit de merge", color=PK)
    a.move("S2", x=535)
    a.commit("S3", "C3", 395, 200, "new", fro=(75, 180))
    a.commit("S4", "M", 465, 300, "new", fro=(150, 290))
    a.edge("S3", "S1")
    a.edge("S4", "S2")
    a.edge("S4", "S3")
    a.rm("E:sm:S2")
    a.edge("sm", "S4", GN)
    a.move("sm", x=575, y=300)
    a.key("git push passe : le serveur contient les deux travaux", color=GN, hold=1800)
    return a


def reset_modes():
    a = Anim("reset-modes", "git-undo")
    a.zone("z1", "Dossier de travail", 110, 190, 190, 340)
    a.zone("z2", "Zone de préparation", 320, 190, 190, 340)
    a.zone("z3", "Dépôt local (.git)", 530, 190, 190, 340)
    a.commit("C1", "C1", 530, 90)
    a.commit("C2", "C2", 530, 200)
    a.edge("C2", "C1")
    a.pill("main", "main", 530, 305)
    a.edge("main", "C2", GN)
    a.key("Le changement est enregistré dans le commit C2")

    def undo(cap, x, col):
        a.rm("E:main:C2", "E:C2:C1", "C2")
        a.edge("main", "C1", GN)
        a.move("main", y=205)
        if x:
            a.card("change", "+ Base : OK", x, 175, fro=(530, 200))
        a.key(cap, color=col, hold=1700)

    def redo():
        a.rm("E:main:C1")
        if "change" in a.s:
            a.rm("change")
        a.commit("C2", "C2", 530, 200)
        a.edge("C2", "C1")
        a.edge("main", "C2", GN)
        a.move("main", y=305)
        a.key("On refait le commit pour essayer le mode suivant", hold=800)
    undo("git reset --soft HEAD~1 : le changement reste préparé", 320, PV)
    redo()
    undo("git reset HEAD~1 : le changement reste dans vos fichiers", 110, PV)
    redo()
    undo("git reset --hard HEAD~1 : le changement est effacé", None, RD)
    return a


def rebase():
    a = Anim("rebase", "git-rebase-cherry-pick")
    a.commit("C1", "C1", 240, 65)
    a.commit("C2", "C2", 240, 170)
    a.commit("C3", "C3", 410, 170)
    a.edge("C2", "C1")
    a.edge("C3", "C1")
    a.pill("main", "main", 110, 170)
    a.edge("main", "C2", GN)
    a.pill("db", "feature/db", 555, 170)
    a.edge("db", "C3", GN)
    a.key("feature/db est partie de C1, et main a avancé jusqu'à C2")
    a.commit("Cp", "C3'", 240, 280, "new", fro=(410, 170))
    a.edge("Cp", "C2", PK)
    a.key("git rebase main rejoue C3 au-dessus de C2 : un nouveau commit, C3'", color=PK)
    a.rm("E:db:C3", "E:C3:C1", "C3")
    a.edge("db", "Cp", GN)
    a.move("db", x=420, y=280)
    a.key("feature/db désigne C3' : l'historique est linéaire", color=GN, hold=1800)
    return a


def cherry_pick():
    a = Anim("cherry-pick", "git-rebase-cherry-pick")
    a.commit("C1", "C1", 240, 65)
    a.commit("C2", "C2", 240, 170)
    a.commit("F1", "F1", 410, 170)
    a.commit("F2", "F2", 410, 280)
    a.edge("C2", "C1")
    a.edge("F1", "C1")
    a.edge("F2", "F1")
    a.pill("main", "main", 110, 170)
    a.edge("main", "C2", GN)
    a.pill("fix", "fix/page", 540, 280)
    a.edge("fix", "F2", GN)
    a.key("fix/page contient un correctif F1, et un essai F2 à laisser")
    a.commit("Fp", "F1'", 240, 280, "new", fro=(410, 170))
    a.edge("Fp", "C2", PK)
    a.rm("E:main:C2")
    a.edge("main", "Fp", GN)
    a.move("main", y=280)
    a.key("git cherry-pick F1 copie ce seul commit sur main, avec un autre numéro", color=PK, hold=1800)
    return a


ALL = [commit_and_branch, lifecycle, switch, fast_forward, merge_commit, push_fetch_pull, push_rejected, reset_modes, rebase, cherry_pick]

if __name__ == "__main__":
    sheet = []
    for f in ALL:
        a = f()
        frames, path = a.render()
        with Image.open(path) as g:
            total = sum((g.seek(i), g.info["duration"])[1] for i in range(g.n_frames))
        print(path, len(a.keys), "étapes", round(total / 1000, 1), "s")
        n = len(a.keys)
        sheet.append(frames[len(frames) // 2])
        sheet.append(frames[-1])
    if "--sheet" in sys.argv:
        out = sys.argv[sys.argv.index("--sheet") + 1]
        tw, th = 400, 262
        im = Image.new("RGB", (tw * 4, th * 5), (200, 200, 210))
        for i, fr in enumerate(sheet):
            c = fr.resize((tw - 4, int(fr.height * (tw - 4) / fr.width)))
            im.paste(c, (i % 4 * tw + 2, i // 4 * th + 2))
        im.save(out)
