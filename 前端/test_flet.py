import flet as ft

def main(page: ft.Page):
    page.title = "Flet Test"
    page.padding = 20
    page.bgcolor = "#1C1C1C"
    
    page.add(
        ft.Text("Flet Test", size=24, color="white"),
        ft.ElevatedButton("Test Button", bgcolor="#0078D4", color="white"),
        ft.Dropdown(
            options=[
                ft.dropdown.Option("Option 1"),
                ft.dropdown.Option("Option 2"),
                ft.dropdown.Option("Option 3")
            ],
            value="Option 1",
            width=200,
            bgcolor="#333333",
            color="white"
        )
    )

if __name__ == "__main__":
    ft.run(main)