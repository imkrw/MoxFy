from flet import *
import hashlib
import base64
import os
import random
import string
import socket


def is_internet_available():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False


def hash_password(password):
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    encoded_salt = base64.b64encode(salt).decode("utf-8")[:24]
    encoded_hashed_password = base64.b64encode(dk).decode("utf-8")[:24]
    return encoded_salt, encoded_hashed_password


def randstr(length):
    characters = string.ascii_lowercase
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


def main(page: Page):
    page.title = randstr(10)
    page.padding = 35
    page.fonts = {
        "poppins": f"/font/Poppins-Regular.ttf"
    }
    page.theme = Theme(use_material3=True, font_family="poppins")
    page.window_maximizable = False
    page.window_resizable = False

    headParagraph = Text("MoxFy's Admin Panel (Beta Version)", size=21, weight="bold")

    username = TextField(
        hint_text="The username that is selected will be shown here.",
        read_only=True,
        border_color="#BDB5D5",
        border_radius=10,
        content_padding=Padding(left=5, top=3, right=5, bottom=3),
    )

    def highlight(e):
        e.control.style.color = colors.PINK_100
        e.control.update()

    def unhighlight(e):
        e.control.style.color = None
        e.control.update()

    def close_update_dlg(e):
        updateDialog.open = False
        page.update()

    def open_update_dlg(e):
        page.dialog = updateDialog
        updateDialog.open = True
        page.update()

    def close_delete_dlg(e):
        deleteDialog.open = False
        page.update()

    def open_delete_dlg(e):
        page.dialog = deleteDialog
        deleteDialog.open = True
        page.update()

    def close_add_dlg(e):
        addDialog.open = False
        page.update()

    def open_add_dlg(e):
        page.dialog = addDialog
        addDialog.open = True
        page.update()

    def close_delete_all_dlg(e):
        deleteAllDialog.open = False
        page.update()

    def open_delete_all_dlg(e):
        if not len(myTable.rows) == 0:
            page.dialog = deleteAllDialog
            deleteAllDialog.open = True
            page.update()
        else:
            return

    updatePasswordTitle = Text("Update Password")
    deleteUserTitle = Text("Removing a user")
    deleteAllUsersTitle = Text("Removing all users")
    deleteUserExplain = Text("*This action can be undone!")
    addUserTitle = Text("Adding a user")

    usernameDialog = TextField(
        label="Username",
        read_only=True,
        border_color="#BDB5D5",
        border_radius=10,
        content_padding=Padding(left=5, top=3, right=5, bottom=3),
    )

    newPassword = TextField(
        hint_text="New Password",
        border_color="#BDB5D5",
        password=True,
        can_reveal_password=True,
        content_padding=Padding(left=5, top=3, right=5, bottom=3),
    )

    addUserName = TextField(
        hint_text="Username",
        border_color="#BDB5D5",
        content_padding=Padding(left=5, top=3, right=5, bottom=3),
    )

    addPassword = TextField(
        hint_text="Password",
        border_color="#BDB5D5",
        password=True,
        can_reveal_password=True,
        content_padding=Padding(left=5, top=3, right=5, bottom=3),
    )

    def UpdatePassword(username):
        if not newPassword.value or not newPassword.value.strip():
            return
        user = collection.find_one({"username": username})
        if user:
            encoded_salt, encoded_hashed_password = hash_password(newPassword.value)
            collection.update_one(
                {"username": username},
                {"$set": {"salt": encoded_salt, "password": encoded_hashed_password}},
            )
            close_update_dlg(e=None)
            newPassword.value = None
            for row in myTable.rows:
                if row.cells[0].content.value == username:
                    row.cells[1].content.value = encoded_salt
                    row.cells[2].content.value = encoded_hashed_password
                    break
            page.show_snack_bar(
                SnackBar(
                    Text("Password updated!", color="#90EE90"),
                    bgcolor="black",
                    open=True,
                )
            )
        else:
            return
        page.update()

    def DeleteUser(delUser):
        user_to_remove = {"username": delUser}
        result = collection.delete_one(user_to_remove)
        if result.deleted_count > 0:
            close_delete_dlg(e=None)
            for row in myTable.rows:
                if row.cells[0].content.value == delUser:
                    myTable.rows.remove(row)
                    break
            username.border_color = "#BDB5D5"
            usernameDialog.value = None
            usernameDialog.label = None
            username.value = None
            trackUsernum()
            page.show_snack_bar(
                SnackBar(
                    Text(f"Deleted {delUser}!", color="#90EE90"),
                    bgcolor="black",
                    open=True,
                )
            )
        else:
            return
        page.update()

    def DeleteAllUsers(e):
        filter = {}
        result = collection.delete_many(filter)
        if result.deleted_count > 0:
            close_delete_all_dlg(e=None)
            myTable.rows.clear()
            username.border_color = "#BDB5D5"
            usernameDialog.value = None
            usernameDialog.label = None
            username.value = None
            trackUsernum()
            page.show_snack_bar(
                SnackBar(
                    Text(f"Deleted all users!", color="#90EE90"),
                    bgcolor="black",
                    open=True,
                )
            )
        else:
            return
        page.update()

    def AddUser(addUser):
        if not addPassword.value or not addPassword.value.strip():
            return
        user = collection.find_one({"username": addUser})
        if user:
            page.show_snack_bar(
                SnackBar(
                    Text(
                        "Username already exists.",
                        color="#90EE90",
                    ),
                    bgcolor="black",
                    open=True,
                )
            )
            return
        if 8 <= len(addUser) <= 12:
            encoded_salt, encoded_hashed_password = hash_password(addPassword.value)
            new_user = {
                "username": addUser,
                "salt": encoded_salt,
                "password": encoded_hashed_password,
            }
            result = collection.insert_one(new_user)
            if result.inserted_id:
                close_add_dlg(e=None)
                row = DataRow(
                    cells=[
                        DataCell(Text(addUser)),
                        DataCell(Text(encoded_hashed_password)),
                        DataCell(Text(encoded_salt)),
                    ],
                    on_select_changed=lambda e: resolveUser(
                        e.control.cells[0].content.value
                    ),
                )
                myTable.rows.append(row)
                addUserName.value = None
                addPassword.value = None
                trackUsernum()
                page.show_snack_bar(
                    SnackBar(
                        Text(f"Added: {addUser}!", color="#90EE90"),
                        bgcolor="black",
                        open=True,
                    )
                )
            else:
                return
            page.update()
        else:
            page.show_snack_bar(
                SnackBar(
                    Text(
                        "Username must be between 8 and 12 characters.", color="#90EE90"
                    ),
                    bgcolor="black",
                    open=True,
                )
            )

    deleteColumn = Container(
        width=400,
        height=75,
        content=Column(
            [
                usernameDialog,
                deleteUserExplain,
            ],
        ),
    )

    deleteAllusersColumn = Container(
        width=400,
        height=25,
        content=Column(
            [
                deleteUserExplain,
            ],
        ),
    )

    updateColumnPassword = Container(
        width=400,
        height=100,
        content=Column(
            [
                usernameDialog,
                newPassword,
            ],
        ),
    )

    addColumnUser = Container(
        width=400,
        height=100,
        content=Column(
            [
                addUserName,
                addPassword,
            ],
        ),
    )

    updateConfirmDialog = Text(
        size=15,
        weight="w400",
        disabled=False,
        spans=[
            TextSpan(
                "Confirm",
                TextStyle(decoration=TextDecoration.NONE),
                on_click=lambda e: UpdatePassword(
                    usernameDialog.value,
                ),
                on_enter=highlight,
                on_exit=unhighlight,
            ),
        ],
    )

    deleteConfirmDialog = Text(
        size=15,
        weight="w400",
        disabled=False,
        spans=[
            TextSpan(
                "Confirm",
                TextStyle(decoration=TextDecoration.NONE),
                on_click=lambda e: DeleteUser(
                    usernameDialog.value,
                ),
                on_enter=highlight,
                on_exit=unhighlight,
            ),
        ],
    )

    deleteAllConfirmDialog = Text(
        size=15,
        weight="w400",
        disabled=False,
        spans=[
            TextSpan(
                "Confirm",
                TextStyle(decoration=TextDecoration.NONE),
                on_click=DeleteAllUsers,
                on_enter=highlight,
                on_exit=unhighlight,
            ),
        ],
    )

    addConfirmDialog = Text(
        size=15,
        weight="w400",
        disabled=False,
        spans=[
            TextSpan(
                "Confirm",
                TextStyle(decoration=TextDecoration.NONE),
                on_click=lambda e: AddUser(
                    addUserName.value,
                ),
                on_enter=highlight,
                on_exit=unhighlight,
            ),
        ],
    )

    ExitUpdateDialog = Text(
        size=15,
        weight="w400",
        disabled=False,
        spans=[
            TextSpan(
                "Exit",
                TextStyle(decoration=TextDecoration.NONE),
                on_click=close_update_dlg,
                on_enter=highlight,
                on_exit=unhighlight,
            ),
        ],
    )

    ExitDeleteDialog = Text(
        size=15,
        weight="w400",
        disabled=False,
        spans=[
            TextSpan(
                "Exit",
                TextStyle(decoration=TextDecoration.NONE),
                on_click=close_delete_dlg,
                on_enter=highlight,
                on_exit=unhighlight,
            ),
        ],
    )

    ExitAddDialog = Text(
        size=15,
        weight="w400",
        disabled=False,
        spans=[
            TextSpan(
                "Exit",
                TextStyle(decoration=TextDecoration.NONE),
                on_click=close_add_dlg,
                on_enter=highlight,
                on_exit=unhighlight,
            ),
        ],
    )

    ExitDeleteAllDialog = Text(
        size=15,
        weight="w400",
        disabled=False,
        spans=[
            TextSpan(
                "Exit",
                TextStyle(decoration=TextDecoration.NONE),
                on_click=close_delete_all_dlg,
                on_enter=highlight,
                on_exit=unhighlight,
            ),
        ],
    )

    updateDialog = AlertDialog(
        shape=None,
        modal=True,
        title=updatePasswordTitle,
        content=updateColumnPassword,
        actions=[
            updateConfirmDialog,
            ExitUpdateDialog,
        ],
        actions_alignment=MainAxisAlignment.END,
    )

    deleteDialog = AlertDialog(
        shape=None,
        modal=True,
        title=deleteUserTitle,
        content=deleteColumn,
        actions=[
            deleteConfirmDialog,
            ExitDeleteDialog,
        ],
        actions_alignment=MainAxisAlignment.END,
    )

    addDialog = AlertDialog(
        shape=None,
        modal=True,
        title=addUserTitle,
        content=addColumnUser,
        actions=[
            addConfirmDialog,
            ExitAddDialog,
        ],
        actions_alignment=MainAxisAlignment.END,
    )

    deleteAllDialog = AlertDialog(
        shape=None,
        modal=True,
        title=deleteAllUsersTitle,
        content=deleteAllusersColumn,
        actions=[
            deleteAllConfirmDialog,
            ExitDeleteAllDialog,
        ],
        actions_alignment=MainAxisAlignment.END,
    )

    creatButton = OutlinedButton(
        "Add user",
        style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        on_click=open_add_dlg,
    )
    updatebutton = OutlinedButton(
        "Update user",
        style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        on_click=open_update_dlg,
        disabled=True,
    )
    deleteButton = OutlinedButton(
        "Delete user",
        style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        on_click=open_delete_dlg,
        disabled=True,
    )
    deleteAllUserButton = ElevatedButton(
        "Delete All Users",
        style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        on_click=open_delete_all_dlg,
        bgcolor="red",
        color="white",
    )

    myTable = DataTable(
        heading_row_color=colors.BLACK54,
        data_row_color={"hovered": "0x30FF0000"},
        vertical_lines=border.BorderSide(1, "blue"),
        horizontal_lines=border.BorderSide(1, "blue"),
        border=border.all(1, "blue"),
        columns=[
            DataColumn(Text("Username (Unecrypted)")),
            DataColumn(Text("Password (Encrypted)")),
            DataColumn(Text("Salt (Encrypted)")),
        ],
        rows=[],
    )

    myContent = Column(
        [
            myTable,
        ],
        scroll=ScrollMode.HIDDEN,
        expand=True,
        height=350,
        width=1200,
    )

    myContainer = Container(
        myContent,
        alignment=alignment.center,
    )

    def resolveUser(e):
        username.value = str(e)
        usernameDialog.value = str(e)
        username.border_color = "green"

        updatebutton.disabled = False
        deleteButton.disabled = False
        page.update()

    if is_internet_available():
        from credentials import cursor, collection

        user_count = 0
        for document in cursor:
            myTable.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(document["username"])),
                        DataCell(Text(document["password"])),
                        DataCell(Text(document["salt"])),
                    ],
                    on_select_changed=lambda e: resolveUser(
                        e.control.cells[0].content.value
                    ),
                )
            )
            user_count += 1

        sum = Text(f"Total number of users: {user_count}")

        page.add(
            Column(
                [
                    Row([headParagraph]),
                    Row([sum]),
                    Divider(height=1, color="transparent"),
                    username,
                    Divider(height=1, color="transparent"),
                    Row(
                        [creatButton, updatebutton, deleteButton, deleteAllUserButton],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Divider(height=1, color="transparent"),
                    Row([myContainer]),
                ]
            )
        )

    else:
        noConnection = Text(
            "No internet connection detected. Please check your internet connection.",
            size=21,
            weight="w400",
            color="#808080",
        )
        page.add(
            Column(
                [
                    Row([noConnection]),
                ]
            )
        )
    page.update()

    def trackUsernum():
        user_count = len(myTable.rows)
        sum.value = f"Total number of users: {user_count}"
        sum.update()


if __name__ == "__main__":
    app(target=main, view=FLET_APP, assets_dir="assets")
