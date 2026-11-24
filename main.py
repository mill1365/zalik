import os
import re
import sys
import random
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window

Window.clearcolor = (0.04, 0.04, 0.04, 1)

BILETY = {
    1: "1. Відокремлені члени речення",
    2: "2. Відокремлені означення (узгоджені/неузгоджені). Розділові знаки при них",
    3: "3. Відокремлені прикладки. Розділові знаки при них",
    4: "4. Відокремлені обставини, додатки. Розділові знаки",
    5: "5. Однорідні члени речення. Види зв'язку при однорідних. Розділові знаки",
    6: "6. Складне речення, його ознаки. Види складних речень",
    7: "7. Складносурядне речення. Смислові відношення в ССР",
    8: "8. Розділові знаки в ССР",
    9: "9. Складнопідрядне речення, його ознаки. Розрізнення сполучників і сполучних слів",
    10: "10. Види СПР",
    11: "11. СПР з підрядним означальним, його ознаки",
    12: "12. СПР з підрядним з'ясувальним. Розрізнення сполучників і сполучних слів"
}

TESTS = {
    1: [
        ("1. Які члени речення можуть бути відокремленими?", ["Лише головні", "Лише другорядні", "Будь-які члени речення", "Тільки присудки та додатки"], 1),
        ("2. Якими розділовими знаками на письмі найчастіше виділяють відокремлені члени?", ["Двокрапкою", "Комами, рідше — тире", "Крапкою з комою", "Лапками"], 1),
        ("3. Коли узгоджене означення завжди відокремлюється комами?", ["Якщо стоїть перед іменником", "Якщо стосується особового займенника", "Якщо виражене присвійним прикметником", "Якщо стоїть на початку речення"], 1),
        ("4. У якому реченні узгоджене означення потрібно відокремити?", ["Степ залитий сонцем прокидався", "Залитий сонцем степ прокидався", "Ми побачили залитий сонцем степ", "У степу росла висока трава"], 0),
        ("5. Чим виражається прикладка?", ["Прикметником", "Іменником", "Дієприслівником", "Прислівником"], 1),
        ("6. У якому реченні прикладка НЕ відокремлюється комами?", ["Тарас Шевченко великий Кобзар народився на Черкащині", "Як досвідчений водій він їхав обережно", "Тарас Шевченко відомий як талановитий поет", "Вона добра душа завжди допоможе"], 2),
        ("7. Який розділовий знак ставимо перед відокремленою прикладкою в кінці речення, якщо можна вставити «а саме»?", ["Двокрапку", "Тире", "Крапку з комою", "Дужки"], 1),
        ("8. Коли одиничний дієприслівник НЕ відокремлюється?", ["Коли стоїть перед присудком", "Коли стоїть після присудка і відповідає на питання «як?»", "Коли має залежні слова", "Коли стоїть на початку речення"], 1),
        ("9. За допомогою яких слів приєднуються відокремлені додатки?", ["Незважаючи на, починаючи з", "Крім, окрім, замість, за винятком", "Тобто, або, наприклад", "Як, ніби, мов"], 1),
        ("10. Яка головна ознака складного речення?", ["Наявність однорідних членів", "Наявність двох або більше граматичних основ", "Наявність звертання", "Наявність відокремлених членів"], 1),
        ("11. На які види поділяють сполучникові складні речення?", ["Прості й ускладнені", "Складносурядні та складнопідрядні", "Односкладні та двоскладні", "Поширені та непоширені"], 1),
        ("12. Які частини у складносурядному реченні (ССР)?", ["Головна і підрядна", "Синтаксично рівноправні", "Одна залежить від іншої", "Без граматичної основи"], 1),
        ("13. Які сполучники належать до єднальних у ССР?", ["Але, проте, зате", "І (й), та (= і), ні... ні", "Або, чи, то... то", "Щоб, бо, якщо"], 1),
        ("14. Коли між частинами ССР, з'єднаними одиничним сполучником «і», кома НЕ ставиться?", ["Якщо частини дуже довгі", "Якщо є спільний другорядний член речення", "Якщо в другій частині є підмет", "Якщо перша частина двоскладна"], 1),
        ("15. Який розділовий знак ставимо в ССР при швидкій зміні подій або несподіваному наслідку?", ["Двокрапку", "Тире", "Крапку з комою", "Лапки"], 1),
        ("16. Чим сполучні слова відрізняються від сполучників підрядності?", ["Вони не мають лексичного значення", "Вони є членами речення і на них падає логічний наголос", "Вони стоять лише в головній частині", "Вони пишуться завжди через дефіс"], 1),
        ("17. На які три основні види поділяють складнопідрядні речення (СПР)?", ["Єднальні, протиставні, розділові", "Означальні, з'ясувальні, обставинні", "Називні, безособові, означено-особові", "Повні, неповні, ускладнені"], 1),
        ("18. На які питання відповідає підрядна означальна частина?", ["Кого? чого? кому? чому?", "Який? яка? яке? які?", "Де? куди? звідки?", "Чому? з якої причини?"], 1),
        ("19. Де завжди стоїть підрядна означальна частина щодо пояснюваного іменника?", ["Перед пояснюваним іменником", "Після пояснюваного іменника", "Тільки на початку речення", "Незалежно від місця іменника"], 1),
        ("20. На які питання відповідає підрядна з'ясувальна частина?", ["Який? чий?", "Питання непрямих відмінків (кого? чого? що? та ін.)", "Де? коли? як?", "Навіщо? з якою метою?"], 1)
    ],
    2: [
        ("1. У якому реченні відокремлене означення стоїть перед означуваним словом і має відтінок причини?", ["Сонце, втомлене за день, сідало", "Наляканий громом, кіт сховався під ліжко", "Він, щасливий, повернувся додому", "Квіти, политі вранці, ожили"], 1),
        ("2. Яким знаком виділяємо неузгоджене означення, виражене інфінітивом, якщо перед ним можна вставити «а саме»?", ["Комою", "Тире", "Двокрапкою", "Крапкою з комою"], 1),
        ("3. Знайдіть речення з відокремленим додатком:", ["Побачивши друзів, я зрадів", "Усі прийшли вчасно, крім Сергія", "Київ, столиця України, дуже гарний", "Степ, залитий сонцем, мовчав"], 1),
        ("4. Коли дієприслівниковий зворот НЕ відокремлюється?", ["Коли стоїть у кінці речення", "Коли є фразеологізмом (бігти не чуючи ніг)", "Коли стоїть у середині речення", "Коли стосується підмета"], 1),
        ("5. Який знак ставимо після узагальнювального слова перед однорідними членами речення?", ["Тире", "Двокрапку", "Крапку з комою", "Кому"], 1),
        ("6. У якому реченні між однорідними членами кома НЕ ставиться?", ["Садок вишневий яблуневий грушевий", "Сонце світить але не гріє", "Тато мама і бабуся прийшли на свято", "То дощ то сніг іде надворі"], 2),
        ("7. До якого типу належить речення: «Гріє сонце, вишні рясно цвітуть»?", ["Складносурядне", "Складнопідрядне", "Безсполучникове складне", "Просте ускладнене"], 2),
        ("8. Який сполучник у ССР виражає зіставні відношення (не можна замінити на «але»)?", ["Проте", "А", "Зате", "Однак"], 1),
        ("9. Визначте смислові відношення в реченні: «То сонце усміхнеться, то дощик землю полива»:", ["Єднальні", "Протиставні", "Розділові", "Зіставні"], 2),
        ("10. Чому не ставиться кома в реченні «Морозить і замітає снігом»?", ["Є спільне вставне слово", "Обидві частини є односкладними безособовими реченнями", "Це просте речення", "Сполучник повторюється"], 1),
        ("11. Коли між частинами ССР ставимо крапку з комою (;)?", ["Коли частини дуже короткі", "Коли частини значні за обсягом або вже мають усередині розділові знаки", "Коли є спільний другорядний член", "Коли речення питальне"], 1),
        ("12. Якими дужками на схемі СПР позначають головну частину?", ["Круглими ( )", "Квадратними [ ]", "Фігурними { }", "Кутовими < >"], 1),
        ("13. У складі якої частини СПР завжди знаходиться підрядний сполучник або сполучне слово?", ["Тільки в головній", "Тільки в підрядній", "Посередині між частинами", "У будь-якій частині"], 1),
        ("14. У якому реченні виділене слово «що» є сполучним словом (членом речення)?", ["Знай, що терен груш не родить", "Я бачу, що надворі вже вечір", "Я знаю те, що тобі допоможе", "Приємно, що ти зателефонував"], 2),
        ("15. Яке слово в головній частині пояснює підрядна означальна частина?", ["Дієслово-присудок", "Іменник (або займенник у значенні іменника)", "Прислівник", "Вигук"], 1),
        ("16. Яким членом речення виступають сполучні слова «де, куди, звідки, коли» в СПР з підрядним означальним?", ["Підметом", "Додатком", "Обставиною", "Присудком"], 2),
        ("17. Визначте вид підрядної частини: «Прийде час, коли наука випередить фантазію»:", ["З'ясувальна", "Означальна", "Обставинна часу", "Обставинна місця"], 1),
        ("18. Які слова в головній частині зазвичай пояснює підрядна з'ясувальна частина?", ["Іменники зі значенням предмета", "Дієслова мовлення, мислення, почуття (сказав, бачу, знаю)", "Числівники", "Прийменники"], 1),
        ("19. Для чого в головній частині СПР з підрядним з'ясувальним вживається вказівне слово «той (те, того, тому)»?", ["Для вираження часу", "Для підсилення змісту", "Для заперечення", "Для порівняння"], 1),
        ("20. Визначте вид підрядної частини: «Приснилося, що я вернувсь додому»:", ["Означальна", "З'ясувальна", "Обставинна умови", "Обставинна мети"], 1)
    ]
}

C_BLACK = (0.04, 0.04, 0.04, 1)
C_PANEL = (0.09, 0.09, 0.09, 1)
C_RED = (0.86, 0.15, 0.15, 1)
C_RED_DARK = (0.55, 0.08, 0.08, 1)
C_BLUE_TG = (0.14, 0.63, 0.87, 1)
C_GREEN = (0.13, 0.55, 0.25, 1)
C_CARD = (0.12, 0.12, 0.12, 1)


def get_app_dir():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def set_bg(widget, color, border_color=None, border_width=1):
    def _update(instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*color)
            Rectangle(pos=instance.pos, size=instance.size)
            if border_color:
                Color(*border_color)
                Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=border_width)
    widget.bind(pos=_update, size=_update)


class AutoLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = "left"
        self.valign = "top"
        self.bind(width=self._update_text_size, texture_size=self._update_height)

    def _update_text_size(self, instance, value):
        self.text_size = (max(10, value), None)

    def _update_height(self, instance, value):
        self.height = value[1]


class ExamApp(App):
    def build(self):
        self.title = "Підготовка до заліку"
        self.current_ticket = 1
        self.photo_index = 0
        self.zoom = 1.0
        self.menu_buttons = {}
        self.test_unlocked = False
        self.current_variant = 1
        self.user_answers = {}
        self.option_buttons = {}

        root = BoxLayout(orientation="vertical", padding=6, spacing=6)
        set_bg(root, C_BLACK)

        header = BoxLayout(size_hint_y=None, height=46, padding=[12, 6], spacing=10)
        set_bg(header, C_PANEL, C_RED, 1.2)
        header.add_widget(Label(
            text="[b]Зробив Касьяненко Ярослав[/b]",
            markup=True, color=(1, 1, 1, 1), font_size="15sp", halign="left", valign="middle"
        ))
        btn_tg = Button(
            text="Telegram @lilshar1k",
            size_hint=(None, 1),
            width=185,
            bold=True,
            font_size="13sp",
            background_normal="",
            background_color=C_BLUE_TG,
            color=(1, 1, 1, 1)
        )
        btn_tg.bind(on_release=lambda _: webbrowser.open("https://t.me/lilshar1k"))
        header.add_widget(btn_tg)
        root.add_widget(header)

        nav_scroll = ScrollView(size_hint_y=None, height=44, do_scroll_y=False)
        self.nav_bar = BoxLayout(size_hint_x=None, height=44, spacing=6)
        self.nav_bar.bind(minimum_width=self.nav_bar.setter("width"))

        for num in range(1, 13):
            btn = Button(
                text=f"Білет {num}",
                size_hint=(None, 1),
                width=90,
                bold=True,
                font_size="13sp",
                background_normal="",
                background_color=C_PANEL,
                color=(1, 1, 1, 1)
            )
            btn.bind(on_release=lambda inst, n=num: self.select_ticket(n))
            self.nav_bar.add_widget(btn)
            self.menu_buttons[num] = btn

        self.btn_test = Button(
            text="Перевірити знання",
            size_hint=(None, 1),
            width=165,
            bold=True,
            font_size="13sp",
            background_normal="",
            background_color=C_RED_DARK,
            color=(1, 1, 1, 1)
        )
        self.btn_test.bind(on_release=lambda _: self.open_test_tab())

        nav_scroll.add_widget(self.nav_bar)
        root.add_widget(nav_scroll)

        title_box = BoxLayout(size_hint_y=None, height=50, padding=[12, 4])
        set_bg(title_box, C_PANEL, C_RED, 1)
        self.lbl_title = Label(
            text="", bold=True, font_size="14sp", color=(1, 1, 1, 1),
            halign="center", valign="middle"
        )
        self.lbl_title.bind(width=lambda inst, w: setattr(inst, "text_size", (w, None)))
        title_box.add_widget(self.lbl_title)
        root.add_widget(title_box)

        self.main_area = BoxLayout(orientation="vertical")
        root.add_widget(self.main_area)

        # Экран просмотра фото билетов
        self.photo_wrapper = BoxLayout(orientation="vertical", padding=6, spacing=6)
        set_bg(self.photo_wrapper, C_PANEL, C_RED, 1)

        controls = BoxLayout(size_hint_y=None, height=38, spacing=8)
        btn_prev = Button(text="< Пред", bold=True, background_normal="", background_color=C_RED_DARK)
        btn_next = Button(text="След >", bold=True, background_normal="", background_color=C_RED_DARK)
        btn_z_out = Button(text="-", size_hint_x=None, width=44, bold=True, background_normal="", background_color=(0.2, 0.2, 0.2, 1))
        btn_z_in = Button(text="+", size_hint_x=None, width=44, bold=True, background_normal="", background_color=(0.2, 0.2, 0.2, 1))

        btn_prev.bind(on_release=lambda _: self.switch_photo(-1))
        btn_next.bind(on_release=lambda _: self.switch_photo(1))
        btn_z_out.bind(on_release=lambda _: self.change_zoom(-0.25))
        btn_z_in.bind(on_release=lambda _: self.change_zoom(0.25))

        self.lbl_photo_info = Label(text="0/0", font_size="13sp", bold=True, color=(0.9, 0.9, 0.9, 1))

        controls.add_widget(btn_prev)
        controls.add_widget(self.lbl_photo_info)
        controls.add_widget(btn_next)
        controls.add_widget(btn_z_out)
        controls.add_widget(btn_z_in)
        self.photo_wrapper.add_widget(controls)

        self.photo_scroll = ScrollView(do_scroll_x=True, do_scroll_y=True)
        self.photo_center_box = BoxLayout(orientation="vertical", size_hint=(None, None))
        self.img_widget = Image(size_hint=(None, None), allow_stretch=True, keep_ratio=True)
        self.photo_center_box.add_widget(self.img_widget)
        self.photo_scroll.add_widget(self.photo_center_box)
        self.photo_scroll.bind(size=lambda *_: self.render_photo())
        self.photo_wrapper.add_widget(self.photo_scroll)

        # Экран тестирования
        self.test_wrapper = BoxLayout(orientation="vertical", padding=8, spacing=8)
        set_bg(self.test_wrapper, C_PANEL, C_RED, 1)

        test_top = BoxLayout(size_hint_y=None, height=40, spacing=8)
        self.lbl_test_info = Label(text="", bold=True, font_size="14sp", color=(1, 1, 1, 1), halign="left", valign="middle")
        self.lbl_test_info.bind(width=lambda inst, w: setattr(inst, "text_size", (w, None)))
        btn_new_var = Button(
            text="Інший варіант", size_hint=(None, 1), width=140, bold=True,
            background_normal="", background_color=(0.22, 0.22, 0.22, 1)
        )
        btn_new_var.bind(on_release=lambda _: self.start_random_test())
        test_top.add_widget(self.lbl_test_info)
        test_top.add_widget(btn_new_var)
        self.test_wrapper.add_widget(test_top)

        self.test_scroll = ScrollView()
        self.test_list = BoxLayout(orientation="vertical", size_hint_y=None, padding=6, spacing=12)
        self.test_list.bind(minimum_height=self.test_list.setter("height"))
        self.test_scroll.add_widget(self.test_list)
        self.test_wrapper.add_widget(self.test_scroll)

        self.select_ticket(1)
        return root

    def find_photos(self, num):
        base_dir = get_app_dir()
        exts = (".jpg", ".jpeg", ".png", ".webp")
        matched = []

        if os.path.exists(base_dir):
            for fname in os.listdir(base_dir):
                low = fname.lower()
                if not low.endswith(exts):
                    continue
                m = re.match(rf"^{num}(?:[._-](\d+))?\.[a-z]+$", low)
                if m:
                    sub_idx = int(m.group(1)) if m.group(1) else 0
                    matched.append((sub_idx, os.path.join(base_dir, fname)))

        matched.sort(key=lambda item: item[0])
        return [path for _, path in matched]

    def select_ticket(self, num):
        self.current_ticket = num
        self.photo_index = 0
        self.zoom = 1.0

        if num == 12 and not self.test_unlocked:
            self.test_unlocked = True
            self.nav_bar.add_widget(self.btn_test)

        for n, btn in self.menu_buttons.items():
            btn.background_color = C_RED if n == num else C_PANEL
        if self.test_unlocked:
            self.btn_test.background_color = C_RED_DARK

        self.lbl_title.text = BILETY[num]

        self.main_area.clear_widgets()
        self.main_area.add_widget(self.photo_wrapper)
        self.render_photo()

    def render_photo(self):
        photos = self.find_photos(self.current_ticket)
        scroll_w = max(200, self.photo_scroll.width)
        scroll_h = max(200, self.photo_scroll.height)

        if not photos:
            self.lbl_photo_info.text = "Нет фото"
            self.img_widget.source = ""
            self.img_widget.size = (10, 10)
            self.photo_center_box.size = (scroll_w, scroll_h)
            return

        self.photo_index %= len(photos)
        self.lbl_photo_info.text = f"{self.photo_index + 1}/{len(photos)}"
        self.img_widget.source = photos[self.photo_index]
        self.img_widget.reload()

        tex_w, tex_h = self.img_widget.texture_size
        ratio = (tex_h / tex_w) if tex_w > 0 else 1.3

        target_w = (scroll_w - 20) * self.zoom
        target_h = target_w * ratio

        if self.zoom == 1.0 and target_h > (scroll_h - 10):
            target_h = scroll_h - 10
            target_w = target_h / ratio

        self.img_widget.size = (target_w, target_h)

        box_w = max(scroll_w, target_w)
        box_h = max(scroll_h, target_h)
        self.photo_center_box.size = (box_w, box_h)

        pad_x = max(0, (box_w - target_w) / 2.0)
        pad_y = max(0, (box_h - target_h) / 2.0)
        self.photo_center_box.padding = [pad_x, pad_y, pad_x, pad_y]

    def switch_photo(self, step):
        photos = self.find_photos(self.current_ticket)
        if len(photos) > 1:
            self.photo_index = (self.photo_index + step) % len(photos)
            self.zoom = 1.0
            self.render_photo()

    def change_zoom(self, delta):
        self.zoom = max(0.6, min(2.5, self.zoom + delta))
        self.render_photo()

    def open_test_tab(self):
        for btn in self.menu_buttons.values():
            btn.background_color = C_PANEL
        self.btn_test.background_color = C_RED

        self.lbl_title.text = "Перевірка знань за всіма білетами (20 запитань)"
        self.main_area.clear_widgets()
        self.main_area.add_widget(self.test_wrapper)
        self.start_random_test()

    def start_random_test(self):
        self.current_variant = random.choice([1, 2])
        self.user_answers = {}
        self.option_buttons = {}
        self.lbl_test_info.text = f"Випадковий тест — Варіант №{self.current_variant} (20 запитань)"

        self.test_list.clear_widgets()
        questions = TESTS[self.current_variant]

        for q_idx, (q_text, options, _) in enumerate(questions):
            card = BoxLayout(orientation="vertical", size_hint_y=None, padding=10, spacing=6)
            card.bind(minimum_height=card.setter("height"))
            set_bg(card, C_CARD, (0.25, 0.25, 0.25, 1), 1)

            lbl_q = AutoLabel(text=q_text, bold=True, font_size="13.5sp", color=(1, 1, 1, 1), size_hint_y=None)
            card.add_widget(lbl_q)

            self.option_buttons[q_idx] = []
            for o_idx, opt_text in enumerate(options):
                btn_opt = Button(
                    text=f"  {['А', 'Б', 'В', 'Г'][o_idx]}) {opt_text}",
                    size_hint_y=None,
                    height=38,
                    font_size="13sp",
                    halign="left",
                    valign="middle",
                    background_normal="",
                    background_color=(0.18, 0.18, 0.18, 1),
                    color=(0.95, 0.95, 0.95, 1)
                )
                btn_opt.bind(width=lambda inst, w: setattr(inst, "text_size", (w - 16, None)))
                btn_opt.bind(on_release=lambda inst, qi=q_idx, oi=o_idx: self.choose_answer(qi, oi))
                card.add_widget(btn_opt)
                self.option_buttons[q_idx].append(btn_opt)

            self.test_list.add_widget(card)

        self.lbl_result = AutoLabel(
            text="", bold=True, font_size="15sp", color=(1, 1, 1, 1), size_hint_y=None
        )
        self.test_list.add_widget(self.lbl_result)

        btn_finish = Button(
            text="Завершити тест і перевірити відповіді",
            size_hint_y=None,
            height=46,
            bold=True,
            font_size="14sp",
            background_normal="",
            background_color=C_RED
        )
        btn_finish.bind(on_release=lambda _: self.finish_test())
        self.test_list.add_widget(btn_finish)
        self.test_scroll.scroll_y = 1.0

    def choose_answer(self, q_idx, o_idx):
        self.user_answers[q_idx] = o_idx
        for idx, btn in enumerate(self.option_buttons[q_idx]):
            btn.background_color = C_RED if idx == o_idx else (0.18, 0.18, 0.18, 1)

    def finish_test(self):
        questions = TESTS[self.current_variant]
        score = 0
        for q_idx, (_, _, correct_idx) in enumerate(questions):
            chosen = self.user_answers.get(q_idx, -1)
            if chosen == correct_idx:
                score += 1
            for o_idx, btn in enumerate(self.option_buttons[q_idx]):
                if o_idx == correct_idx:
                    btn.background_color = C_GREEN
                elif o_idx == chosen and chosen != correct_idx:
                    btn.background_color = C_RED_DARK
                else:
                    btn.background_color = (0.15, 0.15, 0.15, 1)

        self.lbl_result.text = f"Результат (Варіант №{self.current_variant}): {score} з {len(questions)} правильних відповідей!"


if __name__ == "__main__":
    ExamApp().run()
