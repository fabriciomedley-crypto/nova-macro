import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QCheckBox, QComboBox, QFrame,
    QGridLayout, QButtonGroup, QRadioButton, QStackedWidget, QSizePolicy,
    QSpacerItem, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPoint, QSize
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QLinearGradient, QPainter, QPen,
    QBrush, QFontDatabase, QIcon, QPixmap, QPainterPath, QRadialGradient
)

# ─── CONFIG FILE ───────────────────────────────────────────────────────────────
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULT_CONFIG = {
    "weapon": 0,
    "sight": 0,
    "module": 0,
    "position": 0,
    "sensitivity": 50.0,
    "vertical_sensitivity": 1.0,
    "aim_sensitivity": 50.0,
    "ads_sensitivity": 50.0,
    "multiplier_x2": 50.0,
    "multiplier_x3": 50.0,
    "sensitivity_diff_scope": False,
    "bias_x": 0.0,
    "bias_y": 0.0,
    "control_x": 100.0,
    "control_y": 100.0,
    "randomizer": 0.0,
    "zoom_hack": 200,
    "color_inversion": False,
    "sound_switching": True,
    "show_crosshair": False,
    "crosshair_type": "Dot",
    "overlay": False,
    "auto_click": False,
    "auto_fire_delay": 6,
    "language": "EN",
    "sound": False,
    "autodetect_mode": "press",
    "autodetect_weapons": True,
    "autodetect_modules": True,
    "gaming_whdown": "WHDOWN",
    "gaming_c": "C",
    "gaming_b": "B",
    "gaming_z": "Z",
    "gaming_mr": "MR",
    "gaming_v": "V",
    "gaming_1": "1",
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                cfg = DEFAULT_CONFIG.copy()
                cfg.update(data)
                return cfg
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except:
        pass

# ─── STYLE CONSTANTS ───────────────────────────────────────────────────────────
BG_DARK      = "#0a0e1a"
BG_PANEL     = "#0d1525"
BG_CARD      = "#111827"
BG_CARD2     = "#0f1c2e"
BORDER_COLOR = "#1a2744"
ACCENT_BLUE  = "#1a6bff"
ACCENT_GREEN = "#00d084"
ACCENT_ORANGE= "#ff6b35"
TEXT_PRIMARY = "#e8eaf0"
TEXT_SECONDARY = "#6b7fa3"
TEXT_DIM     = "#3a4a6a"
HOVER_BG     = "#162035"
SELECTED_BG  = "#0d2448"

WEAPONS = [
    "AKM", "Beryl M762", "G36C", "M416", "M16A4", "SCAR-L",
    "Mk47 Mutant", "QBZ", "AUG", "Groza", "ACE32", "K2"
]
WEAPON_KEYS = [
    "ALT+1","ALT+2","ALT+3","ALT+4","ALT+5","ALT+6",
    "ALT+7","ALT+8","ALT+9","ALT+0","ALT+-","ALT++"
]
SIGHTS = ["x1 (w/cut)", "x2", "x3", "x4", "x6"]
SIGHT_KEYS = ["NUM_1+NUM_2","NUM_1+NUM_3","NUM_1+NUM_4","NUM_1+NUM_5","NUM_1+NUM_6"]
MODULES = ["Cheek Pad", "Stock for Micro UZI", "Angled Foregrip", "Half Grip", "Thumb Grip"]
MODULE_KEYS = ["NUM_1+Q","NUM_1+W","NUM_1+E","NUM_1+R","NUM_1+T"]
POSITIONS = ["Stand up", "Sit down", "Lie down"]
POSITION_KEYS = ["ALT+F1","ALT+F2","ALT+F2"]
MISC_ITEMS = [
    ("NUM_0","Any off"),("IN0","Hide menu"),("F4","Show Crosshair"),
    ("M3","Zoom Hack"),("NUM_*","Anti-AFK")
]

# ─── CUSTOM WIDGETS ────────────────────────────────────────────────────────────

class StarLogo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 40)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        # Draw star
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(TEXT_PRIMARY)))
        cx, cy, r = 12, 20, 10
        import math
        pts = []
        for i in range(10):
            angle = math.pi * i / 5 - math.pi / 2
            rad = r if i % 2 == 0 else r * 0.45
            pts.append(QPoint(int(cx + rad * math.cos(angle)), int(cy + rad * math.sin(angle))))
        from PyQt5.QtGui import QPolygon
        p.drawPolygon(QPolygon(pts))
        # Draw text
        p.setPen(QPen(QColor(TEXT_PRIMARY)))
        f = QFont("Arial", 11, QFont.Bold)
        f.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        p.setFont(f)
        p.drawText(26, 14, "NOVA")
        f2 = QFont("Arial", 7)
        f2.setLetterSpacing(QFont.AbsoluteSpacing, 3)
        p.setFont(f2)
        p.setPen(QPen(QColor(TEXT_SECONDARY)))
        p.drawText(28, 26, "MACRO")


class NavButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self._active = False
        self.setFont(QFont("Arial", 10))
        self.setFixedHeight(32)
        self.setMinimumWidth(80)
        self._update_style()

    def setActive(self, active):
        self._active = active
        self.setChecked(active)
        self._update_style()

    def _update_style(self):
        if self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {ACCENT_BLUE};
                    border: none;
                    border-bottom: 2px solid {ACCENT_BLUE};
                    padding: 4px 16px;
                    font-weight: 600;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {TEXT_SECONDARY};
                    border: none;
                    border-bottom: 2px solid transparent;
                    padding: 4px 16px;
                }}
                QPushButton:hover {{
                    color: {TEXT_PRIMARY};
                    border-bottom: 2px solid {TEXT_DIM};
                }}
            """)


class KeyButton(QPushButton):
    def __init__(self, key_text, label_text, parent=None):
        super().__init__(parent)
        self.key_text = key_text
        self.label_text = label_text
        self._selected = False
        self.setFixedHeight(28)
        self.setCursor(Qt.PointingHandCursor)
        self._update_style()

    def setSelected(self, sel):
        self._selected = sel
        self._update_style()

    def _update_style(self):
        if self._selected:
            bg = SELECTED_BG
            border = ACCENT_BLUE
            key_color = ACCENT_BLUE
            label_color = ACCENT_GREEN
        else:
            bg = BG_CARD2
            border = BORDER_COLOR
            key_color = TEXT_SECONDARY
            label_color = TEXT_PRIMARY

        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 0px 8px;
                text-align: left;
            }}
            QPushButton:hover {{
                background: {HOVER_BG};
                border: 1px solid {ACCENT_BLUE};
            }}
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.rect()

        # Key text (left, dim)
        key_color = QColor(ACCENT_BLUE if self._selected else TEXT_DIM)
        p.setPen(QPen(key_color))
        f = QFont("Consolas", 7, QFont.Bold)
        p.setFont(f)
        p.drawText(8, 0, 70, r.height(), Qt.AlignVCenter | Qt.AlignLeft, self.key_text)

        # Label text (right)
        lbl_color = QColor(ACCENT_GREEN if self._selected else TEXT_PRIMARY)
        p.setPen(QPen(lbl_color))
        f2 = QFont("Arial", 9, QFont.Bold if self._selected else QFont.Normal)
        p.setFont(f2)
        p.drawText(76, 0, r.width() - 84, r.height(), Qt.AlignVCenter | Qt.AlignLeft, self.label_text)


class SectionCard(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {BG_CARD};
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(12, 8, 12, 12)
        self._layout.setSpacing(6)

        if title:
            lbl = QLabel(title)
            lbl.setFont(QFont("Arial", 10, QFont.Bold))
            lbl.setStyleSheet(f"color: {TEXT_PRIMARY}; background: transparent; border: none;")
            lbl.setAlignment(Qt.AlignCenter)
            self._layout.addWidget(lbl)

    def inner_layout(self):
        return self._layout


class SliderRow(QWidget):
    def __init__(self, label, value, min_val=0, max_val=100, decimals=1, parent=None):
        super().__init__(parent)
        self.decimals = decimals
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        lbl = QLabel(label)
        lbl.setFont(QFont("Arial", 8))
        lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; background: transparent; border: none;")
        lbl.setFixedWidth(150)
        layout.addWidget(lbl)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(int(min_val * 100))
        self.slider.setMaximum(int(max_val * 100))
        self.slider.setValue(int(value * 100))
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 4px;
                background: {BORDER_COLOR};
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                width: 12px; height: 12px;
                background: {ACCENT_BLUE};
                border-radius: 6px;
                margin: -4px 0;
            }}
            QSlider::sub-page:horizontal {{
                background: {ACCENT_BLUE};
                border-radius: 2px;
            }}
        """)
        layout.addWidget(self.slider, 1)

        self.val_lbl = QLabel(f"{value:.{decimals}f}")
        self.val_lbl.setFont(QFont("Consolas", 8))
        self.val_lbl.setStyleSheet(f"color: {ACCENT_BLUE}; background: transparent; border: none;")
        self.val_lbl.setFixedWidth(50)
        layout.addWidget(self.val_lbl)

        self.slider.valueChanged.connect(self._on_change)

    def _on_change(self, v):
        real = v / 100.0
        self.val_lbl.setText(f"{real:.{self.decimals}f}")

    def value(self):
        return self.slider.value() / 100.0

    def setValue(self, v):
        self.slider.setValue(int(v * 100))


class StyledCheckBox(QCheckBox):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 8))
        self.setStyleSheet(f"""
            QCheckBox {{
                color: {TEXT_SECONDARY};
                background: transparent;
                spacing: 6px;
            }}
            QCheckBox::indicator {{
                width: 14px; height: 14px;
                border: 1px solid {BORDER_COLOR};
                border-radius: 3px;
                background: {BG_CARD2};
            }}
            QCheckBox::indicator:checked {{
                background: {ACCENT_BLUE};
                border: 1px solid {ACCENT_BLUE};
            }}
            QCheckBox:hover {{ color: {TEXT_PRIMARY}; }}
        """)


class StyledCombo(QComboBox):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        for i in items:
            self.addItem(i)
        self.setFont(QFont("Arial", 8))
        self.setStyleSheet(f"""
            QComboBox {{
                background: {BG_CARD2};
                color: {TEXT_PRIMARY};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 3px 8px;
                min-width: 80px;
            }}
            QComboBox:hover {{ border: 1px solid {ACCENT_BLUE}; }}
            QComboBox QAbstractItemView {{
                background: {BG_PANEL};
                color: {TEXT_PRIMARY};
                selection-background-color: {SELECTED_BG};
                border: 1px solid {BORDER_COLOR};
            }}
        """)


# ─── TABS ──────────────────────────────────────────────────────────────────────

class KeysTab(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.weapon_btns = []
        self.sight_btns = []
        self.module_btns = []
        self.position_btns = []
        self._build()

    def _build(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(8, 8, 8, 8)
        main.setSpacing(8)

        # ── Column 1: Weapon ──
        weapon_card = SectionCard("Weapon")
        for i, (key, name) in enumerate(zip(WEAPON_KEYS, WEAPONS)):
            btn = KeyButton(key, name)
            btn.setSelected(i == self.config.get("weapon", 0))
            idx = i
            btn.clicked.connect(lambda _, x=idx: self._select_weapon(x))
            weapon_card.inner_layout().addWidget(btn)
            self.weapon_btns.append(btn)
        main.addWidget(weapon_card, 3)

        # ── Column 2+3: Sight, Modules, Misc ──
        col2 = QVBoxLayout()
        col2.setSpacing(8)

        sight_card = SectionCard("Sight")
        for i, (key, name) in enumerate(zip(SIGHT_KEYS, SIGHTS)):
            btn = KeyButton(key, name)
            btn.setSelected(i == self.config.get("sight", 0))
            idx = i
            btn.clicked.connect(lambda _, x=idx: self._select_sight(x))
            sight_card.inner_layout().addWidget(btn)
            self.sight_btns.append(btn)
        col2.addWidget(sight_card)

        mod_card = SectionCard("Modules")
        for i, (key, name) in enumerate(zip(MODULE_KEYS, MODULES)):
            btn = KeyButton(key, name)
            btn.setSelected(i == self.config.get("module", 0))
            idx = i
            btn.clicked.connect(lambda _, x=idx: self._select_module(x))
            mod_card.inner_layout().addWidget(btn)
            self.module_btns.append(btn)
        col2.addWidget(mod_card)
        col2.addStretch()
        main.addLayout(col2, 2)

        # ── Column 3: Misc + Position ──
        col3 = QVBoxLayout()
        col3.setSpacing(8)

        misc_card = SectionCard("Misc")
        for key, name in MISC_ITEMS:
            btn = KeyButton(key, name)
            misc_card.inner_layout().addWidget(btn)
        col3.addWidget(misc_card)

        pos_card = SectionCard("Position")
        pos_colors = [ACCENT_GREEN, TEXT_PRIMARY, TEXT_PRIMARY]
        for i, (key, name) in enumerate(zip(POSITION_KEYS, POSITIONS)):
            btn = KeyButton(key, name)
            btn.setSelected(i == self.config.get("position", 0))
            idx = i
            btn.clicked.connect(lambda _, x=idx: self._select_position(x))
            pos_card.inner_layout().addWidget(btn)
            self.position_btns.append(btn)
        col3.addWidget(pos_card)
        col3.addStretch()
        main.addLayout(col3, 2)

    def _select_weapon(self, idx):
        self.config["weapon"] = idx
        for i, b in enumerate(self.weapon_btns):
            b.setSelected(i == idx)

    def _select_sight(self, idx):
        self.config["sight"] = idx
        for i, b in enumerate(self.sight_btns):
            b.setSelected(i == idx)

    def _select_module(self, idx):
        self.config["module"] = idx
        for i, b in enumerate(self.module_btns):
            b.setSelected(i == idx)

    def _select_position(self, idx):
        self.config["position"] = idx
        for i, b in enumerate(self.position_btns):
            b.setSelected(i == idx)


class SettingsTab(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self._build()

    def _build(self):
        main = QGridLayout(self)
        main.setContentsMargins(8, 8, 8, 8)
        main.setSpacing(8)

        # ── Recoil Control ──
        rc = SectionCard("Recoil control")
        rc_layout = rc.inner_layout()

        bias_row = QHBoxLayout()
        bias_row.setSpacing(8)
        for label, key in [("Bias X:", "bias_x"), ("Bias Y:", "bias_y")]:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setFont(QFont("Arial", 8))
            lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; background: transparent; border: none;")
            row.addWidget(lbl)
            sl = SliderRow("", self.config.get(key, 0.0), -10, 10, 1)
            row.addWidget(sl)
            bias_row.addLayout(row)
        rc_layout.addLayout(bias_row)

        rc_layout.addWidget(SliderRow("Control X: 100,0 %", self.config.get("control_x", 100.0), 0, 200, 1))
        rc_layout.addWidget(SliderRow("Control Y: 100,0 %", self.config.get("control_y", 100.0), 0, 200, 1))
        rc_layout.addWidget(SliderRow("Randomizer:", self.config.get("randomizer", 0.0), 0, 100, 1))
        main.addWidget(rc, 0, 0)

        # ── Autodetect ──
        ad = SectionCard("Autodetect")
        ad_layout = ad.inner_layout()
        ad_layout.setSpacing(4)

        mode_row = QHBoxLayout()
        self.rb_press = QRadioButton("By press slots")
        self.rb_realtime = QRadioButton("In real time")
        for rb in [self.rb_press, self.rb_realtime]:
            rb.setFont(QFont("Arial", 8))
            rb.setStyleSheet(f"""
                QRadioButton {{ color: {TEXT_SECONDARY}; background: transparent; spacing: 5px; }}
                QRadioButton::indicator {{ width: 12px; height: 12px; border-radius: 6px;
                    border: 1px solid {BORDER_COLOR}; background: {BG_CARD2}; }}
                QRadioButton::indicator:checked {{ background: {ACCENT_BLUE}; border: 1px solid {ACCENT_BLUE}; }}
            """)
            mode_row.addWidget(rb)
        if self.config.get("autodetect_mode") == "press":
            self.rb_press.setChecked(True)
        else:
            self.rb_realtime.setChecked(True)
        ad_layout.addLayout(mode_row)

        check_row = QHBoxLayout()
        self.cb_weapons = StyledCheckBox("Weapons")
        self.cb_weapons.setChecked(self.config.get("autodetect_weapons", True))
        self.cb_modules2 = StyledCheckBox("Modules")
        self.cb_modules2.setChecked(self.config.get("autodetect_modules", True))
        check_row.addWidget(self.cb_weapons)
        check_row.addWidget(self.cb_modules2)
        ad_layout.addLayout(check_row)

        res_lbl = QLabel("Current resolution: 2560x1440")
        res_lbl.setFont(QFont("Arial", 8))
        res_lbl.setStyleSheet(f"color: {TEXT_DIM}; background: transparent; border: none;")
        ad_layout.addWidget(res_lbl)
        ad_layout.addStretch()
        main.addWidget(ad, 0, 1)

        # ── Sensitivity ──
        sens = SectionCard("Sensitivity")
        sl = sens.inner_layout()
        sl.addWidget(SliderRow("Sensitivity: 50,00", self.config.get("sensitivity", 50.0), 1, 100, 2))
        sl.addWidget(SliderRow("Vertical sensitivity: 1,00", self.config.get("vertical_sensitivity", 1.0), 0.1, 5.0, 2))
        sl.addWidget(SliderRow("Aim sensitivity: 50,00", self.config.get("aim_sensitivity", 50.0), 1, 100, 2))
        sl.addWidget(SliderRow("ADS sensitivity: 50,00", self.config.get("ads_sensitivity", 50.0), 1, 100, 2))
        sl.addWidget(SliderRow("Multiplier x2: 50,00", self.config.get("multiplier_x2", 50.0), 1, 100, 2))
        cb_diff = StyledCheckBox("Sensitivity for different scope")
        cb_diff.setChecked(self.config.get("sensitivity_diff_scope", False))
        sl.addWidget(cb_diff)
        sl.addWidget(SliderRow("Multiplier x3: 50,00", self.config.get("multiplier_x3", 50.0), 1, 100, 2))
        main.addWidget(sens, 1, 0)

        # ── Gaming Settings ──
        gs = SectionCard("Gaming settings")
        gl = gs.inner_layout()
        gaming = [
            ("gaming_whdown", "Switch weapon"),
            ("gaming_c",      "Sit down"),
            ("gaming_b",      "Firing mode"),
            ("gaming_z",      "Lie down"),
            ("gaming_mr",     "Aim"),
            ("gaming_v",      "Change view"),
            ("gaming_1",      "Slot 1"),
        ]
        defaults = ["WHDOWN","C","B","Z","MR","V","1"]
        for i, (key, desc) in enumerate(gaming):
            row = QHBoxLayout()
            row.setSpacing(6)
            key_lbl = QLabel(self.config.get(key, defaults[i]))
            key_lbl.setFont(QFont("Consolas", 9, QFont.Bold))
            key_lbl.setStyleSheet(f"""
                color: {TEXT_PRIMARY};
                background: {BG_CARD2};
                border: 1px solid {BORDER_COLOR};
                border-radius: 3px;
                padding: 2px 6px;
            """)
            key_lbl.setFixedWidth(70)
            desc_lbl = QLabel(desc)
            desc_lbl.setFont(QFont("Arial", 8))
            desc_lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; background: transparent; border: none;")
            row.addWidget(key_lbl)
            row.addWidget(desc_lbl)
            row.addStretch()
            gl.addLayout(row)
        gl.addStretch()
        main.addWidget(gs, 1, 1)

        main.setRowStretch(0, 1)
        main.setRowStretch(1, 1)
        main.setColumnStretch(0, 1)
        main.setColumnStretch(1, 1)


class MiscTab(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self._build()

    def _build(self):
        main = QGridLayout(self)
        main.setContentsMargins(8, 8, 8, 8)
        main.setSpacing(8)

        # Zoom Hack
        zh = SectionCard("Zoom Hack")
        zl = zh.inner_layout()
        zl.addWidget(SliderRow("", self.config.get("zoom_hack", 200) / 10.0, 10, 80, 0))
        cb_row = QHBoxLayout()
        cb_color = StyledCheckBox("Color inversion")
        cb_color.setChecked(self.config.get("color_inversion", False))
        cb_sound = StyledCheckBox("Sound when switching")
        cb_sound.setChecked(self.config.get("sound_switching", True))
        cb_sound.setStyleSheet(cb_sound.styleSheet().replace(TEXT_SECONDARY, ACCENT_BLUE))
        cb_row.addWidget(cb_color)
        cb_row.addWidget(cb_sound)
        zl.addLayout(cb_row)
        main.addWidget(zh, 0, 0)

        # Crosshair
        ch = SectionCard("Crosshair")
        cl = ch.inner_layout()
        combo = StyledCombo(["Dot", "Cross", "Circle", "T-Shape"])
        combo.setCurrentText(self.config.get("crosshair_type", "Dot"))
        cl.addWidget(combo)
        cb_show = StyledCheckBox("Show Crosshair")
        cb_show.setChecked(self.config.get("show_crosshair", False))
        cl.addWidget(cb_show)
        cl.addStretch()
        main.addWidget(ch, 0, 1)

        # Overlay
        ov = SectionCard("Overlay")
        ol = ov.inner_layout()
        cb_ov = StyledCheckBox("Display overlay while hiding the menu")
        cb_ov.setChecked(self.config.get("overlay", False))
        ol.addWidget(cb_ov)
        ol.addStretch()
        main.addWidget(ov, 1, 0)

        # Reset by default
        rb = SectionCard("Reset by default")
        rl = rb.inner_layout()
        reset_btn = QPushButton("Reset")
        reset_btn.setFont(QFont("Arial", 9))
        reset_btn.setFixedSize(80, 28)
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background: {BG_CARD2};
                color: {TEXT_PRIMARY};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background: {HOVER_BG};
                border: 1px solid {ACCENT_BLUE};
                color: {ACCENT_BLUE};
            }}
        """)
        rl.addWidget(reset_btn)
        rl.addStretch()
        main.addWidget(rb, 1, 1)

        # Auto-Fire
        af = SectionCard("Auto-Fire")
        al = af.inner_layout()
        al.addWidget(SliderRow("Delay:", self.config.get("auto_fire_delay", 6) / 10.0, 0.1, 5.0, 1))
        cb_ac = StyledCheckBox("Auto-click")
        cb_ac.setChecked(self.config.get("auto_click", False))
        al.addWidget(cb_ac)
        main.addWidget(af, 2, 0, 1, 2)

        main.setRowStretch(3, 1)


class InfoTab(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self._build()

    def _build(self):
        main = QGridLayout(self)
        main.setContentsMargins(8, 8, 8, 8)
        main.setSpacing(8)

        # Language
        lang = SectionCard("Language")
        ll = lang.inner_layout()
        lang_row = QHBoxLayout()
        self.rb_en = QRadioButton("EN")
        self.rb_ru = QRadioButton("RU")
        for rb in [self.rb_en, self.rb_ru]:
            rb.setFont(QFont("Arial", 9))
            rb.setStyleSheet(f"""
                QRadioButton {{ color: {TEXT_SECONDARY}; background: transparent; spacing: 5px; }}
                QRadioButton::indicator {{ width: 14px; height: 14px; border-radius: 7px;
                    border: 1px solid {BORDER_COLOR}; background: {BG_CARD2}; }}
                QRadioButton::indicator:checked {{ background: {ACCENT_BLUE}; border: 1px solid {ACCENT_BLUE}; }}
            """)
            lang_row.addWidget(rb)
        if self.config.get("language", "EN") == "EN":
            self.rb_en.setChecked(True)
        else:
            self.rb_ru.setChecked(True)
        ll.addLayout(lang_row)
        ll.addStretch()
        main.addWidget(lang, 0, 0)

        # Contacts
        contacts = SectionCard("Contacts")
        cl = contacts.inner_layout()
        contact_lbl = QLabel(
            "If you need help setting up or encounter other problems,\n"
            "you can contact technical support."
        )
        contact_lbl.setFont(QFont("Arial", 8))
        contact_lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; background: transparent; border: none;")
        contact_lbl.setWordWrap(True)
        cl.addWidget(contact_lbl)
        cl.addStretch()
        main.addWidget(contacts, 0, 1)

        # Sound
        sound = SectionCard("Sound")
        sl = sound.inner_layout()
        self.rb_sound_on = QRadioButton("On all sound")
        self.rb_sound_off = QRadioButton("Off all sound")
        for rb in [self.rb_sound_on, self.rb_sound_off]:
            rb.setFont(QFont("Arial", 9))
            rb.setStyleSheet(f"""
                QRadioButton {{ color: {TEXT_SECONDARY}; background: transparent; spacing: 5px; }}
                QRadioButton::indicator {{ width: 14px; height: 14px; border-radius: 7px;
                    border: 1px solid {BORDER_COLOR}; background: {BG_CARD2}; }}
                QRadioButton::indicator:checked {{ background: {ACCENT_BLUE}; border: 1px solid {ACCENT_BLUE}; }}
            """)
            sl.addWidget(rb)
        if self.config.get("sound", False):
            self.rb_sound_on.setChecked(True)
        else:
            self.rb_sound_off.setChecked(True)
        sl.addStretch()
        main.addWidget(sound, 1, 0)

        # Information
        info = SectionCard("Information")
        il = info.inner_layout()
        for label, value in [("Active time:", "0"), ("Your ID:", ""), ("Software version:", "1.0")]:
            row = QHBoxLayout()
            key_lbl = QLabel(label)
            key_lbl.setFont(QFont("Arial", 8))
            key_lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; background: transparent; border: none;")
            val_lbl = QLabel(value)
            val_lbl.setFont(QFont("Arial", 8, QFont.Bold))
            color = ACCENT_GREEN if label == "Active time:" else TEXT_PRIMARY
            val_lbl.setStyleSheet(f"color: {color}; background: transparent; border: none;")
            row.addWidget(key_lbl)
            row.addWidget(val_lbl)
            row.addStretch()
            il.addLayout(row)
        il.addStretch()
        main.addWidget(info, 1, 1)

        main.setRowStretch(2, 1)


# ─── MAIN WINDOW ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.setWindowTitle("NOVA MACRO")
        self.setFixedSize(680, 460)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._drag_pos = None
        self._build_ui()
        self._switch_tab(0)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        # Outer glow
        glow = QRadialGradient(rect.width() / 2, rect.height() / 2, max(rect.width(), rect.height()) / 1.5)
        glow.setColorAt(0, QColor(26, 107, 255, 15))
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(glow))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(rect, 12, 12)
        # Main background
        p.setBrush(QBrush(QColor(BG_DARK)))
        p.setPen(QPen(QColor(BORDER_COLOR), 1))
        p.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 10, 10)

    def _build_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title bar ──
        title_bar = QWidget()
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet("background: transparent;")
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(16, 0, 16, 0)
        tb_layout.setSpacing(0)

        self.logo = StarLogo()
        tb_layout.addWidget(self.logo)
        tb_layout.addSpacing(20)

        # Nav buttons
        self.nav_buttons = []
        for i, tab in enumerate(["Keys", "Settings", "Misc", "Info"]):
            btn = NavButton(tab)
            btn.clicked.connect(lambda _, x=i: self._switch_tab(x))
            tb_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        tb_layout.addStretch()

        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_DIM};
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: #ff4444;
            }}
        """)
        close_btn.clicked.connect(self._on_close)
        tb_layout.addWidget(close_btn)
        root.addWidget(title_bar)

        # Separator line
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background: {BORDER_COLOR};")
        root.addWidget(sep)

        # ── Arrow buttons + stacked content ──
        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(0)

        # Left arrow
        self.left_arrow = QPushButton("❮")
        self.left_arrow.setFixedWidth(28)
        self.left_arrow.setCursor(Qt.PointingHandCursor)
        self.left_arrow.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_DIM};
                border: none;
                font-size: 16px;
            }}
            QPushButton:hover {{ color: {ACCENT_BLUE}; }}
        """)
        self.left_arrow.clicked.connect(lambda: self._switch_tab((self._current_tab - 1) % 4))
        content_row.addWidget(self.left_arrow)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")

        self.tabs = [
            KeysTab(self.config),
            SettingsTab(self.config),
            MiscTab(self.config),
            InfoTab(self.config),
        ]
        for tab in self.tabs:
            self.stack.addWidget(tab)
        content_row.addWidget(self.stack, 1)

        # Right arrow
        self.right_arrow = QPushButton("❯")
        self.right_arrow.setFixedWidth(28)
        self.right_arrow.setCursor(Qt.PointingHandCursor)
        self.right_arrow.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_DIM};
                border: none;
                font-size: 16px;
            }}
            QPushButton:hover {{ color: {ACCENT_BLUE}; }}
        """)
        self.right_arrow.clicked.connect(lambda: self._switch_tab((self._current_tab + 1) % 4))
        content_row.addWidget(self.right_arrow)
        root.addLayout(content_row, 1)

        # ── Dot indicators ──
        dots_row = QHBoxLayout()
        dots_row.setContentsMargins(0, 4, 0, 8)
        self.dots = []
        for i in range(4):
            dot = QPushButton()
            dot.setFixedSize(10, 10)
            dot.setCursor(Qt.PointingHandCursor)
            idx = i
            dot.clicked.connect(lambda _, x=idx: self._switch_tab(x))
            self.dots.append(dot)
            dots_row.addWidget(dot)
        root.addLayout(dots_row)
        dots_row.setAlignment(Qt.AlignCenter)
        self._current_tab = 0

    def _switch_tab(self, idx):
        self._current_tab = idx
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_buttons):
            btn.setActive(i == idx)
        for i, dot in enumerate(self.dots):
            if i == idx:
                dot.setStyleSheet(f"""
                    QPushButton {{ background: {ACCENT_BLUE}; border-radius: 5px; border: none; }}
                """)
            else:
                dot.setStyleSheet(f"""
                    QPushButton {{ background: {BORDER_COLOR}; border-radius: 5px; border: none; }}
                    QPushButton:hover {{ background: {TEXT_DIM}; }}
                """)

    def _on_close(self):
        save_config(self.config)
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 50:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


# ─── ENTRY POINT ───────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG_DARK))
    palette.setColor(QPalette.WindowText, QColor(TEXT_PRIMARY))
    app.setPalette(palette)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
