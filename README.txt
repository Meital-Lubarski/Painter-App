Shape Drawer GUI Application

Description:
The Drawing Application is a versatile program built using Python's Tkinter library. It allows users to draw various shapes, add text, erase, and perform other basic drawing actions on a canvas. The application provides a user-friendly interface with buttons for selecting drawing tools, changing colors, adjusting brush sizes, undoing actions, saving/loading work, and more.

Features:
In this drawing application, there is an option to flip the shape by dragging the red circle located at the bottom right corner of the shape's bounding box. When the user drags the red circle upwards, the shape flips.
This process allows the user to flip the shape easily and conveniently, useful in cases where immediate and easy shape flipping is desired. Dragging the red circle upwards enables the user to reposition the shape and focus on its orientation without the need for additional actions or special tools.

Color Selection: Users can choose the drawing color and outline color using a color picker.
Updated the color() function so that the color of the buttons changes according to the color chosen by the user.

Select Rectangle: Users can draw a selection rectangle around a shape for highlighting and manipulation.

Scale Shapes: Users can scale shapes by dragging, which is handled by the on_scale_object method.
The select circle provides a visual indication of the selected shape for highlighting and manipulation.
The select circle is drawn using an oval shape with a red outline and fill color.
It is positioned at the bottom right corner of the bounding box of the selected shape.
The select circle is clickable, allowing users to interact with it for scaling and manipulation purposes.

Type Hints Addition: Updated the codebase to include type hints for function parameters and return values.
Type hints improve code readability and maintainability by specifying the expected types of variables and function arguments.
Type hints also enable static type checkers to catch potential errors and improve code robustness during development.

Author:
Meital Lubarski
206480964
cse: meital
