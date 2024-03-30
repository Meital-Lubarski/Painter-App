from tkinter import Canvas, Event
from typing import List, Any, Tuple, Union


class Shape:
    """
        This class represents a generic shape on a canvas.

        Attributes:
            points (list): A list of tuples representing the points of the shape.
            counter (int): A counter to keep track of the number of shapes.
            last_selected (Any): Reference to the last selected shape.
            current_color (str): The current fill color of the shape.
            current_outline_color (str): The current outline color of the shape.
            current_width (int): The current width of the shape's outline.
            last_deleted (Any): Reference to the last deleted shape.
            shape_list (List['Shape']): A list containing all the shapes drawn on the canvas.
            select_bbox (Any): Reference to the bounding box used for selection.
            select_circle (Any): Reference to the circle used for selection.
            center_x (int): The x-coordinate of the center of the shape.
            center_y (int): The y-coordinate of the center of the shape.
            line_mode (bool): A flag indicating if the shape is in line drawing mode.
        """
    points: list[tuple[float, float]] = []
    counter: int = 0
    last_selected: Any = None
    current_color: str = "white"
    current_outline_color: str = "black"
    current_width: int = 1
    last_deleted: Any = None
    shape_list: List['Shape'] = []
    select_bbox: Any = None
    select_circle: Any = None
    center_x: int = -1000
    center_y: int = -1000
    line_mode: bool = False

    def __init__(self, canvas: Canvas, color: str) -> None:
        """
            Initialize a Shape object.

            Args:
                canvas (Canvas): The canvas to draw the shape on.
                color (str): The fill color of the shape.

            Returns:
            None
        """
        print("Creating shape")
        self.x: int = 0
        self.y: int = 0
        self.canvas: Canvas = canvas
        self.color: str = color
        self.outline_color: str = Shape.current_outline_color
        self.outline_width: int = Shape.current_width
        self.shape: Any = None
        self.last_x: int = 0
        self.last_y: int = 0
        Shape.counter += 1
        self.canvas.tag_bind("clickable" + str(Shape.counter), "<Button-1>", self.on_select)
        self.canvas.tag_bind("clickable" + str(Shape.counter), "<ButtonRelease-1>", self.on_release)
        self.canvas.tag_bind("clickable" + str(Shape.counter), '<B1-Motion>', self.on_drag)
        print("Shape created")
        Shape.shape_list.append(self)

    def set_outline(self, outline_color: str, outline_width: int) -> None:
        """
            Set the outline color and width of the shape.

            Args:
                outline_color (str): The color of the outline.
                outline_width (int): The width of the outline.

            Returns:
                None
        """
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.canvas.itemconfig(self.shape, outline=self.outline_color, width=self.outline_width)

    def move(self, x: float, y: float) -> None:
        """
            Move the shape by the specified x and y distances.

            Args:
                x (float): The distance to move the shape along the x-axis.
                y (float): The distance to move the shape along the y-axis.

            Returns:
                None
            """
        if self.shape is not None:
            self.canvas.move(self.shape, x, y)
            self.x += x
            self.y += y

    def on_select(self, event: Any) -> None:
        """
            Handle the selection of the shape.

            Args:
                event (Any): The event object associated with the selection.

            Returns:
                None
            """
        print("on_select")
        if Shape.line_mode:
            return
        self.draw_select_rect()
        Shape.last_selected = self
        print("Select", event.x, event.y)
        self.start_drag(event)

    def on_unselect(self) -> None:
        """
            Handle the unselection of the shape.

            Returns:
                None
            """
        print("on_unselect")
        if Shape.select_bbox is not None:
            self.canvas.delete(Shape.select_bbox)
            Shape.select_bbox = None
        if Shape.select_circle is not None:
            self.canvas.delete(Shape.select_circle)
            Shape.select_circle = None
        Shape.last_selected = None

    def start_drag(self, event: Any) -> None:
        """
            Start dragging the shape.

            Args:
                event (Any): The event object associated with the drag action.

            Returns:
                None
            """
        if Shape.line_mode:
            return
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event: Any) -> None:
        """
           Handle dragging of the shape.

           Args:
               event (Any): The event object associated with the drag action.

           Returns:
               None
           """
        if Shape.line_mode:
            return
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.move(dx, dy)
        self.last_x = event.x
        self.last_y = event.y
        self.draw_select_rect()

    def delete(self, is_to_remove_from_list: bool = True) -> None:
        """
            Delete the shape from the canvas.

            Args:
                is_to_remove_from_list (bool): Flag indicating whether to remove the shape from the shape list.

            Returns:
                None
            """
        print("Deleting shape")
        if self.shape is None:
            return
        self.canvas.delete(self.shape)
        self.shape = None
        if is_to_remove_from_list:
            Shape.shape_list.remove(self)
        if Shape.select_bbox is not None:
            self.canvas.delete(Shape.select_bbox)
            Shape.select_bbox = None
        if Shape.select_circle is not None:
            self.canvas.delete(Shape.select_circle)
            Shape.select_circle = None

    def on_release(self, event: Any) -> None:
        """
            Handle the release event.

            This method is called when the mouse button is released after selecting or dragging a shape.

            Args:
                event (Any): The event object associated with the release action.

            Returns:
                None
            """
        print("on_release")

    def set_color(self, color: str) -> None:
        """
            Set the fill color of the shape.

            Args:
                color (str): The color to set.

            Returns:
                None
            """
        self.color = color
        self.canvas.itemconfig(self.shape, fill=color)

    def set_outline_color(self, shape: Any, color: str) -> None:
        """
            Set the outline color of the shape.

            Args:
                shape (Any): The shape object.
                color (str): The color to set for the outline.

            Returns:
                None
            """
        print("set_outline_color")
        self.outline_color = color
        self.canvas.itemconfig(self.shape, outline=color)

    def draw_select_rect(self) -> None:
        """
            Draw the selection rectangle around the shape.

            This method draws a rectangle around the selected shape for highlighting and manipulation.

            Returns:
                None
            """
        if Shape.select_circle is not None:
            self.canvas.delete(Shape.select_circle)

        if Shape.select_bbox is not None:
            self.canvas.delete(Shape.select_bbox)
        if Shape.select_circle is not None:
            self.canvas.delete(Shape.select_circle)
        bbox = self.canvas.bbox(self.shape)
        Shape.select_bbox = self.canvas.create_rectangle(bbox, outline="red", width=1)
        Shape.select_circle = self.canvas.create_oval(-5, -5, 5, 5, outline="red", fill="red", width=6,
                                                      tags="clickable_bbox")
        self.canvas.moveto(Shape.select_circle, bbox[2] - 5, bbox[3] - 5)
        self.canvas.tag_bind("clickable_bbox", '<Button-1>', self.start_scale_drag)
        self.canvas.tag_bind("clickable_bbox", '<B1-Motion>', self.on_scale_object)

    def update_select_rect(self) -> None:
        """
            Update the selection rectangle around the shape.

            This method updates the position and size of the selection rectangle based on the shape's bounding box.

            Returns:
                None
            """
        if Shape.select_bbox is None:
            return
        bbox = self.canvas.bbox(self.shape)
        self.canvas.coords(Shape.select_bbox, bbox)
        self.canvas.moveto(Shape.select_circle, bbox[2] - 5, bbox[3] - 5)

    def start_scale_drag(self, event: Any) -> None:
        """
            Begin dragging to scale the shape.

            This method is called when the user starts dragging to scale the shape.

            Args:
                event (Any): The event object associated with the start of the drag action.

            Returns:
                None
            """
        print("on_start_drag")
        self.last_x = event.x
        self.last_y = event.y
        coords = self.canvas.coords(Shape.select_bbox)
        Shape.center_x = (coords[0] + coords[2]) / 2
        Shape.center_y = (coords[1] + coords[3]) / 2

    def on_scale_object(self, event: Any) -> None:
        """
            Scale the shape based on the drag action.
            This method is called when the user drags to scale the shape.
            Args: event (Any): The event object associated with the scale action.
            Returns: None
            """
        print("on_scale_object")
        size_x = event.x - Shape.center_x
        if size_x > 1:
            scale_x = 1 + (event.x - self.last_x) / size_x
        else:
            scale_x = 1
        size_y = event.y - Shape.center_y
        print(str(size_x) + " -- " + str(scale_x))
        if size_y > 1:
            scale_y = 1 + (event.y - self.last_y) / size_y
        else:
            scale_y = 1
        print(str(size_y) + " -- " + str(scale_y))
        self.canvas.scale(self.shape, self.x, self.y, scale_x, scale_y)
        # self.canvas.moveto(self.shape, self.x, self.y)
        self.last_x = event.x
        self.last_y = event.y
        self.update_select_rect()

    def get_shape(self) -> Any:
        """
           Get the shape object.

           This method returns the shape object associated with this instance.

           Returns:
               Any: The shape object.
           """
        pass

    def __str__(self) -> str:
        """
           Return a string representation of the shape.

           This method returns a JSON-formatted string representing the attributes of the shape.

           Returns:
               str: A string representation of the shape.
           """
        bbox = self.canvas.bbox(self.shape)
        width = abs(bbox[0] - bbox[2])
        height = abs(bbox[1] - bbox[3])
        return '{"name":"' + self.__class__.__name__ + '", "x":' + str(self.x) + ',"y":' + str(
            self.y) + ', "color": "' + self.color + '", "outline_color": "' + self.outline_color + (
            '", "outline_width''": ') + str(
            self.outline_width) + ', "current_width": ' + str(width) + ', "current_height": ' + str(height)


# ______________________________________________________

class Rectangle(Shape):
    def __init__(self, canvas: Canvas, w: int, h: int, color: str) -> None:
        """
            Initialize a Rectangle object.

            Args:
                canvas (Canvas): The tkinter canvas on which the rectangle will be drawn.
                w (int): The width of the rectangle.
                h (int): The height of the rectangle.
                color (str): The fill color of the rectangle.

            Returns:
                None
        """
        super().__init__(canvas, color)
        self.half_w = w / 2
        self.half_h = h / 2
        self.shape = self.get_shape()

    def get_shape(self) -> Any:
        """
            Create the rectangle shape on the canvas.

            Returns:
                Any: The shape object representing the rectangle.
        """
        print("Creating rectangle")
        return self.canvas.create_rectangle(-self.half_w, -self.half_h, self.half_w, self.half_h,
                                            fill=self.color,
                                            tags=("clickable" + str(Shape.counter)))

    def __str__(self) -> str:
        """
            Return a string representation of the rectangle.

            Returns:
                str: A string representation of the rectangle object.
        """
        return super().__str__() + ', "width": ' + str(self.half_w * 2) + ', "height": ' + str(self.half_h * 2) + '}'


# ______________________________________________________

class Elips(Shape):
    def __init__(self, canvas: Canvas, radius_1: int, radius_2: int, color: str) -> None:
        """
            Initialize an Ellipse object.

            Args:
                canvas (Canvas): The tkinter canvas on which the ellipse will be drawn.
                radius_1 (int): The radius of the ellipse along its major axis.
                radius_2 (int): The radius of the ellipse along its minor axis.
                color (str): The fill color of the ellipse.

            Returns:
                None
        """
        super().__init__(canvas, color)
        self.half_r1: float = radius_1 / 2
        self.half_r2: float = radius_2 / 2
        self.shape: Any = self.get_shape()

    def get_shape(self) -> Any:
        """
            Create the ellipse shape on the canvas.

            Returns:
                Any: The shape object representing the ellipse.
        """
        print("Creating oval")
        points = ((-self.half_r1, -self.half_r2), (self.half_r1, self.half_r2))
        return self.canvas.create_oval(*points, fill=self.color, tags=("clickable" + str(Shape.counter)))

    def __str__(self) -> str:
        """
            Return a string representation of the ellipse.

            Returns:
                str: A string representation of the ellipse object.
        """
        return super().__str__() + ', "radius_1": ' + str(self.half_r1 * 2) + ', "radius_2": ' + str(
            self.half_r2 * 2) + '}'


# ______________________________________________________

class Triangle(Shape):
    def __init__(self, canvas: Canvas, base: int, height: int, color: str) -> None:
        """
               Initialize a Triangle object.

               Args:
                   canvas (Canvas): The tkinter canvas on which the triangle will be drawn.
                   base (int): The length of the base of the triangle.
                   height (int): The height of the triangle.
                   color (str): The fill color of the triangle.

               Returns:
                   None
               """
        super().__init__(canvas, color)
        self.base = base
        self.height = height
        self.shape = self.get_shape()

    def get_shape(self) -> Any:
        """
                Create the triangle shape on the canvas.

                Returns:
                    Any: The shape object representing the triangle.
                """
        print("creating triangle")
        x0: float = -self.base / 2
        y0: float = self.height / 2
        x1: float = self.base / 2
        y1: float = self.height / 2
        x2: float = 0
        y2: float = -self.height / 2
        return self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, tags=("clickable" + str(Shape.counter)),
                                          fill=self.color)

    def __str__(self) -> str:
        """
            Return a string representation of the triangle.

            Returns:
                str: A string representation of the triangle object.
        """
        return super().__str__() + ', "base": ' + str(self.base) + ', "height": ' + str(self.height) + '}'


# ______________________________________________________


class PolygonShape(Shape):
    def __init__(self, canvas: Canvas, color: str) -> None:
        """
                Initialize a PolygonShape object.

                Args:
                    canvas (Canvas): The tkinter canvas on which the polygon will be drawn.
                    color (str): The fill color of the polygon.

                Returns:
                    None
                """
        super().__init__(canvas, color)
        self.lines: List[Any] = []
        self.points: Union[List[List[float]], List[Tuple[float, float]]] = []
        self.shape: Any = None
        self.is_drawing: bool = False
        self.cursor: Any = None

    def start_draw(self) -> None:
        """
            Start drawing the polygon.

            Returns:
                None
        """
        print("Start drawing polygon")
        if self.is_drawing:
            return
        self.is_drawing = True
        self.bind_motion()
        self.cursor = self.canvas.create_oval(-5, -5, 5, 5, outline="black", width=2, tags="clickable_bbox")

    def bind_motion(self) -> None:
        """
            Bind motion events for drawing the polygon.

            Returns:
                None
        """
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Motion>", self.mouse_move)

    def mouse_move(self, event: Event) -> None:
        """
            Handle mouse movement during polygon drawing.

            Args:
                event (Event): The mouse event.

            Returns:
                None
        """
        if self.is_drawing:
            self.canvas.moveto(self.cursor, event.x - 5, event.y - 5)
            if len(self.points) >= 1:
                self.points[len(self.points) - 1][0] = event.x
                self.points[len(self.points) - 1][1] = event.y
                self.update_polygon()

    def add_point(self, event: Event) -> None:
        """
               Add a point to the polygon.

               Args:
                   event (Event): The mouse event.

               Returns:
                   None
               """
        print("Adding point")
        self.points.append([event.x, event.y])
        if len(self.points) == 1:
            self.points.append([event.x, event.y])
        self.update_polygon()

    def update_polygon(self) -> None:
        """
                Update the polygon shape on the canvas.

                Returns:
                    None
                """
        if self.shape:
            self.canvas.delete(self.shape)
        self.shape = self.canvas.create_polygon(self.points, fill=self.color, outline=self.outline_color,
                                                width=self.outline_width, tags=("clickable" + str(Shape.counter)))
        if self.cursor is not None:
            self.canvas.tag_raise(self.cursor)

    def stop_draw(self) -> None:
        """
                Stop drawing the polygon.

                Returns:
                    None
                """
        print("Stop drawing polygon")
        self.is_drawing = False
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.delete(self.cursor)
        self.cursor = None

    def on_select(self, event: Any) -> None:
        """
                Handle selection of the polygon.

                Args:
                    event (Any): The event triggering the selection.

                Returns:
                    None
                """
        if not self.is_drawing:
            super().on_select(event)

    def on_scale_object(self, event: Any) -> None:
        """
                Handle scaling of the polygon.

                Args:
                    event (Any): The event triggering the scaling.

                Returns:
                    None
                """
        bbox = self.canvas.bbox(self.shape)
        self.x, self.y = bbox[0], bbox[1]
        super().on_scale_object(event)

    def __str__(self) -> str:
        """
                Return a string representation of the polygon.

                Returns:
                    str: A string representation of the polygon object.
                """
        coords = self.canvas.coords(self.shape)
        self.points: List[List[float]] = []
        print(str(len(coords)))
        i = 0
        while i < (len(coords) - 1):
            print(str(i) + " " + str(coords[i]))
            self.points.append([coords[i], coords[i + 1]])
            i = i + 2
        return super().__str__() + ', "points": ' + str(self.points) + '}'


# ______________________________________________________

class Lines(Shape):
    def __init__(self, canvas: Canvas, color: str) -> None:
        """
               Initialize a Lines object.

               Args:
                   canvas (Canvas): The tkinter canvas on which the lines will be drawn.
                   color (str): The color of the lines.

               Returns:
                   None
               """
        if color == "white":
            color = "black"
        super().__init__(canvas, color)
        self.lines: set = set()
        self.drawn_points: List[List[int]] = []
        self.canvas.bind("<Button-1>", self.on_start_draw)
        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<ButtonRelease-1>", self.on_stop_draw)
        self.prev_x: int = 0
        self.prev_y: int = 0
        self.width: int = Shape.current_width
        Shape.line_mode = True

    def delete(self, **kwargs: Any) -> None:
        """
                Delete the lines from the canvas.

                Returns:
                    None
                """
        for line_id in self.lines:
            self.canvas.delete(line_id)

    def on_drag(self, event: Event) -> None:
        """
                Handle dragging of the lines.

                Args:
                    event (Event): The mouse event.

                Returns:
                    None
                """
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        for line_id in self.lines:
            self.canvas.move(line_id, dx, dy)
        self.last_x = event.x
        self.last_y = event.y

    def set_outline(self, outline_color: str, outline_width: int) -> None:
        """
                Set the outline color and width of the lines.

                Args:
                    outline_color (str): The color of the outline.
                    outline_width (int): The width of the outline.

                Returns:
                    None
                """
        self.outline_width = outline_width
        self.outline_color = outline_color
        for line_id in self.lines:
            self.canvas.itemconfig(line_id, width=outline_width)

    def set_color(self, color: str) -> None:
        """
                Set the color of the lines.

                Args:
                    color (str): The color to set.

                Returns:
                    None
                """
        self.color = color
        for line_id in self.lines:
            self.canvas.itemconfig(line_id, fill=color)

    def set_outline_color(self, shape: Any, color: str) -> None:
        """
               Set the outline color of the lines.

               Args:
                   shape: The shape object.
                   color (str): The color of the outline.

               Returns:
                   None
               """
        print("set_outline_color")

    def on_start_draw(self, event: Event) -> None:
        """
               Handle the start of drawing lines.

               Args:
                   event (Event): The mouse event.

               Returns:
                   None
               """
        self.prev_x, self.prev_y = event.x, event.y

    def on_draw(self, event: Event) -> None:
        """
                Handle drawing lines.

                Args:
                    event (Event): The mouse event.

                Returns:
                    None
                """
        x, y = event.x, event.y
        self.drawn_points.append([x, y])
        self.shape = self.canvas.create_line(self.prev_x, self.prev_y, x, y, fill=self.color, width=self.width,
                                             tags=("clickable" + str(Shape.counter)))
        self.lines.add(self.shape)
        self.prev_x, self.prev_y = x, y

    def draw_select_rect(self) -> None:
        """
               Draw the selection rectangle.

               Returns:
                   None
               """
        if Shape.select_bbox is not None:
            self.canvas.delete(Shape.select_bbox)
        if Shape.select_circle is not None:
            self.canvas.delete(Shape.select_circle)
        Shape.select_bbox = None
        Shape.select_circle = None

    def connect_points(self) -> None:
        """
               Connect the drawn points with lines.

               Returns:
                   None
               """
        for i in range(len(self.drawn_points) - 1):
            x1, y1 = self.drawn_points[i]
            x2, y2 = self.drawn_points[i + 1]
            line_id = self.canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.width)
            self.lines.add(line_id)

    def on_stop_draw(self, event: Event) -> None:
        """
               Handle the end of drawing lines.

               Args:
                   event (Event): The mouse event.

               Returns:
                   None
               """
        Shape.line_mode = False
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def __str__(self) -> str:
        """
               Return a string representation of the Lines object.

               Returns:
                   str: A string representation of the Lines object.
               """
        return super().__str__() + ', "width": ' + str(self.width) + ', "lines": ' + str(self.drawn_points) + '}'


# ______________________________________________________
class Eraser(Lines):
    def __init__(self, canvas: Canvas) -> None:
        """
                Initialize an Eraser object.

                Args:
                    canvas (Canvas): The tkinter canvas on which the eraser will be used.

                Returns:
                    None
                """
        super().__init__(canvas, "white")
        self.drawn_points: List[List[int]] = []

    def on_draw(self, event: Event) -> None:
        """
                Handle drawing with the eraser.

                Args:
                    event (Event): The mouse event.

                Returns:
                    None
                """
        x, y = event.x, event.y
        self.drawn_points.append([x, y])
        self.shape = self.canvas.create_line(self.prev_x, self.prev_y, x, y, fill="white", width=self.width,
                                             tags=("clickable" + str(Shape.counter)))
        self.lines.add(self.shape)
        self.prev_x, self.prev_y = x, y

    def connect_points(self) -> None:
        """
                Connect the drawn points with lines for the eraser.

                Returns:
                    None
                """
        for i in range(len(self.drawn_points) - 1):
            x1, y1 = self.drawn_points[i]
            x2, y2 = self.drawn_points[i + 1]
            line_id = self.canvas.create_line(x1, y1, x2, y2, fill="white", width=Shape.current_width)
            self.lines.add(line_id)

    def on_stop_draw(self, event: Event) -> None:
        """
                Handle the end of using the eraser.

                Args:
                    event (Event): The mouse event.

                Returns:
                    None
                """
        super().on_stop_draw(event)
        self.canvas.config(cursor="arrow")


# ______________________________________________________
class TextShape(Shape):
    def __init__(self, canvas: Canvas, text: str, font_family: str = "Arial", font_size: int = 12,
                 font_style: str = "normal", color: str = "black") -> None:
        """
               Initialize a TextShape object.

               Args:
                   canvas (Canvas): The tkinter canvas on which the text will be drawn.
                   text (str): The text content.
                   font_family (str): The font family.
                   font_size (int): The font size.
                   font_style (str): The font style.
                   color (str): The fill color of the text.

               Returns:
                   None
               """
        super().__init__(canvas, color)
        self.text: str = text
        self.font_family: str = font_family
        self.font_size: int = font_size
        self.font_style: str = font_style
        self.shape = None
        self.initial_x = 0
        self.initial_y = 0

    def on_drag_start(self, event):
        self.initial_x = event.x
        self.initial_y = event.y

    def add_text(self) -> None:
        """
                Add the text to the canvas.

                Returns:
                    None
                """
        self.shape = self.canvas.create_text(30, 30, text=self.text, fill=self.color,
                                             font=(self.font_family, self.font_size, self.font_style),
                                             tags=("clickable" + str(Shape.counter)))

    def set_outline(self, outline_color: str, outline_width: int) -> None:
        """
                Set the outline color and width of the text.

                Args:
                    outline_color (str): The color of the outline.
                    outline_width (int): The width of the outline.

                Returns:
                    None
                """
        print("set_outline_color")

    def set_outline_color(self, shape: Any, color: str) -> None:
        """
                Set the outline color of the text.

                Args:
                    shape: The shape.
                    color (str): The color of the outline.

                Returns:
                    None
                """
        print("set_outline_color")

    def __str__(self) -> str:
        return super().__str__() + ', "text": "' + self.text + '" , "font_family": "' + self.font_family + '" , "font_size": ' + str(
            self.font_size) + ', "font_style": "' + self.font_style + '"}'

    def set_position(self, x: int, y: int) -> None:
        """
        Set the position of the TextShape.

        Args:
            x (int): The x-coordinate of the new position.
            y (int): The y-coordinate of the new position.

        Returns:
            None
        """
        self.canvas.coords(self.shape, x, y)

    def set_color(self, color: str) -> None:
        """
        Set the fill color of the text.

        Args:
            color (str): The fill color.

        Returns:
            None
        """
        self.color = color
        self.canvas.itemconfig(self.shape, fill=self.color)