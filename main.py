import argparse
import tkinter
from tkinter import *
import tkinter as tki
from Shape import Rectangle, Elips, Shape, Triangle, Lines, Eraser, TextShape, PolygonShape
from tkinter import colorchooser, filedialog, messagebox
from PIL import (ImageGrab, ImageTk, Image)
import json
from typing import Any, Optional, Callable, List

BUTTON_WIDTH: int = 30
SHAPE_BUTTON_WIDTH: int = 10
SHAPE_BUTTON_BG: str = "lavender"


class Draw:
    """
    Main class for the drawing application.
    This class represents the main functionality of a drawing application. It provides methods to create shapes,
    interact with the canvas, manage undo and redo actions, save and load work, and change the drawing tools.
        """

    def __init__(self) -> None:
        """
        Initialize the drawing application.
        This method initializes the drawing application by creating the main window, canvas, and various buttons
        for different functionalities.
                """

        self.start_y: Optional[int] = None
        self.start_x = None
        self.selected_text: List[Any] = []
        self.on_text_release: Optional[Callable] = None
        self.on_text_drag: Optional[Callable] = None
        self.text_item: Optional[int] = None
        self.on_text_click: Optional[Callable] = None
        self.current_polygon: Optional[PolygonShape] = None
        self.text_entry: Optional[Entry] = None
        self.text_alignment: str = ""
        self.eraser_size: Optional[int] = None
        self.__root: tkinter.Tk = tki.Tk()
        self.tool_mode: str = "paint"

        self.canvas_frame: Frame = tki.Frame(self.__root)
        self.canvas_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self.__canvas: Canvas = Canvas(self.__root, bg='white', width=600, height=600)
        self.__canvas.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)

        self.bar_frame: Frame = tki.Frame(self.__root, bg="lavender")
        self.bar_frame.pack(side=tki.TOP, fill=tki.X)

        self.create_buttons()
        self.create_shapes()
        self.create_delete_buttons()
        self.create_save_buttons()
        self.bring_to_front = Button(self.bar_frame, text="front", width=10, bg="lavender", command=self.bring_to_front)
        self.bring_to_front.pack(side=tki.LEFT, padx=5)

        self.prev_x: Optional[int] = None
        self.prev_y: Optional[int] = None
        self.deleted_shapes: List[Optional[int]] = []

        self.__root.mainloop()

    # ______________________________#Using the brush and the eraser#___________________________________________________

    def set_button_image(self, image_location: str, image_size: int) -> ImageTk.PhotoImage:
        """
                Loads an image from the specified location, resizes it to the provided size,
                and converts it to a Tkinter PhotoImage object.

                Parameters:
                    image_location (str): The file path or URL of the image.
                    image_size (int): The desired size (in pixels) for the image (both width and height).

                Returns:
                    ImageTk.PhotoImage: The PhotoImage object containing the resized image.
                """
        button_image = Image.open(image_location).resize((image_size, image_size))
        return ImageTk.PhotoImage(button_image)

    def create_shape_button(self, shape_button_frame: Frame, shape_image: ImageTk.PhotoImage, button_width: int,
                            button_bg: str,
                            button_command: Callable) -> None:
        """
                Creates a button with the specified shape image, width, background color, and command function,
                and places it in the specified frame.

                Parameters:
                    shape_button_frame (Frame): The frame in which the button will be placed.
                    shape_image (ImageTk.PhotoImage): The image to be displayed on the button.
                    button_width (int): The width of the button.
                    button_bg (str): The background color of the button.
                    button_command (Callable): The function to be called when the button is clicked.

                Returns:
                    None
                """
        shape_button = Button(shape_button_frame, image=shape_image, width=button_width, bg=button_bg,
                              command=button_command)
        shape_button.pack(side=tki.TOP, padx=5)

    def change_to_eraser(self) -> None:
        """This method sets the cursor to 'X_cursor' to indicate that the eraser tool is active. It then creates
                an instance of the Eraser class to handle erasing actions on the canvas."""
        if Shape.last_selected is not None:
            Shape.last_selected.on_unselect()
        self.__canvas.config(cursor="X_cursor")
        Eraser(self.__canvas)

    def change_to_pen(self) -> None:
        """Change the drawing tool to pen.

                This method sets the cursor to 'arrow' to indicate that the pen tool is active. It then creates
                an instance of the Lines class to handle drawing actions on the canvas."""
        if Shape.last_selected is not None:
            Shape.last_selected.on_unselect()
        self.__canvas.config(cursor="arrow")
        Lines(self.__canvas, Shape.current_color)

    # _______________________________#Delete and clear functions#______________________________________________________
    def delete_it(self) -> None:
        """
        Delete the selected shape.

       This method deletes the currently selected shape from the canvas.

       Returns:
       None
       """
        if Shape.last_selected is not None:
            Shape.last_selected.delete()

    def clear_canvas(self) -> None:
        """
        Clear all shapes from the canvas.

        This method removes all shapes drawn on the canvas.

        Returns:s
        None
        """
        for shape in Shape.shape_list[:]:
            shape.delete(is_to_remove_from_list=False)
        Shape.shape_list.clear()

    # ______________________________#Add shapes functions#______________________________________________________________

    # Add shapes
    def add_elips(self) -> None:
        """
            Add an ellipse shape to the canvas.

            This method creates an ellipse shape with default dimensions and positions it at the center of
            the canvas.
            If there is an ongoing polygon drawing, this method does nothing.

            Returns:
            None
            """
        if self.current_polygon is not None:
            return
        elips = Elips(self.__canvas, 50, 60, Shape.current_color)
        elips.set_outline(Shape.current_outline_color, Shape.current_width)
        elips.move(self.__canvas.winfo_width() / 2, self.__canvas.winfo_height() / 2)

    def add_circle(self) -> None:
        """
        Add a circle shape to the canvas.

        This method creates a circle shape with default dimensions and positions it at the center of
        the canvas.
        If there is an ongoing polygon drawing, this method does nothing.

        Returns:
        None
        """
        if self.current_polygon is not None:
            return
        circle = Elips(self.__canvas, 60, 60, Shape.current_color)
        circle.set_outline(Shape.current_outline_color, Shape.current_width)
        circle.move(self.__canvas.winfo_width() / 2, self.__canvas.winfo_height() / 2)

    def add_rectangle(self) -> None:
        """
        Add a rectangle shape to the canvas.

        This method creates a rectangle shape with default dimensions and positions it at the center
        of the canvas.
        If there is an ongoing polygon drawing, this method does nothing.

        Returns:
        None
        """
        if self.current_polygon is not None:
            return
        rect = Rectangle(self.__canvas, 100, 100, Shape.current_color)
        rect.set_outline(Shape.current_outline_color, Shape.current_width)
        rect.move(self.__canvas.winfo_width() / 2, self.__canvas.winfo_height() / 2)

    def add_triangle(self) -> None:
        """
        Add a triangle shape to the canvas.

        This method creates a triangle shape with default dimensions and positions it at the center of
        the canvas.
        If there is an ongoing polygon drawing, this method does nothing.

        Returns:
        None
        """
        if self.current_polygon is not None:
            return
        triangle = Triangle(self.__canvas, 100, 150, Shape.current_color)
        triangle.set_outline(Shape.current_outline_color, Shape.current_width)
        triangle.move(self.__canvas.winfo_width() / 2, self.__canvas.winfo_height() / 2)

    def start_polygon(self) -> None:
        """
            Start drawing a polygon shape.

            This method initiates the drawing of a polygon shape on the canvas.

            Returns:
                None
            """
        if self.current_polygon:
            self.current_polygon.stop_draw()
            self.current_polygon = None

        if self.current_polygon is None:
            self.current_polygon = PolygonShape(self.__canvas, Shape.current_color)
            self.current_polygon.start_draw()
            self.__canvas.bind("<Double-Button-1>", self.stop_polygon)

    def stop_polygon(self, event) -> None:
        """
            Stop drawing a polygon shape.

            This method stops the drawing of a polygon shape on the canvas.

            Returns:
                None
            """
        if self.current_polygon:
            self.current_polygon.stop_draw()
            self.current_polygon = None
            self.__canvas.unbind("<Double-Button-1>")

    # ______________________________________________________________________________________________________________
    def color(self) -> None:
        """
            Set the current drawing color.

            This method opens a color chooser dialog and sets the current drawing color to the selected color.
            It also updates the color buttons accordingly.

            Returns:
                None
            """
        color: Any = colorchooser.askcolor()[1]
        if color:
            self.choose_color_button.config(bg=color, fg="white")
            Shape.current_color = color
            if Shape.last_selected is not None:
                Shape.last_selected.set_color(color)

    def set_outline_color(self) -> None:
        """
                Allows the user to select a color for the outline of the shape using a color picker dialog.
                Updates the outline color of the shape and the color of a button indicating the selected color.

                Returns:
                    None
                """
        color: Any = colorchooser.askcolor()[1]
        if color:
            self.choose_outline_color_button.config(bg=color, fg="white")
            Shape.current_outline_color = color
            if Shape.last_selected is not None:
                Shape.last_selected.outline_color = color
                Shape.last_selected.set_outline_color(Shape.last_selected, color)

    # ____________________________________#Changing sizes#__________________________________________________________
    def change_brush_size(self, size: str) -> None:
        """
            Set the current outline color.

            This method opens a color chooser dialog and sets the current outline color to the selected color.
            It also updates the outline color buttons accordingly.

            Returns:
                None
            """
        Shape.current_width = size
        if Shape.last_selected is not None:
            Shape.last_selected.set_outline(Shape.last_selected.outline_color, size)

    def change_eraser_size(self, size: int) -> None:
        """
            Change the size of the eraser.

            This method updates the size of the eraser used for drawing.

            Args:
                size (int): The size of the eraser.

            Returns:
                None
            """
        self.eraser_size = size

    # ______________________________________________________________________________________________________________
    def bring_to_front(self) -> None:
        """
            Bring the selected shape to the front.

            This method brings the selected shape to the front of all other shapes on the canvas.

            Returns:
                None
            """
        print("bring_to_front")
        self.__canvas.tag_raise(Shape.last_selected.shape)
        # Move the last selected shape to the end of the shape_list
        Shape.shape_list.remove(Shape.last_selected)
        Shape.shape_list.append(Shape.last_selected)

    def add_text(self) -> None:
        """
            Add text to the canvas.

            This method opens a window to input text properties and adds the entered text to the canvas.

            Returns:
                None
            """
        self.text_window = Toplevel(self.__root)
        self.text_window.title("Add Text")

        self.text_entry = Entry(self.text_window)
        self.text_entry.pack(pady=5)

        self.font = ["Arial", "Times New Roman", "Verdana"]
        self.font_var = StringVar(self.text_window)
        self.font_var.set(self.font[0])
        self.font_menu = OptionMenu(self.text_window, self.font_var, *self.font)
        self.font_menu.pack(pady=5)

        self.text_color_label = Label(self.text_window, text="Text Color:")
        self.text_color_label.pack(pady=5)
        self.text_color_var = StringVar(self.text_window)
        self.text_color_var.set("black")
        self.text_color_menu = OptionMenu(self.text_window, self.text_color_var, "black", "red", "blue", "green")
        self.text_color_menu.pack(pady=5)

        self.font_size_label = Label(self.text_window, text="Text Size:")
        self.font_size_label.pack(pady=5)
        self.font_size_var = StringVar(self.text_window)
        self.font_size_var.set("12")
        self.font_size_entry = Entry(self.text_window, textvariable=self.font_size_var)
        self.font_size_entry.pack(pady=5)

        self.add_text_button = Button(self.text_window, text="Add Text", command=self.add_text_to_canvas)
        self.add_text_button.pack(pady=5)

        self.text_window.mainloop()

    def add_text_to_canvas(self) -> None:
        """
            Add text to the canvas.

            This method adds the text to the canvas.

            Returns:
                None
            """
        text = TextShape(self.__canvas, self.text_entry.get(), self.font_var.get(), int(self.font_size_var.get()),
                         "normal",
                         self.text_color_var.get())
        text.add_text()

    # _________________________________#Save and load functions#____________________________________________________
    def save_work(self) -> None:
        """
            Save the current work to a JSON file.

            This method saves the current work, including all shapes drawn on the canvas, to a JSON file.
            The user is prompted to select a location to save the file.

            Returns:
                None
            """
        global i
        if len(Shape.shape_list) == 0:
            messagebox.showerror("Error", "You have not created any shapes")
            return
        json_file = '['
        if len(Shape.shape_list) == 1:
            json_file += str(Shape.shape_list[0]) + ']'
        else:
            for i in range(len(Shape.shape_list) - 1):
                json_file += str(Shape.shape_list[i]) + ','
            json_file += str(Shape.shape_list[i + 1])
            json_file += ']'
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(json_file)

    def load_work(self) -> None:
        """
            Load previously saved work from a JSON file.

            This method loads previously saved work from a JSON file.
            The user is prompted to select the file to load.

            Returns:
                 None
            """
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        f = open(file_path)
        data = json.load(f)
        for item in data:
            if item["name"] == "Triangle":
                triangle = Triangle(self.__canvas, item["base"], item["height"], item["color"])
                triangle.set_outline(item["outline_color"], item["outline_width"])
                triangle.move(item["x"], item["y"])
                self.__canvas.scale(triangle.shape, item["x"], item["y"], item["current_width"] / item["base"],
                                    item["current_height"] / item["height"])

            elif item["name"] == "Rectangle":
                rect = Rectangle(self.__canvas, item["width"], item["height"], item["color"])
                rect.set_outline(item["outline_color"], item["outline_width"])
                rect.move(item["x"], item["y"])
                self.__canvas.scale(rect.shape, item["x"], item["y"], item["current_width"] / item["width"],
                                    item["current_height"] / item["height"])

            elif item["name"] == "Elips":
                elips = Elips(self.__canvas, item["radius_1"], item["radius_2"], item["color"])
                elips.set_outline(item["outline_color"], item["outline_width"])
                elips.move(item["x"], item["y"])
                self.__canvas.scale(elips.shape, item["x"], item["y"], item["current_width"] / item["radius_1"],
                                    item["current_height"] / item["radius_2"])
            elif item["name"] == "PolygonShape":
                polygon = PolygonShape(self.__canvas, item["color"])
                polygon.points = item["points"]
                polygon.set_outline(item["outline_color"], item["outline_width"])
                polygon.update_polygon()
                Shape.shape_list.append(polygon)
            elif item["name"] == "Lines":
                lines = Lines(self.__canvas, item["color"])
                lines.drawn_points = item["lines"]
                lines.width = item["width"]
                lines.connect_points()
            elif item["name"] == "Eraser":
                lines = Eraser(self.__canvas)
                lines.drawn_points = item["lines"]
                lines.width = item["width"]
                lines.connect_points()

            elif item["name"] == "TextShape":
                # Load TextShape
                text_shape = TextShape(self.__canvas, item["text"], item["font_family"], item["font_size"],
                                       item["font_style"])
                text_shape.set_color(item["color"])
                text_shape.set_outline(item["outline_color"], item["outline_width"])
                text_shape.set_position(item["x"], item["y"])  # Set the position of the TextShape
                text_shape.add_text()

    def save_image(self) -> None:
        """
            Save a screenshot of the canvas as an image file.

            This method captures a screenshot of the canvas and saves it as a PNG or JPEG image file.
            The user is prompted to select the location and file format to save the screenshot.

            Returns:
                None
            """
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),
                                                                                         ("JPEG files", "*.jpg")])
            if file_path:
                x0 = self.__root.winfo_rootx() + self.__canvas.winfo_x()
                y0 = self.__root.winfo_rooty() + self.__canvas.winfo_y()
                x1 = x0 + self.__canvas.winfo_width()
                y1 = y0 + self.__canvas.winfo_height()
                ImageGrab.grab().crop((x0, y0, x1 + 600, y1 + 400)).save(file_path)
                messagebox.showinfo("Success", "Screenshot saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed saving: {str(e)}")

    # ______________________________#Brush, text and eraser buttons#____________________________________________________
    def create_buttons(self) -> None:
        """
        Create buttons for brush, text, and eraser.

        This method creates buttons for selecting the brush, text, and eraser tools.
        """
        # eraser
        self.eraser_image = Image.open("images/eraser.png").resize((30, 30))
        self.eraser_icon = ImageTk.PhotoImage(self.eraser_image)
        self.eraser_button = Button(self.bar_frame, image=self.eraser_icon, command=self.change_to_eraser, width=30,
                                    bg="lavender")
        self.eraser_button.pack(side=tki.LEFT, padx=5)

        # brush
        self.brush_image = Image.open("images/paint-brush.png").resize((30, 30))
        self.brush_icon = ImageTk.PhotoImage(self.brush_image)
        self.brush_button = Button(self.bar_frame, image=self.brush_icon, width=30, command=self.change_to_pen,
                                   bg="lavender")
        self.brush_button.pack(side=tki.LEFT, padx=5)

        # Create a frame for the scale
        self.scale_frame = tki.Frame(self.bar_frame)
        self.scale_frame.pack(side=tki.LEFT, padx=5)

        # Create the label widget
        self.label = tki.Label(self.scale_frame, text="size")
        self.label.pack(side=tki.TOP, pady=(0, 5))

        # Create the scale widget
        self.brush_size_scale = tki.Scale(self.scale_frame, from_=1, to=10, orient=tki.HORIZONTAL,
                                          command=self.change_brush_size)
        self.brush_size_scale.pack(side=tki.TOP, pady=(0, 5))

        # choose color
        self.choose_color_button = Button(self.bar_frame, text="color", width=10, bg="lavender", command=self.color)
        self.choose_color_button.pack(side=tki.LEFT, padx=5)

        self.choose_outline_color_button = Button(self.bar_frame, text="outline color", width=10, bg="lavender",
                                                  command=self.set_outline_color)
        self.choose_outline_color_button.pack(side=tki.LEFT, padx=5)

        # text
        self.text_image = Image.open("images/font.png").resize((30, 30))
        self.text_icon = ImageTk.PhotoImage(self.text_image)
        self.add_text_button = Button(self.bar_frame, image=self.text_icon, width=30, bg="lavender",
                                      command=self.add_text)
        self.add_text_button.pack(side=tki.LEFT, padx=5)

        # polygon
        self.polygon_button_frame = tki.Frame(self.bar_frame, bg="lavender")
        self.polygon_button_frame.pack(side=tki.LEFT)
        self.start_polygon_button = Button(self.polygon_button_frame, text="Start Polygon", width=10,
                                           command=self.start_polygon)
        self.start_polygon_button.pack(side=tki.TOP, padx=5)
        Label(self.polygon_button_frame, text="Double click for stop").pack(side=tki.TOP, padx=5)

    # _______________________________________________#Shapes buttons#__________________________________________________
    def create_shapes(self) -> None:
        """
        Create buttons for adding different shapes.

        This method creates buttons for adding rectangle, ellipse, circle, and triangle shapes.
        """
        self.shape_button_frame = tki.Frame(self.bar_frame, bg="lavender")
        self.shape_button_frame.pack(side=tki.LEFT)

        self.rectangle_image = self.set_button_image("images/rectangle.png", 10)
        self.create_shape_button(self.shape_button_frame, self.rectangle_image, SHAPE_BUTTON_WIDTH, SHAPE_BUTTON_BG,
                                 self.add_rectangle)

        self.oval_image = self.set_button_image("images/oval.png", 10)
        self.create_shape_button(self.shape_button_frame, self.oval_image, SHAPE_BUTTON_WIDTH, SHAPE_BUTTON_BG,
                                 self.add_elips)

        self.circle_image = self.set_button_image("images/circle.png", 10)
        self.create_shape_button(self.shape_button_frame, self.circle_image, SHAPE_BUTTON_WIDTH, SHAPE_BUTTON_BG,
                                 self.add_circle)

        self.triangle_image = self.set_button_image("images/triangle.png", 10)
        self.create_shape_button(self.shape_button_frame, self.triangle_image, SHAPE_BUTTON_WIDTH, SHAPE_BUTTON_BG,
                                 self.add_triangle)

    # ______________________________#Delete and clear all buttons#____________________________________________________
    def create_delete_buttons(self) -> None:
        """
            Create buttons for deleting shapes and clearing the canvas.

            This method creates buttons for deleting selected shapes and clearing all shapes from the canvas.
        """
        self.delete_button_frame = tki.Frame(self.bar_frame, bg="lavender")
        self.delete_button_frame.pack(side=tki.LEFT)

        self.delete = Button(self.delete_button_frame, text="delete", width=10, bg="lavender", command=self.delete_it)
        self.delete.pack(side=tki.TOP, padx=5)

        self.clear = Button(self.delete_button_frame, text="clear_all", width=10, bg="lavender",
                            command=self.clear_canvas)
        self.clear.pack(side=tki.TOP, padx=5)

    # ______________________________#Save and load buttons#____________________________________________________
    def create_save_buttons(self) -> None:
        """
        Create buttons for saving and loading work.

        This method creates buttons for saving the current canvas as an image, saving the current work to a file,
        and loading previously saved work from a file.
        """
        self.save_buttons_frame = tki.Frame(self.bar_frame, bg="lavender")
        self.save_buttons_frame.pack(side=tki.LEFT)

        self.save_button = Button(self.save_buttons_frame, text="save png", width=10, bg="lavender",
                                  command=self.save_image)
        self.save_button.pack(side=tki.TOP, padx=5)

        self.save_button = Button(self.save_buttons_frame, text="save work", width=10, bg="lavender",
                                  command=self.save_work)
        self.save_button.pack(side=tki.BOTTOM, padx=5)

        self.save_button = Button(self.save_buttons_frame, text="load work", width=10, bg="lavender",
                                  command=self.load_work)
        self.save_button.pack(side=tki.LEFT, padx=5)


# _____________________________ The instructions for using the project.____________________________________________

parser = argparse.ArgumentParser(description='Here are the instructions for using your project:\n\n'
                                             'Choosing Shapes: Click on the corresponding shape button '
                                             '(rectangle, ellipse, circle, triangle) to select it.\n\n'
                                             'To draw a polygon, click on the canvas to create points. To finish '
                                             'drawing the polygon, double-click on the circle that appears at the '
                                             'end of the line.\n\nTo resize shapes, click and drag the circle located '
                                             'on the red bounding box at the bottom right corner of the shape. Dragging'
                                             'this circle allows you to enlarge or shrink the shape according to your '
                                             'desired size.')
parser.add_argument('--masters', nargs='?', default=None, type=int, help='Enter one or more ids.')

if __name__ == "__main__":
    parser.parse_args()
    draw = Draw()
