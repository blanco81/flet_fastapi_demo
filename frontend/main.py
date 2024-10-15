import flet as ft
import requests

# URL del backend
backend_url = "http://127.0.0.1:8000/items/"

def main(page: ft.Page):
    page.title = "Flet Frontend"
    
    # Campos de entrada
    name_input = ft.TextField(label="Nombre del ítem", autofocus=True)
    description_input = ft.TextField(label="Descripción del ítem")
    item_id_input = ft.TextField(label="ID del ítem", visible=False)  # Campo oculto para actualizar

    # Función para mostrar Snackbar
    def show_snackbar(message):
        snackbar = ft.SnackBar(content=ft.Text(message), action="Cerrar", duration=3000)
        page.add(snackbar)  # Agregar el snackbar a la página
        snackbar.open = True  # Abrir el snackbar
        page.update()  # Actualizar la página para mostrar el snackbar

    # Función para agregar un ítem
    def add_item(e):
        item_data = {
            "name": name_input.value,
            "description": description_input.value
        }
        response = requests.post(backend_url, json=item_data)
        
        if response.status_code == 200:
            load_items(e)  # Cargar los ítems después de agregar uno
            show_snackbar("Ítem agregado correctamente")
        else:
            show_snackbar("Error al agregar el ítem")

    # Función para cargar los ítems
    def load_items(e):
        response = requests.get(backend_url)
        if response.status_code == 200:
            items = response.json()
            items_list.controls.clear()
            for item in items:
                item_control = ft.Row(
                    controls=[
                        ft.Text(f"{item['id']}: {item['name']} - {item['description']}"),
                        ft.ElevatedButton(text="Editar", on_click=lambda e, item=item: edit_item(e, item)),
                        ft.ElevatedButton(text="Eliminar", on_click=lambda e, item=item: delete_item(e, item['id']))
                    ]
                )
                items_list.controls.append(item_control)
            page.update()
        else:
            show_snackbar("Error al cargar los ítems")

    # Función para editar un ítem
    def edit_item(e, item):
        name_input.value = item['name']
        description_input.value = item['description']
        item_id_input.value = str(item['id'])
        item_id_input.visible = True  # Mostrar campo de ID para actualizar
        page.update()

    # Función para actualizar un ítem
    def update_item(e):
        item_data = {
            "name": name_input.value,
            "description": description_input.value
        }
        item_id = item_id_input.value
        response = requests.put(f"{backend_url}{item_id}/", json=item_data)
        
        if response.status_code == 200:
            load_items(e)  # Cargar los ítems después de actualizar uno
            show_snackbar("Ítem actualizado correctamente")
        else:
            show_snackbar("Error al actualizar el ítem")

    # Función para eliminar un ítem
    def delete_item(e, item_id):
        response = requests.delete(f"{backend_url}{item_id}/")
        if response.status_code == 200:
            load_items(e)  # Cargar los ítems después de eliminar uno
            show_snackbar("Ítem eliminado correctamente")
        else:
            show_snackbar("Error al eliminar el ítem")

    items_list = ft.Column()

    # Botones
    add_button = ft.ElevatedButton(text="Agregar ítem", on_click=add_item)
    update_button = ft.ElevatedButton(text="Actualizar ítem", on_click=update_item)

    page.add(name_input, description_input, item_id_input, add_button, update_button, items_list)
    load_items(None)  # Cargar ítems al iniciar la aplicación

ft.app(target=main)
