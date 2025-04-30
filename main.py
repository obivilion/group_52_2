import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True

    shopping_list = ft.Column(spacing=10)
    bought_count = ft.Text("SHOP")
    filter_type = "all"

    def update_bought_count():
        count = sum(
            1 for item in shopping_list.controls
            if isinstance(item.controls[0], ft.Checkbox) and item.controls[0].value
        )
        bought_count.value = f"Куплено: {count} товаров"
        page.update()

    def load_items():
        shopping_list.controls.clear()
        db_tasks = main_db.get_tasks(filter_type)
        for task_id, task_text, quantity, completed in db_tasks:
            row = create_item_row(task_id, task_text, quantity, bool(completed))
            shopping_list.controls.append(row)
        update_bought_count()
        page.update()

    def on_checkbox_change(e, task_id):
        checked = e.control.value
        main_db.update_task_db(task_id, completed=int(checked))
        update_bought_count()
        load_items()

    def on_delete(task_id, row):
        main_db.delete_task_db(task_id)
        shopping_list.controls.remove(row)
        page.update()
        update_bought_count()

    def create_item_row(task_id, task_text, quantity, completed):
        checkbox = ft.Checkbox(
            value=completed,
            on_change=lambda e: on_checkbox_change(e, task_id)
        )

        quantity_text = ft.Text(f" x{quantity}")

        delete_btn = ft.IconButton(
            icon=ft.icons.DELETE,
            icon_color=ft.colors.RED_400,
            on_click=lambda e: on_delete(task_id, row)
        )

        row = ft.Row(
            [checkbox, ft.Text(task_text), quantity_text, delete_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        return row

    def add_item(e):
        name = item_input.value.strip()
        quantity = quantity_input.value.strip() or "1"

        if name:
            task_id = main_db.add_task_db(name, quantity)
            row = create_item_row(task_id, name, quantity, False)
            shopping_list.controls.append(row)
            item_input.value = ""
            quantity_input.value = ""
            page.update()
            update_bought_count()

    def set_filter(value):
        nonlocal filter_type
        filter_type = value
        load_items()

    item_input = ft.TextField(hint_text="Введите название товара", expand=True)
    quantity_input = ft.TextField(hint_text="Количество", width=100)
    add_button = ft.ElevatedButton("Добавить", icon=ft.icons.ADD, on_click=add_item)

    filter_buttons = ft.Row(
        [
            ft.ElevatedButton("Все", on_click=lambda e: set_filter("all")),
            ft.ElevatedButton("Купленные", on_click=lambda e: set_filter("completed")),
            ft.ElevatedButton("Корзина", on_click=lambda e: set_filter("uncompleted")),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(
        ft.Column(
            [
                ft.Row([item_input, quantity_input, add_button]),
                filter_buttons,
                bought_count,
                shopping_list,
            ],
            spacing=20,
            expand=True,
        )
    )

    load_items()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
