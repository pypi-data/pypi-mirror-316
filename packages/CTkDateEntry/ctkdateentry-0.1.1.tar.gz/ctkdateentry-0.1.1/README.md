# CTkDateEntry

**CTkDateEntry** is a Python library that extends the use of `customtkinter` to provide custom widgets such as a customtkinter DateEntry with a calendar `CTkCalendar` with selectable dates. It was designed to make it easier to create more modern and interactive graphical user interfaces (GUIs).


## Example:

Debug CTkDateEntry

![img_1](https://github.com/user-attachments/assets/d0be5cc6-7ab2-4135-b85a-64a1a386a097)

## Example:

Open Calendar CTkDateEntry

![Img_2](https://github.com/user-attachments/assets/e3799515-59d5-4347-a95a-d63f1ec7347a "CTkDateEntry open Calendar")

## Features

- **CTkDateEntry**: A custom DateEntry based on Customtkinter to facilitate date selection in graphical interfaces.

## Themes

- **CTkDateEntry**: When customtkinter themes are applied to the graphical interface, they are automatically applied to CTkDateEntry, meaning there is no need to use a separate Theme Style

## Usage

Here's a simple example of how to use the `CTkDateEntr` widget:

```
import customtkinter asctk
from ctkdateentry import CTkDateEntry

root = ctk.CTk()

root.geometry('200x200')

root.title('CTkDateEntry ')

calendar = CTkDateEntry(root)

calendar.pack(pady=50)

root.mainloop()
```
