import flet as ft

print(f"Flet version: {ft.__version__}")

def main(page: ft.Page):
    page.title = "Flet Test"
    page.add(ft.Text("Flet is working!"))

if __name__ == "__main__":
    ft.run(main)
